"""Day 05 Starter (Buggy): Blind subprocess.run hides logs on timeout."""

import subprocess
from dataclasses import dataclass
from typing import Callable, List, Optional


@dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False


def run_streaming_command(
    cmd: List[str],
    timeout_sec: Optional[float] = None,
    on_line: Optional[Callable[[str, str], None]] = None,
) -> CommandResult:
    """
    BUGGY IMPLEMENTATION:
    Uses subprocess.run(capture_output=True) which buffers all output until exit
    and loses real-time visibility when a timeout occurs.

    TODO: Refactor to subprocess.Popen + concurrent stdout/stderr reader threads.
    """
    _ = on_line
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout_sec,
        shell=False,
    )
    return CommandResult(
        returncode=proc.returncode,
        stdout=proc.stdout,
        stderr=proc.stderr,
        timed_out=False,
    )
