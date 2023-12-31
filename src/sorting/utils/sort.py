import logging
import shutil
from collections.abc import Iterator
from functools import wraps
from pathlib import Path
from typing import Protocol

logging.basicConfig(level=logging.INFO)


class Stream(Protocol):
    file: Path


class Result(Protocol):
    stream: Stream
    partition: str


def sort(parents=False):
    def _sort(func):
        @wraps(func)
        def decorator(streams: Iterator[Stream], *args, **kwargs):
            results: Iterator[Result] = func(streams, *args, **kwargs)

            for result in results:
                path = Path(f"{result.stream.file.parent}/{result.partition}")

                path.mkdir(exist_ok=True, parents=parents)

                shutil.move(result.stream.file, path)

                logging.info(" %s --> %s" % (result.stream.file.name, path))

        return decorator

    return _sort
