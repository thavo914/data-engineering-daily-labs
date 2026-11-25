"""Day 03 Solution: Selective OCC Concurrency Retry with Snapshot Reload."""

import time
from typing import Callable, Optional, TypeVar

T = TypeVar("T")

CONCURRENCY_KEYWORDS = (
    "MetadataChangedException",
    "ConcurrentAppendException",
    "ConcurrentTransactionException",
    "ConcurrentDeleteReadException",
)


def is_concurrency_error(exc: Exception) -> bool:
    """Return True if the exception represents a retryable OCC conflict."""
    err_str = str(exc)
    return any(kw in err_str for kw in CONCURRENCY_KEYWORDS)


def execute_with_occ_retry(
    operation_fn: Callable[[], T],
    max_attempts: int = 3,
    base_backoff_sec: float = 2.0,
    on_retry_reload: Optional[Callable[[], None]] = None,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> T:
    """Execute operation_fn with selective OCC retry, linear backoff, and reload hook."""
    for attempt in range(1, max_attempts + 1):
        try:
            return operation_fn()
        except Exception as exc:
            if is_concurrency_error(exc) and attempt < max_attempts:
                sleep_fn(base_backoff_sec * attempt)
                if on_retry_reload is not None:
                    on_retry_reload()
            else:
                raise
    raise RuntimeError("Unreachable retry state")
