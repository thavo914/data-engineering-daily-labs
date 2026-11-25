"""Tests for Day 05: Real-time streaming Popen runner with safe timeout handling."""

import importlib.util
import os
import sys
from pathlib import Path

DAY_DIR = Path(__file__).resolve().parent.parent
TARGET_DIR = "solution" if os.getenv("USE_SOLUTION") == "1" else "starter"
MODULE_PATH = DAY_DIR / TARGET_DIR / "command_runner.py"

spec = importlib.util.spec_from_file_location("day05_command_runner", MODULE_PATH)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

run_streaming_command = mod.run_streaming_command


def test_streams_stdout_and_stderr_in_real_time() -> None:
    seen: list[tuple[str, str]] = []
    script = "import sys; print('model_1_ok', flush=True); print('warn_msg', file=sys.stderr, flush=True)"
    result = run_streaming_command(
        [sys.executable, "-c", script],
        timeout_sec=5.0,
        on_line=lambda stream, line: seen.append((stream, line)),
    )

    assert result.returncode == 0
    assert result.timed_out is False
    assert ("stdout", "model_1_ok") in seen
    assert ("stderr", "warn_msg") in seen


def test_timeout_preserves_partial_logs_instead_of_going_blind() -> None:
    seen: list[tuple[str, str]] = []
    script = "import time; print('starting_slow_model', flush=True); time.sleep(5)"
    result = run_streaming_command(
        [sys.executable, "-c", script],
        timeout_sec=0.3,
        on_line=lambda stream, line: seen.append((stream, line)),
    )

    assert result.timed_out is True
    assert result.returncode == -1
    assert "starting_slow_model" in result.stdout
    assert ("stdout", "starting_slow_model") in seen
