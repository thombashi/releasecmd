import sys
import time
from random import uniform
from typing import List, Optional


class Retry:
    def __init__(self, total: int = 3, no_retry_returncodes: Optional[List[int]] = None) -> None:
        self.total = total

        if not no_retry_returncodes:
            self.no_retry_returncodes = []
        else:
            self.no_retry_returncodes = no_retry_returncodes


def _calc_backoff_time(attempt: int, backoff_factor: float = 0.5, jitter: float = 0.5) -> float:
    sleep_duration = backoff_factor * (2 ** max(0, attempt - 1))
    sleep_duration += uniform(0.5 * jitter, 1.5 * jitter)

    return sleep_duration


def sleep_before_retry(attempt: int, retries: int) -> float:
    sleep_duration = _calc_backoff_time(attempt)

    print(
        "Retrying in {:.2f} seconds ... (attempt={}/{})".format(sleep_duration, attempt, retries),
        file=sys.stderr,
    )

    time.sleep(sleep_duration)

    return sleep_duration
