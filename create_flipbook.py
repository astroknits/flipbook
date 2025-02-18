from PIL import Image
import PyPDF2
from parse_args import parse_args
from flipbook import Flipbook



def main():
    # Parse command line arguments
    args = parse_args()

    # Get the vide file name from the command line arguments
    filename = args.filename

    # Get output directory from command line args
    output_dir = args.output_dir

    # Get base name for output PDF files
    output_base_name = args.output_base_name

    # Output frame rate
    output_frame_rate = args.output_frame_rate

    flipbook = Flipbook(filename, output_dir, output_base_name=output_base_name, output_frame_rate=output_frame_rate)
    flipbook.print_info()

    flipbook.run()


if __name__ == '__main__':
    main()