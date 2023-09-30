import asyncio
import asyncio.subprocess
import json
import os
import shlex
from pathlib import Path
from typing import Iterable
from typing import NamedTuple

from utils.read_stream import Stream

COMMAND = "ffprobe -v quiet -print_format json -show_format -show_streams"


class Map(NamedTuple):
    file: Path
    deserialized: dict


async def _read(file: Path, limit: int) -> Map:
    cmd = shlex.split(COMMAND)
    cmd.append(file)

    async with asyncio.Semaphore(limit):
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE
        )

        stdout, _ = await process.communicate()

        deserialized = json.loads(stdout)

        # Can't pass imported Stream dataclass to async context, event loop closed before import
        return Map(file, deserialized)


async def _stream_collection(files: Iterable[Path]) -> list[Map]:
    limit = os.cpu_count()

    tasks = [asyncio.create_task(_read(file, limit)) for file in files]
    streams = await asyncio.gather(*tasks)

    return streams


def _filter_extensions(directory: Path, extension: tuple) -> Iterable[Path]:
    extensions = [("." + ext) for ext in extension]

    for file in directory.iterdir():
        if file.suffix.lower() in extensions:
            yield file


def create_streams(directory: Path, extension: tuple) -> Iterable[Stream]:
    filtered = _filter_extensions(directory, extension)

    streams = asyncio.run(_stream_collection(filtered))

    for stream in streams:
        yield Stream(stream.deserialized, stream.file)
