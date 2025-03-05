from src.size import Size
from src.video_source import VideoSource
from src.flipbook_output import FlipbookOutput
from src.parse_args import parse_args
from src.flipbook import Flipbook

def main():
    # Parse command line arguments
    args = parse_args()

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