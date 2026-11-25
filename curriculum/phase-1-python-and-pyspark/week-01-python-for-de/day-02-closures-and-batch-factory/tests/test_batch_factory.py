"""Tests for Day 02: Closure Factory with Enclosing Cache & Resource Hygiene."""

import importlib.util
import os
from pathlib import Path

import pytest

DAY_DIR = Path(__file__).resolve().parent.parent
TARGET_DIR = "solution" if os.getenv("USE_SOLUTION") == "1" else "starter"
MODULE_PATH = DAY_DIR / TARGET_DIR / "batch_factory.py"

spec = importlib.util.spec_from_file_location("day02_batch_factory", MODULE_PATH)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

create_batch_processor = mod.create_batch_processor


class FakeBatch:
    def __init__(self, rows: int) -> None:
        self.rows = rows
        self.persisted = False
        self.unpersisted = False

    def persist(self) -> "FakeBatch":
        self.persisted = True
        return self

    def unpersist(self) -> None:
        self.unpersisted = True

    def is_empty(self) -> bool:
        return self.rows == 0


def test_empty_batch_short_circuits_and_unpersists() -> None:
    opened = 0
    written = 0

    def open_fn(name: str) -> str:
        nonlocal opened
        opened += 1
        return f"handle:{name}"

    def write_fn(handle: str, batch: FakeBatch, batch_id: int) -> None:
        nonlocal written
        written += 1

    proc = create_batch_processor("orders", open_fn, write_fn)
    batch = FakeBatch(rows=0)
    proc(batch, 1)

    assert batch.persisted and batch.unpersisted
    assert opened == 0
    assert written == 0


def test_handle_cached_across_batches() -> None:
    opened = 0
    seen_batches: list[int] = []

    def open_fn(name: str) -> str:
        nonlocal opened
        opened += 1
        return f"handle:{name}:{opened}"

    def write_fn(handle: str, batch: FakeBatch, batch_id: int) -> None:
        seen_batches.append(batch_id)

    proc = create_batch_processor("orders", open_fn, write_fn)
    b1, b2 = FakeBatch(10), FakeBatch(20)
    proc(b1, 1)
    proc(b2, 2)

    assert opened == 1
    assert seen_batches == [1, 2]
    assert b1.unpersisted and b2.unpersisted


def test_exception_evicts_cache_and_still_unpersists() -> None:
    opened = 0

    def open_fn(name: str) -> str:
        nonlocal opened
        opened += 1
        return f"handle:{opened}"

    def flaky_write(handle: str, batch: FakeBatch, batch_id: int) -> None:
        if batch_id == 1:
            raise RuntimeError("Schema changed")

    proc = create_batch_processor("orders", open_fn, flaky_write)
    b1 = FakeBatch(5)
    with pytest.raises(RuntimeError, match="Schema changed"):
        proc(b1, 1)

    assert b1.unpersisted

    b2 = FakeBatch(5)
    proc(b2, 2)
    assert opened == 2
    assert b2.unpersisted
