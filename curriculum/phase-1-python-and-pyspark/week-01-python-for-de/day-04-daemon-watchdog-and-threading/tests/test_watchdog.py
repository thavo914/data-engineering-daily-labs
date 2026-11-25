"""Tests for Day 04: Daemon Executor Watchdog with Grace Period."""

import importlib.util
import os
import threading
from pathlib import Path

DAY_DIR = Path(__file__).resolve().parent.parent
TARGET_DIR = "solution" if os.getenv("USE_SOLUTION") == "1" else "starter"
MODULE_PATH = DAY_DIR / TARGET_DIR / "watchdog.py"

spec = importlib.util.spec_from_file_location("day04_watchdog", MODULE_PATH)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

ExecutorWatchdog = mod.ExecutorWatchdog


def test_transient_core_drop_resets_grace_timer() -> None:
    cores = 0
    triggered = 0

    def on_unhealthy() -> None:
        nonlocal triggered
        triggered += 1

    wd = ExecutorWatchdog(
        get_active_cores=lambda: cores,
        on_unhealthy=on_unhealthy,
        min_cores=2,
        grace_period_sec=10.0,
    )

    assert wd.evaluate_once(now=100.0) is True
    assert wd.evaluate_once(now=105.0) is True
    assert triggered == 0

    # Cores recover before grace period expires
    cores = 4
    assert wd.evaluate_once(now=108.0) is True

    # Drop again: grace timer must start fresh from t=110.0
    cores = 0
    assert wd.evaluate_once(now=110.0) is True
    assert wd.evaluate_once(now=119.0) is True
    assert triggered == 0

    # Grace period exceeded at t=120.0
    assert wd.evaluate_once(now=120.0) is False
    assert triggered == 1


def test_background_daemon_thread_triggers_on_unhealthy() -> None:
    done = threading.Event()
    wd = ExecutorWatchdog(
        get_active_cores=lambda: 0,
        on_unhealthy=done.set,
        min_cores=1,
        check_interval_sec=0.01,
        grace_period_sec=0.03,
    )
    wd.start()
    try:
        assert done.wait(timeout=1.0), "Watchdog did not trigger within 1 second"
    finally:
        wd.stop()
