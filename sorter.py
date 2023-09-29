from pathlib import Path

import click

from utils.create_stream import create_streams
from utils.sort_stream import sort_audio
from utils.sort_stream import sort_dimension
from utils.sort_stream import sort_duration_between
from utils.sort_stream import sort_duration_long
from utils.sort_stream import sort_duration_short
from utils.sort_stream import sort_extension

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
def audio(directory: Path, extension: tuple):
    """Sort by audio"""

    streams = create_streams(directory, extension)

    for stream in streams:
        sort_audio(stream)


@cli.command("dimensions")
@directory
@extension
def dimensions(directory: Path, extension: tuple):
    """Sort by dimensions"""

    streams = create_streams(directory, extension)

    for stream in streams:
        sort_dimension(stream)


@cli.command("extensions")
@directory
@extension
def extensions(directory: Path, extension: tuple):
    """Sort by extensions"""

    streams = create_streams(directory, extension)

    for stream in streams:
        sort_extension(stream)


@cli.command("duration_longer")
@directory
@extension
@click.option("--value", nargs=1, type=click.FLOAT, required=True)
def duration_longer(directory: Path, extension: tuple, value: float):
    """Sort by duration longer than"""

    streams = create_streams(directory, extension)

    for stream in streams:
        sort_duration_long(stream, value)


@cli.command("duration_shorter")
@directory
@extension
@click.option("--value", nargs=1, type=click.FLOAT, required=True)
def duration_shorter(directory: Path, extension: tuple, value: float):
    """Sort by duration shorter than"""

    streams = create_streams(directory, extension)

    for stream in streams:
        sort_duration_short(stream, value)


@cli.command("duration_between")
@directory
@extension
@click.option("--value", nargs=2, type=click.FLOAT, required=True)
def duration_between(directory: Path, extension: tuple, value: tuple[float, float]):
    """Sort by duration between"""

    streams = create_streams(directory, extension)

    for stream in streams:
        sort_duration_between(stream, value)


@cli.command("year")
@directory
@extension
def creation_year(directory: Path, extension: tuple):
    """Sort by year"""

    return directory


@cli.command("month")
@directory
@extension
def creation_year(directory: Path, extension: tuple):
    """Sort by month"""

    return directory


@cli.command("day")
@directory
@extension
def creation_day(directory: Path, extension: tuple):
    """Sort by day"""

    return directory


@cli.command("date")
@directory
@extension
def creation_date(directory: Path, extension: tuple):
    """Sort by full date"""

    return directory


@cli.command("specfic_date")
@directory
@extension
def creation_specific(directory: Path, extension: tuple):
    """Sort by specfic date"""

    return directory


@cli.command("size_larger")
@directory
@extension
def size_larger(directory: Path, extension: tuple):
    """Sort by size larger than"""

    return directory


@cli.command("size_smaller")
@directory
@extension
def size_smaller(directory: Path, extension: tuple):
    """Sort by size smaller than"""

    return directory


@cli.command("size_between")
@directory
@extension
def size_between(directory: Path, extension: tuple):
    """Sort by size between"""

    return directory


if __name__ == "__main__":
    cli()
