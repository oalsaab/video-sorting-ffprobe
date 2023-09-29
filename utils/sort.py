import logging
import shutil
from functools import wraps
from pathlib import Path
from typing import Optional
from typing import Protocol

logging.basicConfig(level=logging.INFO)


class Stream(Protocol):
    ...


class StreamMap(Protocol):
    path: Path
    stream: Stream


def sort(parents=False):
    def _sort(func):
        @wraps(func)
        def decorator(mapped: StreamMap, *args, **kwargs):
            details: Optional[str] = func(mapped, *args, **kwargs)

            if details is None:
                return

            partition = Path(f"{mapped.path.parent}/{details}")

            partition.mkdir(exist_ok=True, parents=parents)

            shutil.move(mapped.path, partition)

            logging.info(" %s moved to %s" % (mapped.path.name, partition))

        return decorator

    return _sort
