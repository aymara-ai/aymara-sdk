# Simple event loop management for running async code from any context
import asyncio
import concurrent.futures
import logging
import sys
import threading
from typing import Awaitable, Optional, TypeVar, cast

logger = logging.getLogger(__name__)

# Global thread executor for running async code in Jupyter and other contexts
_THREAD_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=1)

# Application-wide event loop
_APP_LOOP: Optional[asyncio.AbstractEventLoop] = None
_LOOP_LOCK = threading.RLock()
T = TypeVar("T")


def _in_pytest_context() -> bool:
    """Check if we are running in a pytest context."""
    return any("pytest" in arg for arg in sys.argv)


def _get_running_loop() -> Optional[asyncio.AbstractEventLoop]:
    """Try to get the currently running event loop."""
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return None


def get_loop() -> asyncio.AbstractEventLoop:
    """
    Get the most appropriate event loop for the current context.

    Follows this priority order:
    1. Currently running loop
    2. Pytest loop (if in pytest context)
    3. Global app loop

    Returns:
        The appropriate event loop for the current context
    """
    # Priority 1: Currently running loop
    loop = _get_running_loop()
    if loop:
        return loop

    # Priority 2: Pytest loop
    if _in_pytest_context():
        try:
            # Try to find the pytest-asyncio loop
            import pytest_asyncio

            if hasattr(pytest_asyncio, "plugin") and hasattr(pytest_asyncio.plugin, "_event_loop"):
                loop = getattr(pytest_asyncio.plugin, "_event_loop")
                if loop and not loop.is_closed():
                    logger.debug(f"Found pytest_asyncio loop: {loop!r}, id={id(loop)}")
                    return cast(asyncio.AbstractEventLoop, loop)

            # Fallback to default event loop in pytest context
            loop = asyncio.get_event_loop_policy().get_event_loop()
            if not loop.is_closed():
                return loop
        except (ImportError, AttributeError):
            pass

    # Priority 3: Global app loop
    global _APP_LOOP
    with _LOOP_LOCK:
        if _APP_LOOP is None or _APP_LOOP.is_closed():
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
    # Case 1: Already a future
    if isinstance(coro, asyncio.Future):
        loop = coro.get_loop()
        if not coro.done():
            return loop.run_until_complete(coro)
        return coro.result()

    # Case 2: Jupyter notebook environment
    try:
        import IPython

        if IPython.get_ipython() is not None:

            def run_in_thread():
                loop = get_loop()
                return loop.run_until_complete(coro)

            return _THREAD_EXECUTOR.submit(run_in_thread).result()
    except (ImportError, AttributeError):
        pass

    # Case 3: Already in a running loop
    current_loop = _get_running_loop()
    if current_loop:
        future = asyncio.run_coroutine_threadsafe(coro, current_loop)
        return future.result()

    # Case 4: Get the best loop for our context and run the coroutine
    loop = get_loop()
    try:
        return loop.run_until_complete(coro)
    except Exception as e:
        logger.error(f"Error running coroutine: {e}")
        import traceback

        logger.error(traceback.format_exc())
        raise
