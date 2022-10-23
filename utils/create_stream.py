import asyncio
import asyncio.subprocess
import shlex
import os


async def read(file):
    cmd = shlex.split("ffprobe -v quiet -print_format json -show_format -show_streams")
    cmd.append(file)
    limit = os.cpu_count()

    async with asyncio.Semaphore(limit):
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        return stdout


async def stream_collection(files):
    tasks = [asyncio.create_task(read(file)) for file in files]
    streams = await asyncio.gather(*tasks)
    return dict(zip(files, streams))
