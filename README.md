# Video Files Sorting

A command-line interface (CLI) utility program for sorting video files using ffprobe and Pathlib stat object.
The program employs ffprobe to accurately read multimedia streams. The output is piped to the python script and used to sort the video files.

The program allows you to sort video files by:
* Audio
* Dimensions
* Extension
* Duration
* Creation date
* Size

Concatenating video files is made easier if the files are sorted appropriately. 

## Installation

To use the program you must have FFmpeg installed and add ffprobe to your enviorment variables.

Download ffprobe: https://www.ffmpeg.org/download.html

Clone the repository: ``` git clone https://github.com/oalsaab/video-sorting-ffprobe.git ```

## Usage

In the CLI run:

``` main.py [options] [path-to-directory] [video-extension] ```

The positional arguments are required and one optional argument is required. <br />
The video-extension positional specifiy which video file extensions to perform the action on. <br />
The user can specifiy as many video file extensions as required, for example: ``` mov mp4 webm ```

To view the list of availaible options and their usage run the following command:

``` main.py -h ``` or ``` main.py --help```

The output of running the help command:

```
usage: main.py [-h] [-a] [-d] [-e] [-dl DURATION_LONG] [-ds DURATION_SHORT] [-db DURATION_BETWEEN DURATION_BETWEEN]
               [-cy CREATION_YEAR] [-cm [1-12]] [-cd [1-31]] [-cs [YYYY-MM-DD]] [-cf] [-sl SIZE_LARGER]
               [-ss SIZE_SMALLER] [-sb SIZE_BETWEEN SIZE_BETWEEN]
               folderPath videoExtension [videoExtension ...]

positional arguments:
  folderPath            path to folder with video files
  videoExtension        extension of videos to sort

optional arguments:
  -h, --help            show this help message and exit
  -a, --audio           sort videos by audio
  -d, --dimensions      sort videos by dimensions
  -e, --extension       sort videos by extension

duration:
  duration in seconds

  -dl DURATION_LONG, --duration_long DURATION_LONG
                        sort videos by duration longer than argument
  -ds DURATION_SHORT, --duration_short DURATION_SHORT
                        sort videos by duration shorter than argument
  -db DURATION_BETWEEN DURATION_BETWEEN, --duration_between DURATION_BETWEEN DURATION_BETWEEN
                        sort videos by duration between arguments

creation time:
  European date format

  -cy CREATION_YEAR, --creation_year CREATION_YEAR
                        sort videos by year
  -cm [1-12], --creation_month [1-12]
                        sort videos by month
  -cd [1-31], --creation_day [1-31]
                        sort videos by day
  -cs [YYYY-MM-DD], --creation_specific [YYYY-MM-DD]
                        sort videos by specific date
  -cf, --creation_full  sort videos by full date

size:
  Size in Megabytes

  -sl SIZE_LARGER, --size_larger SIZE_LARGER
                        sort videos by size larger than argument
  -ss SIZE_SMALLER, --size_smaller SIZE_SMALLER
                        sort videos by size smaller than argument
  -sb SIZE_BETWEEN SIZE_BETWEEN, --size_between SIZE_BETWEEN SIZE_BETWEEN
                        sort videos by size between arguments
                        
```
