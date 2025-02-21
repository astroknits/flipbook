from src.parse_args import parse_args
from src.flipbook import Flipbook

def main():
    # Parse command line arguments
    args = parse_args()

    # Instantiate flipbook object
    flipbook = Flipbook(
        args.filename,
        args.output_dir,
        output_frame_rate=args.output_frame_rate)

    # Print the info
    flipbook.print_info()

    # Create the flipbook
    flipbook.run()


if __name__ == '__main__':
    main()