from collections.abc import AsyncIterator

import httpx2
import pytest

from openai import OpenAI, AsyncOpenAI
from openai._streaming import Stream, AsyncStream


async def _aiter(chunks: list[bytes]) -> AsyncIterator[bytes]:
    for chunk in chunks:
        yield chunk


@pytest.mark.parametrize("sync", [True, False])
async def test_control_only_events_are_skipped(sync: bool, client: OpenAI, async_client: AsyncOpenAI) -> None:
    chunks = [b"retry: 1000\n\n", b"id: stream-1\n\n", b"data: {}\n\n"]

    if sync:
        response = httpx2.Response(200, content=iter(chunks))
        stream = Stream(cast_to=object, client=client, response=response)
        assert list(stream) == [{}]
    else:
        response = httpx2.Response(200, content=_aiter(chunks))
        stream = AsyncStream(cast_to=object, client=async_client, response=response)
        assert [item async for item in stream] == [{}]
