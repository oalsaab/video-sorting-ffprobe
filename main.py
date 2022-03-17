import argparse
from pathlib import Path
from arguments import arguments
from sort_class import VideoSorting


def main():
    """Create command-line interface and call Video_sorting to process and sort the files."""
    
    parser = argparse.ArgumentParser('Video sorting command line utility program')
    arguments(parser) 
    args = parser.parse_args()

    path = Path(args.folderPath)
    files = path.iterdir()
    videos = ['.' + i for i in args.videoExtension]

    for file in files:
        if file.suffix.lower() in videos:
            try:
                process = VideoSorting(file, args, path)

                if args.audio: 
                    process.audio_sort()
                    
                elif args.dimensions:
                    process.dimensions_sort()
                
                elif args.extension:
                    process.extension()
                    
                elif (
                    args.size_larger or
                    args.size_smaller or
                    args.size_between
                ): 
                    process.size_sort()
                
                elif (
                    args.duration_long or
                    args.duration_short or
                    args.duration_between
                ):
                    process.duration_sort()
                    
                elif (
                    args.creation_year or
                    args.creation_month or
                    args.creation_day or
                    args.creation_specific or
                    args.creation_full
                ):
                    process.creation_sort()
                
                else:
                    parser.error('Choose a action to perform')
            except KeyError:
                print(file.name, 'corrupted or does not contain multimedia streams')
                

if __name__ == '__main__':
    print('Sorting video files...')
    main()
    print('Completed sorting video files')

        


