from dataclasses import dataclass
from datetime import date
from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import NamedTuple

from .enums import Model


class Dimensions(NamedTuple):
    width: str
    height: str


@dataclass
class Stream:
    stream: dict
    file: Path

    @cached_property
    def streams(self) -> list[dict]:
        return self.stream.get(Model.STREAMS, [{}])

    @property
    def audio(self) -> bool:
        _codecs = (streams.get(Model.CODEC_TYPE) for streams in self.streams)

        return Model.AUDIO.value in _codecs

    @property
    def dimension(self) -> Dimensions:
        for item in self.streams:
            width, height = item.get(Model.WIDTH), item.get(Model.HEIGHT)

            if all(_ is not None for _ in (width, height)):
                return Dimensions(width, height)

    @property
    def duration(self) -> str:
        return self.stream.get(Model.FORMAT, {}).get(Model.DURATION)

    @property
    def creation(self) -> date:
        _tags: dict = next(iter(self.streams), {}).get(Model.TAGS, {})
        _creation_time = _tags.get(Model.CREATION_TIME)

        if _creation_time is None:
            return None

        return datetime.strptime(_creation_time, "%Y-%m-%dT%H:%M:%S.%fZ").date()

    @property
    def size(self) -> int:
        _size = self.file.stat().st_size
        return _size / (1024 * 1024)

    @property
    def extension(self) -> str:
        _, extension = self.file.suffix.split(".")

        return extension
