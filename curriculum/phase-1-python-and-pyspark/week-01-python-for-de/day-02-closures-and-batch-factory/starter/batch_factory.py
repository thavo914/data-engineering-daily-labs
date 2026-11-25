"""Day 02 Starter: Closure Factory with Enclosing Cache & Resource Hygiene."""

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
        _ = (_handle_cache, table_name, open_table_fn, write_fn, batch_df, batch_id)
        # TODO:
        # 1. Call persisted = batch_df.persist()
        # 2. Wrap logic in try ... except ... finally: persisted.unpersist()
        # 3. Short-circuit if persisted.is_empty()
        # 4. Lazily populate and reuse _handle_cache[table_name] via open_table_fn(table_name)
        # 5. Call write_fn(handle, persisted, batch_id)
        # 6. On any exception during write_fn, evict table_name from _handle_cache and re-raise
        raise NotImplementedError("Implement process_batch closure")

    return process_batch
