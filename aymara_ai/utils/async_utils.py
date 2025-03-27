# Simple event loop management for running async code from any context
import asyncio
import concurrent.futures
import threading
from typing import Awaitable, TypeVar

# Global thread executor for running async code in Jupyter and other contexts
_THREAD_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=1)

# Application-wide event loop
_APP_LOOP = None
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
    # Try to get the running loop first (works in async contexts)
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        # No running loop, create/return our application loop
        pass

    global _APP_LOOP

    with _LOOP_LOCK:
        # Check if we have a valid app loop already
        if _APP_LOOP is None or _APP_LOOP.is_closed():
            # Create new loop and set as default for this thread
            _APP_LOOP = asyncio.new_event_loop()
            asyncio.set_event_loop(_APP_LOOP)

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
        # We're in an event loop already (could be Jupyter)
        # Use run_coroutine_threadsafe to avoid blocking the current loop
        return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass

    # Standard synchronous context
    loop = get_loop()
    return loop.run_until_complete(coro)
