# Simple event loop management for running async code from any context
import asyncio
import concurrent.futures
import inspect
import logging
import threading
from typing import Awaitable, Optional, TypeVar, cast

logger = logging.getLogger(__name__)

# Global thread executor for running async code in Jupyter and other contexts
_THREAD_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=1)

# Application-wide event loop
_APP_LOOP: Optional[asyncio.AbstractEventLoop] = None
_LOOP_LOCK = threading.RLock()
T = TypeVar("T")


def _get_caller_info() -> str:
    """Helper function to get caller information for debugging."""
    frame = inspect.currentframe()
    caller_info = "unknown"
    if frame and frame.f_back:
        caller_frame = frame.f_back
        caller_info = f"{caller_frame.f_code.co_filename}:{caller_frame.f_lineno} ({caller_frame.f_code.co_name})"
    return caller_info


def _try_get_pytest_loop() -> Optional[asyncio.AbstractEventLoop]:
    """Helper to extract pytest loop detection logic."""
    try:
        import pytest
        import pytest_asyncio

        # Check if we're in pytest with py.path or pathlib
        if hasattr(pytest, "config"):
            # Try to find the pytest-asyncio loop
            if hasattr(pytest_asyncio, "plugin") and hasattr(pytest_asyncio.plugin, "_event_loop"):
                loop = getattr(pytest_asyncio.plugin, "_event_loop")
                if loop and not loop.is_closed():
                    logger.debug(f"Found pytest_asyncio loop: {loop!r}, id={id(loop)}")
                    return cast(asyncio.AbstractEventLoop, loop)
    except (ImportError, AttributeError):
        pass
    return None


def get_loop(*, create_new: bool = False) -> asyncio.AbstractEventLoop:
    """
    Get the appropriate event loop for any context.

    Works consistently in:
    - Synchronous code
    - Asyncio contexts
    - pytest with asyncio fixtures
    - Jupyter notebooks

    Args:
        create_new: If True, creates a new loop even if no existing loop is found.
                   This should be set to True when a temporary loop is needed for a single operation.

    Returns:
        The appropriate event loop for the current context
    """

    # Priority 1: Get running loop if possible
    try:
        loop = asyncio.get_running_loop()
        return loop
    except RuntimeError:
        logger.debug("No running loop found")

    # Priority 2: Get pytest loop if in pytest environment
    pytest_loop = _try_get_pytest_loop()
    if pytest_loop:
        return pytest_loop

    # Priority 3: If create_new is True, return a new loop without setting as default
    if create_new:
        loop = asyncio.new_event_loop()
        logger.debug(f"Created new temporary loop: {loop!r}, id={id(loop)}")
        return loop

    # Priority 4: Use or create global app loop
    global _APP_LOOP
    with _LOOP_LOCK:
        if _APP_LOOP is None or _APP_LOOP.is_closed():
            # Create new loop and set as default for this thread
            _APP_LOOP = asyncio.new_event_loop()
            asyncio.set_event_loop(_APP_LOOP)
            logger.debug(f"Created new global app loop: {_APP_LOOP!r}, id={id(_APP_LOOP)}")

    return _APP_LOOP


def run_async(coro: Awaitable[T]) -> T:
    """
    Run a coroutine in any context (sync, async, pytest, jupyter).

    This function ensures consistent execution across all contexts,
    preventing 'Future attached to different loop' errors by using a thread
    executor when needed.

    Args:
        coro: Coroutine to run

    Returns:
        Result of the coroutine execution
    """

    # If this is already a future, just return its result
    if isinstance(coro, asyncio.Future):
        loop = coro.get_loop()
        # If the future is not done, we need to ensure it completes
        if not coro.done():
            return loop.run_until_complete(coro)
        return coro.result()

    # Special case for Jupyter environment
    try:
        import IPython

        if IPython.get_ipython() is not None:
            # We're in a Jupyter notebook but no event loop is running
            # Run in a separate thread to avoid interfering with Jupyter's event loop
            def run_in_thread():
                loop = get_loop()
                return loop.run_until_complete(coro)

            global _THREAD_EXECUTOR
            return _THREAD_EXECUTOR.submit(run_in_thread).result()
    except (ImportError, AttributeError):
        pass

    # Try to get the current running loop
    try:
        loop = asyncio.get_running_loop()
        # We're in an event loop already
        # Use run_coroutine_threadsafe to avoid blocking the current loop
        future = asyncio.run_coroutine_threadsafe(coro, loop)
        return future.result()
    except RuntimeError:
        logger.debug("No running loop found in run_async")

    # Check for pytest loop again (in case it wasn't detected earlier)
    pytest_loop = _try_get_pytest_loop()
    if pytest_loop:
        return pytest_loop.run_until_complete(coro)

    # No running event loop - use the global app loop
    # For concurrent tests, we need a persistent loop that doesn't close
    # after each operation, so we use get_loop() instead of a temporary loop
    loop = get_loop()
    try:
        result = loop.run_until_complete(coro)
        return result
    except Exception as e:
        logger.error(f"Error running coroutine: {e}")
        import traceback

        logger.error(traceback.format_exc())
        raise
