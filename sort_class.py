import subprocess
import json
import shlex

import shutil
from pathlib import Path


class VideoSorting():
    """Spawns a new process of ffprobe or stat object on every file in the user-supplied directory. 
    Connects to the output pipes and captures the output for video file sorting."""
    
    def __init__(self, file, args, path):
        
        cmd = 'ffprobe -v quiet -print_format json -show_format -show_streams'
        args_ffprobe = shlex.split(cmd)
        self.file = file
        args_ffprobe.append(self.file)

        process = subprocess.run(args_ffprobe, capture_output=True)
        self.video_json = json.loads(process.stdout)

        self.args = args
        self.path = path
    
    def sort(self, folder, parents=False):

        Path(f'{self.args.folderPath}/{folder}').mkdir(parents=parents, exist_ok=True)
        shutil.move(self.file, f'{self.path}/{folder}')
        
        print(f'{self.file.name} moved to {folder}')

    def audio_sort(self):

        codecs = [stream['codec_type'] for stream in self.video_json['streams']]

        if 'audio' in codecs:
            self.sort('audio')
        else:
            self.sort('no_audio')
        
    def dimensions_sort(self):

        try:
            width = self.video_json['streams'][0]['width']
            height = self.video_json['streams'][0]['height']
        except KeyError:
            width = self.video_json['streams'][1]['width']
            height = self.video_json['streams'][1]['height']
        
        self.sort(f'{width}x{height}')
    
    def duration_sort(self):

        duration = self.video_json['format']['duration']
        
        if self.args.duration_long:
            if float(duration) > self.args.duration_long:
                self.sort(f'longer_than_{self.args.duration_long}')
        
        if self.args.duration_short:
            if self.args.duration_short > float(duration):
                self.sort(f'shorter_than_{self.args.duration_short}')
        
        if self.args.duration_between:
            if self.args.duration_between[0] < float(duration) < self.args.duration_between[1]:
                self.sort(f'between_{self.args.duration_between[0]}-{self.args.duration_between[1]}')

    def creation_sort(self):
        
        try:
            creation_time_utc = self.video_json['streams'][0]['tags']['creation_time']
        except KeyError:
            return print(f'no creation time tag found for {self.file.name}')
        
        creation_time_str = creation_time_utc[:10]
        creation_time = creation_time_str.split('-')

        year, month, day = creation_time

        if self.args.creation_year:
            if self.args.creation_year == int(year):
                self.sort(f'year-{self.args.creation_year}')

        if self.args.creation_month:
            if self.args.creation_month == int(month):
                self.sort(f'month-{self.args.creation_month}')

        if self.args.creation_day:
            if self.args.creation_day == int(day):
                self.sort(f'day-{self.args.creation_day}') 
            
        if self.args.creation_specific:
            if self.args.creation_specific == creation_time_str:
                self.sort(self.args.creation_specific)
            
        if self.args.creation_full:
            self.sort(f'{year}/{year}-{month}/{year}-{month}-{day}', True)

    def size_sort(self):
    
        size = Path(self.file).stat().st_size
        size_mb = size / (1024 * 1024)
        
        if self.args.size_larger:
            if float(size_mb) > self.args.size_larger:
                self.sort(f'size_larger_than_{self.args.size_larger}')

        if self.args.size_smaller:
            if self.args.size_smaller > float(size_mb):
                self.sort(f'size_smaller_than_{self.args.size_smaller}')
        
        if self.args.size_between:
            if self.args.size_between[0] < float(size_mb) < self.args.size_between[1]:
                self.sort(f'size_between_{self.args.size_between[0]}-{self.args.size_between[1]}')

    def extension(self):
        
        extension = Path(self.file).suffix
        extension_split = extension.split('.')
        extension_index = extension_split[1]
        self.sort(f'{extension_index}')

        
        
        
    
