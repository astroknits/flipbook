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

    output_width, output_height = get_dimensions(args.output_size)

    # Instantiate flipbook object
    flipbook = Flipbook(
        args.filename,
        args.output_dir,
        output_frame_rate=args.output_frame_rate,
        output_width=output_width,
        output_height=output_height,
        paper_type=args.paper_type
    )

    # Print the info
    flipbook.print_info()

    # Create the flipbook
    flipbook.run()


if __name__ == '__main__':
    main()