from datetime import datetime
from pathlib import Path
from typing import Iterable

import click

from src.create_stream import create_streams
from src.read_stream import Stream
from src.sort_stream import *

directory = click.argument("directory", type=click.Path(exists=True, path_type=Path))
extension = click.argument("extension", nargs=-1)


@click.group()
def cli():
    """Multimedia sorting CLI

    Provide a sort command followed by path to directory
    and extensions of multimedia files to process

    e.g. sorter.py audio 'path/videos' mov mp4

    """


@cli.command("audio")
@directory
@extension
@create_streams
def audio(streams: Iterable[Stream]):
    """Sort by audio"""

    for stream in streams:
        sort_audio(stream)


@cli.command("dimensions")
@directory
@extension
@create_streams
def dimensions(streams: Iterable[Stream]):
    """Sort by dimensions"""

    for stream in streams:
        sort_dimension(stream)


@cli.command("extensions")
@directory
@extension
@create_streams
def extensions(streams: Iterable[Stream]):
    """Sort by extensions"""

    for stream in streams:
        sort_extension(stream)


@cli.command("duration")
@directory
@extension
@create_streams
@click.option("--longer", nargs=1, type=click.FLOAT)
@click.option("--shorter", nargs=1, type=click.FLOAT)
@click.option("--between", nargs=2, type=click.FLOAT)
def duration(
    streams: Iterable[Stream],
    longer: float,
    shorter: float,
    between: tuple[float, float],
):
    """Sort by duration"""

    if not any((longer, shorter, between)):
        raise click.UsageError("PLACEHOLDER")

    for stream in streams:
        if longer:
            sort_duration_long(stream, longer)

        if shorter:
            sort_duration_short(stream, shorter)

        if between:
            sort_duration_between(stream, between)


@cli.command("year")
@directory
@extension
@create_streams
@click.option("--value", nargs=1, type=click.DateTime(formats=["%Y"]), required=True)
def creation_year(streams: Iterable[Stream], value: datetime):
    """Sort by year"""

    for stream in streams:
        sort_year(stream, value.year)


@cli.command("month")
@directory
@extension
@create_streams
@click.option("--value", nargs=1, type=click.DateTime(formats=["%m"]), required=True)
def creation_year(streams: Iterable[Stream], value: datetime):
    """Sort by month"""

    for stream in streams:
        sort_month(stream, value.month)


@cli.command("day")
@directory
@extension
@create_streams
@click.option("--value", nargs=1, type=click.DateTime(formats=["%d"]), required=True)
def creation_day(streams: Iterable[Stream], value: datetime):
    """Sort by day"""

    for stream in streams:
        sort_day(stream, value.day)


@cli.command("date")
@directory
@extension
@create_streams
def creation_full(streams: Iterable[Stream]):
    """Sort by full date"""

    for stream in streams:
        sort_full_date(stream)


@cli.command("specific_date")
@directory
@extension
@create_streams
@click.option(
    "--value", nargs=1, type=click.DateTime(formats=["%Y-%m-%d"]), required=True
)
def creation_specific(streams: Iterable[Stream], value: datetime):
    """Sort by specific date"""

    for stream in streams:
        sort_specific_date(stream, value.date())


@cli.command("size_larger")
@directory
@extension
@create_streams
@click.option("--value", nargs=1, type=click.FLOAT, required=True)
def size_larger(streams: Iterable[Stream], value: float):
    """Sort by size larger than"""

    for stream in streams:
        sort_size_larger(stream, value)


@cli.command("size_smaller")
@directory
@extension
@create_streams
@click.option("--value", nargs=1, type=click.FLOAT, required=True)
def size_smaller(streams: Iterable[Stream], value: float):
    """Sort by size smaller than"""

    for stream in streams:
        sort_size_smaller(stream, value)


@cli.command("size_between")
@directory
@extension
@create_streams
@click.option("--value", nargs=2, type=click.FLOAT, required=True)
def size_between(streams: Iterable[Stream], value: tuple[float, float]):
    """Sort by size between"""

    for stream in streams:
        sort_size_between(stream, value)


if __name__ == "__main__":
    cli()
