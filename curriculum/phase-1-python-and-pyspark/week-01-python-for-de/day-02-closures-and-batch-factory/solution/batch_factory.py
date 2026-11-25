"""Day 02 Solution: Closure Factory with Enclosing Cache & Resource Hygiene."""

from typing import Any, Callable, Protocol


class MicroBatch(Protocol):
    def persist(self) -> "MicroBatch": ...
    def unpersist(self) -> None: ...
    def is_empty(self) -> bool: ...


def create_batch_processor(
    table_name: str,
    open_table_fn: Callable[[str], Any],
    write_fn: Callable[[Any, MicroBatch, int], None],
) -> Callable[[MicroBatch, int], None]:
    """Return a foreachBatch-compatible closure with handle caching and cleanup."""
    _handle_cache: dict[str, Any] = {}

    def process_batch(batch_df: MicroBatch, batch_id: int) -> None:
        persisted = batch_df.persist()
        try:
            if persisted.is_empty():
                return

            if table_name not in _handle_cache:
                _handle_cache[table_name] = open_table_fn(table_name)

            write_fn(_handle_cache[table_name], persisted, batch_id)
        except Exception:
            _handle_cache.pop(table_name, None)
            raise
        finally:
            persisted.unpersist()

    return process_batch
