import sys
from pathlib import Path

from src.core.video_source import VideoSource
from src.core.flipbook_output import FlipbookOutput
from src.helpers.flipbook_helper import FlipbookHelper
from src.helpers.parse_args import parse_args
from src.core.flipbook import Flipbook


def main():
    # Parse command line arguments
    args = parse_args()

    try:
        FlipbookHelper.validate_output_dir(Path(args.output_dir))
    except (FileExistsError, IsADirectoryError) as e:
        print(f'\n\nError:{e}\n\n')
        print(f'Exiting because the directory {args.output_dir} is invalid.\n\n')
        sys.exit(1)

    # instantiate Input object with input video path and metadata
    flipbook_input = VideoSource(args.filename)

    # instantiate Output object with output frame parameters
    flipbook_output = FlipbookOutput(
        args.output_frame_rate,
        args.width,
        args.height,
        args.border_padding,
        args.left_padding,
        args.border_line_width,
        args.dpi
    )

    # Instantiate flipbook object
    flipbook = Flipbook(flipbook_input, flipbook_output)

    # Run the flipbook to extract the frames
    flipbook.extract_frames()

    # Save the frames to disk
    flipbook.save(args.paper_type, args.dpi, args.output_dir)

if __name__ == '__main__':
    main()