import math
from collections.abc import AsyncIterator, Callable, Coroutine
from typing import Any, TypeVar

T = TypeVar("T")


async def stream_batches(
    fetch_batch_fn: Callable[[int, int], Coroutine[Any, Any, list[T]]],
    batch_size: int = 100,
    max_records: int | float = math.inf,
    initial_offset: int = 0,
) -> AsyncIterator[list[T]]:
    """Yield batches of records using an async paging function."""
    current_offset = initial_offset
    total_yielded = 0

    while total_yielded < max_records:
        limit = int(min(batch_size, max_records - total_yielded))
        batch = await fetch_batch_fn(current_offset, limit)
        if not batch:
            break

        yield batch
        total_yielded += len(batch)
        current_offset += len(batch)

        if len(batch) < limit:
            break


async def stream_records(
    fetch_batch_fn: Callable[[int, int], Coroutine[Any, Any, list[T]]],
    batch_size: int = 100,
    max_records: int | float = math.inf,
    initial_offset: int = 0,
) -> AsyncIterator[T]:
    """Yield records one by one using an async paging function."""
    async for batch in stream_batches(
        fetch_batch_fn=fetch_batch_fn,
        batch_size=batch_size,
        max_records=max_records,
        initial_offset=initial_offset,
    ):
        for item in batch:
            yield item
