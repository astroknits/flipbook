from src.paper_type import PaperType
from src.parse_args import parse_args
from src.flipbook import Flipbook

def get_dimensions(arg):
    if 'x' not in arg:
        raise ValueError(f'--os must be in form $NUMx$NUM.  Entered {arg}')
    dims = arg.split('x')
    if len(dims) != 2:
        raise ValueError(f'--os must be in form $NUMx$NUM.  Entered {arg}')
    return [float(dim) for dim in dims]

def main():
    # Parse command line arguments
    args = parse_args()

    output_width = int(args.width * args.dpi)
    output_height = int(args.height * args.dpi)

    # Instantiate flipbook object
    flipbook = Flipbook(
        args.filename,
        args.output_frame_rate,
        output_width,
        output_height,
    )

    # Run the flipbook to extract the frames
    flipbook.extract_frames()

    # Save the frames to disk
    flipbook.save(args.paper_type, args.dpi, args.output_dir)

if __name__ == '__main__':
    main()