import asyncio
import mock

def run(async_method):
    return asyncio.get_event_loop().run_until_complete(async_method)

def mock_async_method(*args, **kwargs):
    m = mock.MagicMock(*args, **kwargs)

    async def mock_method(*args, **kwargs):
        return m(*args, **kwargs)

    mock_method.mock = m
    return mock_method
