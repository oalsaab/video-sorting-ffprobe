import asyncio
import asyncio.subprocess
import json
import os
import shlex
from pathlib import Path

COMMAND = "ffprobe -v quiet -print_format json -show_format -show_streams"


async def _read(file: Path, limit: int) -> dict:
    cmd = shlex.split(COMMAND)
    cmd.append(file)

    async with asyncio.Semaphore(limit):
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE
        )

        stdout, _ = await process.communicate()

        return json.loads(stdout)


async def stream_collection(files: list[Path]) -> dict[Path, dict]:
    limit = os.cpu_count()

    tasks = [asyncio.create_task(_read(file, limit)) for file in files]
    streams = await asyncio.gather(*tasks)

    return dict(zip(files, streams))
