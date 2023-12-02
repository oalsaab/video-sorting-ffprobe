import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable

import click

from .utils.create_stream import create_streams
from .utils.enums import Argument
from .utils.enums import Command
from .utils.enums import Option
from .utils.read_stream import Stream
from .utils.sort_stream import *


class Args:
    def __init__(self):
        self._args = {idx: arg for idx, arg in enumerate(sys.argv)}

    @property
    def option(self) -> Optional[str]:
        return self._args.get(2)

    def err_msg(self, command: str, options: list[str]) -> str:
        return f"{command} command requires at least one of the following options: {options}"


directory = click.argument(
    Argument.DIRECTORY, type=click.Path(exists=True, path_type=Path)
)
extension = click.argument(Argument.EXTENSION, nargs=-1)


@click.group()
def cli():
    """Multimedia sorting CLI

    Provide a sort command followed by path to directory
    and extensions of multimedia files to process

    e.g. sorter.py audio 'path/videos' mov mp4

    """


@cli.command(Command.AUDIO)
@directory
@extension
@create_streams
def audio(streams: Iterable[Stream]):
    """Sort by audio"""

    for stream in streams:
        sort_audio(stream)


@cli.command(Command.DIMENSIONS)
@directory
@extension
@create_streams
def dimensions(streams: Iterable[Stream]):
    """Sort by dimensions"""

    for stream in streams:
        sort_dimension(stream)


@cli.command(Command.EXTENSIONS)
@directory
@extension
@create_streams
def extensions(streams: Iterable[Stream]):
    """Sort by extensions"""

    for stream in streams:
        sort_extension(stream)


@cli.command(Command.DURATION)
@directory
@extension
@create_streams
@click.option(Option.LONGER, nargs=1, type=click.FLOAT)
@click.option(Option.SHORTER, nargs=1, type=click.FLOAT)
@click.option(Option.BETWEEN, nargs=2, type=click.FLOAT)
def duration(
    streams: Iterable[Stream],
    longer: float,
    shorter: float,
    between: tuple[float, float],
):
    """Sort by duration"""

    args = Args()

    for stream in streams:
        match args.option:
            case Option.LONGER:
                sort_duration_long(stream, longer)

            case Option.SHORTER:
                sort_duration_short(stream, shorter)

            case Option.BETWEEN:
                sort_duration_between(stream, between)

            case _:
                message = args.err_msg("Duration", Option.duration())
                raise click.UsageError(message)


@cli.command(Command.DATE)
@directory
@extension
@create_streams
@click.option(Option.YEAR, nargs=1, type=click.DateTime(formats=["%Y"]))
@click.option(Option.MONTH, nargs=1, type=click.DateTime(formats=["%m"]))
@click.option(Option.DAY, nargs=1, type=click.DateTime(formats=["%d"]))
@click.option(Option.SPECIFIC, nargs=1, type=click.DateTime(formats=["%Y-%m-%d"]))
def creation(
    streams: Iterable[Stream],
    year: datetime,
    month: datetime,
    day: datetime,
    specific: datetime,
):
    """Sort by date"""

    args = Args()

    for stream in streams:
        match args.option:
            case Option.YEAR:
                sort_year(stream, year.year)

            case Option.MONTH:
                sort_month(stream, month.month)

            case Option.DAY:
                sort_day(stream, day.day)

            case Option.SPECIFIC:
                sort_specific_date(stream, specific.date())

            case _:
                sort_full_date(stream)


@cli.command(Command.SIZE)
@directory
@extension
@create_streams
@click.option(Option.LARGER, nargs=1, type=click.FLOAT)
@click.option(Option.SMALLER, nargs=1, type=click.FLOAT)
@click.option(Option.BETWEEN, nargs=2, type=click.FLOAT)
def size_larger(
    streams: Iterable[Stream],
    larger: float,
    smaller: float,
    between: tuple[float, float],
):
    """Sort by size"""

    args = Args()

    for stream in streams:
        match args.option:
            case Option.LARGER:
                sort_size_larger(stream, larger)

            case Option.SMALLER:
                sort_size_smaller(stream, smaller)

            case Option.BETWEEN:
                sort_size_between(stream, between)

            case _:
                message = args.err_msg("Size", Option.size())
                raise click.UsageError(message)
