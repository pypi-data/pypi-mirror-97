#!/usr/bin/env python

# pylint: disable=protected-access,redefined-outer-name

"""AIOTempFile tests."""

import logging

from asyncio import coroutine
from pathlib import Path
from typing import Any

import pytest

from aiofiles.base import AiofilesContextManager
from aiofiles.threadpool.binary import AsyncBufferedReader
from aiotempfile.aiotempfile import open as aiotempfile

pytestmark = [pytest.mark.asyncio]

LOGGER = logging.getLogger(__name__)


def assert_closed_and_clean(file, path: Path):
    """Closes a given file, ensures it's deleted."""
    assert file is None or file.closed
    assert not path.exists()


async def read_file(file) -> bytes:
    """Reads a given file."""
    await file.seek(0)
    return await file.read()


async def write_to_file(file: Any, content: bytes) -> Path:
    """Consolidated file write tests."""
    assert isinstance(file, AsyncBufferedReader)
    path = Path(file.name)
    assert path
    await file.write(content)
    assert await file.tell() > 0
    return path


async def test_open_async_with():
    """Test that temporary files can be opened."""
    content_expected = b"This is test content."

    _file = None
    path = None
    async with aiotempfile() as file:
        _file = file
        path = await write_to_file(file, content_expected)
        assert await read_file(file) == content_expected
    assert_closed_and_clean(_file, path)


async def test_open_await():
    """Test that temporary files can be opened."""
    content_expected = b"This is test content."

    file = await aiotempfile()
    path = await write_to_file(file, content_expected)
    assert await read_file(file) == content_expected
    file.close()
    assert_closed_and_clean(file, path)


async def test_open_context_manager__aenter__():
    """Test that temporary files can be opened."""
    content_expected = b"This is test content."

    aiofiles_context_manager = aiotempfile()
    assert isinstance(aiofiles_context_manager, AiofilesContextManager)
    file = await aiofiles_context_manager.__aenter__()

    path = await write_to_file(file, content_expected)
    assert await read_file(file) == content_expected

    await aiofiles_context_manager.__aexit__(None, None, None)
    aiofiles_context_manager.close()
    assert_closed_and_clean(file, path)


async def test_open_context_manager__anext__():
    """Test that temporary files can be opened."""
    content_expected = b"This is test content."

    aiofiles_context_manager = aiotempfile()
    assert isinstance(aiofiles_context_manager, AiofilesContextManager)

    file = await aiofiles_context_manager.__anext__()
    path = await write_to_file(file, content_expected)
    assert await read_file(file) == content_expected
    await file.close()

    aiofiles_context_manager.close()
    assert_closed_and_clean(file, path)


@pytest.mark.filterwarnings('ignore:.*use "async def" instead:DeprecationWarning')
def test_open_context_manager__await__():
    # pylint: disable=not-an-iterable
    """Test that temporary files can be opened."""
    content_expected = b"This is test content."

    aiofiles_context_manager = aiotempfile()
    assert isinstance(aiofiles_context_manager, AiofilesContextManager)

    # https://stackoverflow.com/a/56114311/1201075
    @coroutine
    def do_test() -> Path:
        file = yield from aiofiles_context_manager.__await__()
        path = yield from write_to_file(file, content_expected)
        content_acutal = yield from read_file(file)
        file.close()
        assert content_acutal == content_expected
        return path

    path = yield from do_test()

    aiofiles_context_manager.close()
    assert_closed_and_clean(aiofiles_context_manager._obj, path)


async def test_open_context_manager__iter__():
    """Test that temporary files can be opened."""
    content_expected = b"This is test content."

    aiofiles_context_manager = aiotempfile()
    assert isinstance(aiofiles_context_manager, AiofilesContextManager)

    file = await aiofiles_context_manager.__iter__()
    path = await write_to_file(file, content_expected)
    assert await read_file(file) == content_expected
    file.close()

    aiofiles_context_manager.close()
    assert_closed_and_clean(file, path)


async def test_open_context_manager_await():
    """Test that temporary files can be opened."""
    content_expected = b"This is test content."

    aiofiles_context_manager = aiotempfile()
    assert isinstance(aiofiles_context_manager, AiofilesContextManager)

    file = await aiofiles_context_manager
    path = await write_to_file(file, content_expected)
    assert await read_file(file) == content_expected
    file.close()

    aiofiles_context_manager.close()
    assert_closed_and_clean(file, path)
