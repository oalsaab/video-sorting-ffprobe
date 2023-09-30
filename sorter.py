from datetime import datetime
from pathlib import Path
from typing import Iterable

import click

from src.create_stream import create_streams
from src.read_stream import Stream
from src.sort_stream import sort_audio
from src.sort_stream import sort_day
from src.sort_stream import sort_dimension
from src.sort_stream import sort_duration_between
from src.sort_stream import sort_duration_long
from src.sort_stream import sort_duration_short
from src.sort_stream import sort_extension
from src.sort_stream import sort_full_date
from src.sort_stream import sort_month
from src.sort_stream import sort_size_between
from src.sort_stream import sort_size_larger
from src.sort_stream import sort_size_smaller
from src.sort_stream import sort_specific_date
from src.sort_stream import sort_year

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


@cli.command("duration_longer")
@directory
@extension
@create_streams
@click.option("--value", nargs=1, type=click.FLOAT, required=True)
def duration_longer(streams: Iterable[Stream], value: float):
    """Sort by duration longer than"""

    for stream in streams:
        sort_duration_long(stream, value)


@cli.command("duration_shorter")
@directory
@extension
@create_streams
@click.option("--value", nargs=1, type=click.FLOAT, required=True)
def duration_shorter(streams: Iterable[Stream], value: float):
    """Sort by duration shorter than"""

    for stream in streams:
        sort_duration_short(stream, value)


@cli.command("duration_between")
@directory
@extension
@create_streams
@click.option("--value", nargs=2, type=click.FLOAT, required=True)
def duration_between(streams: Iterable[Stream], value: tuple[float, float]):
    """Sort by duration between"""

    for stream in streams:
        sort_duration_between(stream, value)


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
