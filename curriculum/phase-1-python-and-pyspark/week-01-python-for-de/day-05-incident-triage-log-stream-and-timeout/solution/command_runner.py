"""Day 05 Solution: Real-time streaming Popen runner with safe timeout handling."""

import subprocess
import threading
from dataclasses import dataclass
from typing import IO, Callable, List, Optional


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
    """Execute cmd while streaming stdout/stderr line-by-line and preserving logs on timeout."""
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=False,
        bufsize=1,
    )

    stdout_lines: List[str] = []
    stderr_lines: List[str] = []

    def _reader(stream: Optional[IO[str]], sink: List[str], stream_name: str) -> None:
        if stream is None:
            return
        try:
            for line in iter(stream.readline, ""):
                sink.append(line)
                cleaned = line.rstrip("\r\n")
                if on_line is not None and cleaned:
                    on_line(stream_name, cleaned)
        finally:
            stream.close()

    t_out = threading.Thread(target=_reader, args=(process.stdout, stdout_lines, "stdout"), daemon=True)
    t_err = threading.Thread(target=_reader, args=(process.stderr, stderr_lines, "stderr"), daemon=True)
    t_out.start()
    t_err.start()

    timed_out = False
    try:
        returncode = process.wait(timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        timed_out = True
        process.kill()
        process.wait()
        returncode = -1
    finally:
        t_out.join(timeout=2.0)
        t_err.join(timeout=2.0)

    return CommandResult(
        returncode=returncode,
        stdout="".join(stdout_lines),
        stderr="".join(stderr_lines),
        timed_out=timed_out,
    )
