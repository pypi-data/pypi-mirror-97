from typing import Callable, Optional, Any, Iterable, Mapping
import time
import threading


class BackoffThread(threading.Thread):
    """
    Executes an operation function defined by 'request' with a backoff type until a timeout is reached. Does so threaded

    Args are passed to the operation function and are updated each time.

    An operation function MUST either return a dict of args to pass to the next iteration of the operation function OR
        return True to signify that no more iterations are required. Any other return types will break.
    """
    def __init__(self, timeout_seconds: int, request: Callable, backoff_type: str = 'exponential', **args) -> None:
        super().__init__()
        self.timeout_seconds: int = timeout_seconds
        self.request: Callable = request
        self.backoff_type: str = backoff_type
        self.args = args

    def run(self) -> None:
        """
        Runs the chosen backoff algorithm
        """
        if self.backoff_type == 'exponential':
            self.exponential_backoff()
        elif self.backoff_type == 'linear':
            self.linear_backoff()

    def exponential_backoff(self):
        """
        Exponential backoff uses a power of 2 to increase the length of time to wait between retries.
        """
        exponent: int = 1
        delay = pow(2, exponent)

        while delay < self.timeout_seconds and self.args is not True:
            self.args = self.request(**self.args)

            time.sleep(delay)

            exponent += 1
            delay = pow(2, exponent)

    def linear_backoff(self):
        """
        Linear backoff waits the same amount of time between each backoff. By default, 2s between each attempt.
        """
        delay = 0

        while delay < self.timeout_seconds and self.args is not True:
            self.args = self.request(**self.args)

            time.sleep(2)

            delay += 2


def backoff(request: Callable, timeout_seconds: int = 30, backoff_type: str = 'exponential', **args) -> BackoffThread:
    """
    Helper function spawns a backoff thread, starts it, and returns it.

    Read the docs above in BackoffThread class to better understand the parameters to this helper function.
    """
    backoff_thread: BackoffThread = BackoffThread(timeout_seconds, request, backoff_type, **args)
    backoff_thread.start()
    return backoff_thread
