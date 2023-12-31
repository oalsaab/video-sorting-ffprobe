import asyncio
import asyncio.subprocess
import json
import os
import shlex
from asyncio import Semaphore
from functools import wraps
from pathlib import Path
from typing import Iterable
from typing import NamedTuple

from .read_stream import Stream

COMMAND = "ffprobe -v quiet -print_format json -show_format -show_streams"


class Processed(NamedTuple):
    file: Path
    deserialized: dict


async def _process(file: Path, semaphore: Semaphore) -> Processed:
    cmd = shlex.split(COMMAND)
    cmd.append(file)

    async with semaphore:
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE
        )

        stdout, _ = await process.communicate()

        deserialized = json.loads(stdout)

        # Can't pass imported Stream dataclass to async context, event loop closed before import
        return Processed(file, deserialized)


async def _stream_collection(files: Iterable[Path]) -> list[Processed]:
    limit = os.cpu_count()
    semaphore = asyncio.Semaphore(limit)

    tasks = [asyncio.create_task(_process(file, semaphore)) for file in files]
    processed = await asyncio.gather(*tasks)

    return processed


def _filter_files(directory: Path, extension: tuple) -> Iterable[Path]:
    extensions = [("." + ext) for ext in extension]

    for file in directory.iterdir():
        if file.suffix.lower() in extensions:
            yield file


def _iter_streams(processed: list[Processed]) -> Iterable[Stream]:
    for process in processed:
        yield Stream(process.deserialized, process.file)


def create_streams(func):
    @wraps(func)
    def decorator(directory: Path, extension: tuple, *args, **kwargs):
        filtered = _filter_files(directory, extension)

        processed = asyncio.run(_stream_collection(filtered))

        streams = _iter_streams(processed)

        func(streams, *args, **kwargs)

    return decorator
