# Simple event loop management for running async code from any context
import asyncio
import concurrent.futures
import inspect
import logging
import threading
from typing import Awaitable, Optional, TypeVar, cast

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("aymara.async_utils")

# Global thread executor for running async code in Jupyter and other contexts
_THREAD_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=1)

# Application-wide event loop
_APP_LOOP: Optional[asyncio.AbstractEventLoop] = None
_LOOP_LOCK = threading.RLock()
T = TypeVar("T")


def get_loop() -> asyncio.AbstractEventLoop:
    """
    Get the appropriate event loop for any context.

    Works consistently in:
    - Synchronous code
    - Asyncio contexts
    - pytest with asyncio fixtures
    - Jupyter notebooks

    Returns:
        The appropriate event loop for the current context
    """
    # Get calling function info for debugging
    frame = inspect.currentframe()
    caller_info = "unknown"
    if frame and frame.f_back:
        caller_frame = frame.f_back
        caller_info = f"{caller_frame.f_code.co_filename}:{caller_frame.f_lineno} ({caller_frame.f_code.co_name})"
    logger.debug(f"get_loop() called from {caller_info}")

    # Try to get the running loop first (works in async contexts)
    loop: Optional[asyncio.AbstractEventLoop] = None
    try:
        loop = asyncio.get_running_loop()
        logger.debug(f"Found running loop: {loop!r}, id={id(loop)}")
        return loop

    except RuntimeError:
        logger.debug("No running loop found")
        # No running loop, check if we're in pytest
        try:
            # Try to import pytest and use any existing loop
            import pytest
            import pytest_asyncio

            logger.debug(f"pytest imported: {pytest!r}")

            # Check if we're in pytest with py.path or pathlib
            if hasattr(pytest, "config"):
                logger.debug(f"pytest.config exists: {pytest.config!r}")
                logger.debug(f"pytest_asyncio: {pytest_asyncio!r}")
                logger.debug(f"pytest_asyncio.plugin exists: {hasattr(pytest_asyncio, 'plugin')}")

                if hasattr(pytest_asyncio, "plugin"):
                    logger.debug(f"plugin: {pytest_asyncio.plugin!r}")
                    logger.debug(f"plugin has _event_loop: {hasattr(pytest_asyncio.plugin, '_event_loop')}")

                    if hasattr(pytest_asyncio.plugin, "_event_loop"):
                        loop = getattr(pytest_asyncio.plugin, "_event_loop")
                        logger.debug(f"Using pytest_asyncio loop: {loop!r}, id={id(loop)}")

                # Try to find the event_loop fixture using getattr to avoid mypy errors
                pytest_module = pytest
                if hasattr(pytest_module, "_pytest"):
                    pytest_internal = getattr(pytest_module, "_pytest")
                    if hasattr(pytest_internal, "fixtures"):
                        logger.debug("Checking for event_loop fixture")
                        fixture_manager = getattr(pytest.config, "_fixturemanager", None)
                        if fixture_manager:
                            event_loop_fixture = fixture_manager.getfixturedefs("event_loop", None)
                            logger.debug(f"event_loop fixture: {event_loop_fixture!r}")
        except (ImportError, AttributeError) as e:
            logger.debug(f"Error inspecting pytest: {e}")

    global _APP_LOOP

    with _LOOP_LOCK:
        logger.debug(f"Current _APP_LOOP: {_APP_LOOP!r}, id={id(_APP_LOOP) if _APP_LOOP else None}")
        _APP_LOOP = loop
        # Check if we have a valid app loop already
        if _APP_LOOP is None or _APP_LOOP.is_closed():
            # Create new loop and set as default for this thread
            _APP_LOOP = asyncio.new_event_loop()
            asyncio.set_event_loop(_APP_LOOP)
            logger.debug(f"Created new loop: {_APP_LOOP!r}, id={id(_APP_LOOP)}")
        else:
            logger.debug(f"Using existing loop: {_APP_LOOP!r}, id={id(_APP_LOOP)}")

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
    # Get calling function info for debugging
    frame = inspect.currentframe()
    caller_info = "unknown"
    if frame and frame.f_back:
        caller_frame = frame.f_back
        caller_info = f"{caller_frame.f_code.co_filename}:{caller_frame.f_lineno} ({caller_frame.f_code.co_name})"
    logger.debug(f"run_async() called from {caller_info} with coroutine {coro!r}")

    # If this is already a future, just return its result
    if isinstance(coro, asyncio.Future):
        loop = coro.get_loop()
        logger.debug(f"Input is a Future with loop {loop!r}, id={id(loop)}")
        # If the future is not done, we need to ensure it completes
        if not coro.done():
            logger.debug("Future not done, running with loop.run_until_complete()")
            return loop.run_until_complete(coro)
        logger.debug("Future already done, returning result")
        return coro.result()

    # First check for pytest environment and ensure we're using the pytest loop
    try:
        import pytest
        import pytest_asyncio

        # Check if we're running under pytest
        if hasattr(pytest, "config"):
            logger.debug("Running under pytest, trying to use pytest event loop")
            loop = None

            # Try to find the pytest-asyncio loop
            if hasattr(pytest_asyncio, "plugin") and hasattr(pytest_asyncio.plugin, "_event_loop"):
                loop = cast(asyncio.AbstractEventLoop, getattr(pytest_asyncio.plugin, "_event_loop"))
                logger.debug(f"Found pytest_asyncio loop: {loop!r}, id={id(loop)}")
                if loop and not loop.is_closed():
                    # Run the coroutine in the pytest loop
                    return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except (ImportError, AttributeError, RuntimeError) as e:
        logger.debug(f"Error trying to use pytest loop: {e}")

    # Check if we're in a Jupyter environment
    try:
        import IPython

        if IPython.get_ipython() is not None:
            # We're in a Jupyter notebook but no event loop is running
            # Run in a separate thread to avoid interfering with Jupyter's event loop
            def run_in_thread():
                loop = get_loop()  # Use the global loop getter
                return loop.run_until_complete(coro)

            global _THREAD_EXECUTOR
            return _THREAD_EXECUTOR.submit(run_in_thread).result()
    except (ImportError, AttributeError):
        pass

    # Try to get the current running loop
    try:
        loop = asyncio.get_running_loop()
        logger.debug(f"Found running loop in run_async: {loop!r}, id={id(loop)}")
        # We're in an event loop already (could be Jupyter)
        # Use run_coroutine_threadsafe to avoid blocking the current loop
        logger.debug("Using run_coroutine_threadsafe")
        future = asyncio.run_coroutine_threadsafe(coro, loop)
        logger.debug(f"Created future: {future!r}, in loop {loop!r}")
        return future.result()
    except RuntimeError:
        logger.debug("No running loop found in run_async")

    # Standard synchronous context - make our app loop reuse the global loop
    global _APP_LOOP
    if _APP_LOOP is None or _APP_LOOP.is_closed():
        logger.debug("Creating a new event loop for synchronous context")
        _APP_LOOP = asyncio.new_event_loop()
        asyncio.set_event_loop(_APP_LOOP)

    logger.debug(f"Using app loop: {_APP_LOOP!r}, id={id(_APP_LOOP)}")
    try:
        result = _APP_LOOP.run_until_complete(coro)
        logger.debug("Coroutine completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error running coroutine: {e}")
        # Print traceback for debugging
        import traceback

        logger.error(traceback.format_exc())
        raise
