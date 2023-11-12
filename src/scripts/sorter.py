from datetime import datetime
from pathlib import Path
from typing import Iterable

import click

from ..create_stream import create_streams
from ..enums import Argument
from ..enums import Command
from ..enums import Option
from ..read_stream import Stream
from ..sort_stream import *

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

    if not any((longer, shorter, between)):
        raise click.UsageError(
            f"Duration command requires at least one of following options: {Option.duration()}"
        )

    for stream in streams:
        if longer:
            sort_duration_long(stream, longer)

        if shorter:
            sort_duration_short(stream, shorter)

        if between:
            sort_duration_between(stream, between)


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

    for stream in streams:
        if year:
            sort_year(stream, year.year)

        elif month:
            sort_month(stream, month.month)

        elif day:
            sort_day(stream, day.day)

        elif specific:
            sort_specific_date(stream, specific.date())

        else:
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

    if not any((larger, smaller, between)):
        raise click.UsageError(
            f"Size command requires at least one of following options: {Option.size()}"
        )

    for stream in streams:
        if larger:
            sort_size_larger(stream, larger)

        if smaller:
            sort_size_smaller(stream, smaller)

        if between:
            sort_size_between(stream, between)


if __name__ == "__main__":
    cli()