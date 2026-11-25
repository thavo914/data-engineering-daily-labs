"""Tests for Day 03: Selective OCC Concurrency Retry with Snapshot Reload."""

import importlib.util
import os
from pathlib import Path

import pytest

DAY_DIR = Path(__file__).resolve().parent.parent
TARGET_DIR = "solution" if os.getenv("USE_SOLUTION") == "1" else "starter"
MODULE_PATH = DAY_DIR / TARGET_DIR / "occ_retry.py"

spec = importlib.util.spec_from_file_location("day03_occ_retry", MODULE_PATH)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

execute_with_occ_retry = mod.execute_with_occ_retry


def test_succeeds_after_transient_occ_conflict() -> None:
    calls = 0
    reloads = 0
    sleeps: list[float] = []

    def op() -> str:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise RuntimeError("ConcurrentAppendException: files added by compaction")
        return "committed"

    def reload_snapshot() -> None:
        nonlocal reloads
        reloads += 1

    result = execute_with_occ_retry(
        op,
        max_attempts=3,
        base_backoff_sec=2.0,
        on_retry_reload=reload_snapshot,
        sleep_fn=sleeps.append,
    )
    assert result == "committed"
    assert calls == 3
    assert reloads == 2
    assert sleeps == [2.0, 4.0]


def test_non_concurrency_error_fails_immediately() -> None:
    calls = 0
    sleeps: list[float] = []

    def op() -> None:
        nonlocal calls
        calls += 1
        raise ValueError("Invalid schema column")

    with pytest.raises(ValueError, match="Invalid schema column"):
        execute_with_occ_retry(op, max_attempts=3, sleep_fn=sleeps.append)

    assert calls == 1
    assert sleeps == []


def test_exhausted_occ_retries_raises_last_error() -> None:
    sleeps: list[float] = []

    def op() -> None:
        raise RuntimeError("MetadataChangedException: concurrent ALTER TABLE")

    with pytest.raises(RuntimeError, match="MetadataChangedException"):
        execute_with_occ_retry(op, max_attempts=3, base_backoff_sec=1.5, sleep_fn=sleeps.append)

    assert sleeps == [1.5, 3.0]
