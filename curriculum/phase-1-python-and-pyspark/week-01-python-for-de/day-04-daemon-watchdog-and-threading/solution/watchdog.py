"""Day 04 Solution: Daemon Executor Watchdog with Grace Period."""

import threading
import time
from typing import Callable, Optional


class ExecutorWatchdog:
    """Monitors active worker cores and triggers a callback after grace_period_sec."""

    def __init__(
        self,
        get_active_cores: Callable[[], int],
        on_unhealthy: Callable[[], None],
        min_cores: int = 1,
        check_interval_sec: float = 0.05,
        grace_period_sec: float = 0.2,
        clock_fn: Callable[[], float] = time.monotonic,
    ) -> None:
        self._get_active_cores = get_active_cores
        self._on_unhealthy = on_unhealthy
        self._min_cores = min_cores
        self._check_interval_sec = check_interval_sec
        self._grace_period_sec = grace_period_sec
        self._clock_fn = clock_fn
        self._unhealthy_since: Optional[float] = None
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def evaluate_once(self, now: Optional[float] = None) -> bool:
        """Evaluate current core count once. Return True if healthy or within grace period."""
        current_time = self._clock_fn() if now is None else now
        cores = self._get_active_cores()

        if cores >= self._min_cores:
            self._unhealthy_since = None
            return True

        if self._unhealthy_since is None:
            self._unhealthy_since = current_time

        if current_time - self._unhealthy_since >= self._grace_period_sec:
            self._on_unhealthy()
            self._stop_event.set()
            return False

        return True

    def _run_loop(self) -> None:
        while not self._stop_event.is_set():
            self.evaluate_once()
            self._stop_event.wait(self._check_interval_sec)

    def start(self) -> None:
        """Start the daemon watchdog thread."""
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, name="executor-watchdog", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Signal the watchdog to stop and join the thread."""
        self._stop_event.set()
        if self._thread is not None and self._thread.is_alive():
            self._thread.join(timeout=2.0)
