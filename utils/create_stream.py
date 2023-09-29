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


class StreamMap(NamedTuple):
    path: Path
    stream: Stream


async def _read(file: Path, limit: int) -> dict:
    cmd = shlex.split(COMMAND)
    cmd.append(file)

    async with asyncio.Semaphore(limit):
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE
        )

        stdout, _ = await process.communicate()

        return json.loads(stdout)


async def _stream_collection(files: Iterable[Path]) -> Iterable[tuple[Path, dict]]:
    limit = os.cpu_count()

    tasks = [asyncio.create_task(_read(file, limit)) for file in files]
    streams = await asyncio.gather(*tasks)

    return zip(files, streams)


def _filter_extensions(directory: Path, extension: tuple) -> Iterable[Path]:
    for file in directory.iterdir():
        if file.suffix.lower() in extension:
            yield file


def create_streams(directory: Path, extension: tuple) -> Iterable[StreamMap]:
    filtered = _filter_extensions(directory, extension)

    streams = asyncio.run(_stream_collection(filtered))

    for path, stream in streams:
        yield StreamMap(path=path, stream=Stream(stream))
