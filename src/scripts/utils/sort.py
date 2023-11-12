import logging
import shutil
from functools import wraps
from pathlib import Path
from typing import Optional
from typing import Protocol

logging.basicConfig(level=logging.INFO)


class Stream(Protocol):
    file: Path


def sort(parents=False):
    def _sort(func):
        @wraps(func)
        def decorator(stream: Stream, *args, **kwargs):
            details: Optional[str] = func(stream, *args, **kwargs)

            if details is None:
                return

            partition = Path(f"{stream.file.parent}/{details}")

            partition.mkdir(exist_ok=True, parents=parents)

            shutil.move(stream.file, partition)

            logging.info(" %s moved to %s" % (stream.file.name, partition))

        return decorator

    return _sort
