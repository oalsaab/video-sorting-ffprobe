# Video Files Sorting

A command-line interface (CLI) utility program for sorting video files, ffprobe is used to accuratley read the multimedia streams. The output is piped to the python script and used to sort the video files.

The program allows you to sort video files by:

- Audio
- Dimensions
- Extension
- Duration
- Creation date
- Size

Concatenating of video files is made easier when the files are sorted appropriately.

## Installation

Requires python version 3.9+.

To use the program you must have FFmpeg installed and add ffprobe to your enviorment variables.

Download ffprobe: https://www.ffmpeg.org/download.html

Clone the repository: `git clone https://github.com/oalsaab/video-sorting-ffprobe.git`

Install with poetry: `poetry install`

## Usage

To run:

`poetry run sorter [options] [path-to-directory] [video-extension]`

The positional arguments are required and one optional argument is required. <br />
The video-extension positional specify which video file extensions to perform the sorting action on. <br />
You can specify as many video file extensions as required, for example: `mov mp4 webm`

To view the list of available options and their usage run the following command:

`poetry run sorter`
