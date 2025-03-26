# Event loop singleton for running async code from sync contexts
import asyncio
import concurrent.futures
from typing import Awaitable, TypeVar

_EVENT_LOOP = None
T = TypeVar("T")


def get_event_loop():
    """Get or create a singleton event loop for running async code from sync contexts."""
    global _EVENT_LOOP
    if _EVENT_LOOP is None or _EVENT_LOOP.is_closed():
        _EVENT_LOOP = asyncio.get_event_loop()
    return _EVENT_LOOP


def run_async(coro: Awaitable[T]) -> T:
    """Run an async coroutine from any context using a thread executor."""

    # This function will run in a separate thread
    def thread_runner():
        # Get or create an event loop for this thread
        try:
            # For Python 3.7+
            loop = asyncio.get_event_loop()
        except RuntimeError:
            # "There is no current event loop in thread"
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Run the coroutine in this thread's event loop
        return loop.run_until_complete(coro)

    # Use a ThreadPoolExecutor to run our function in a separate thread
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(thread_runner)
        return future.result()  # This blocks until the future completes
