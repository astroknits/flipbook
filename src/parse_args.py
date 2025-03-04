from argparse import ArgumentParser
from src.paper_type import PaperType

def parse_args():
    '''
    Parse command line arguments using argparse
    '''
    parser = ArgumentParser(
        description=('Create a flipbook from a video file by extracting frames and arranging them'
                     ' on specific paper type for printing'))
    parser.add_argument('filename', help='Path of the video file to use')
    parser.add_argument('output_dir', help='Directory to write output')
    parser.add_argument('output_base_name', nargs='?', default=None,
                        help=('Base name for output PDF files '
                              '(default None -> use stem of the input video file)'))
    parser.add_argument('-fr', '--output-frame-rate', type=float, default=3.0,
                        help=('Output frame rate for flipbook in fps (default 3.0fps)'))
    parser.add_argument('-W', '--width', type=float, default=5,
                        help=('Output flipbook frame width in inches (default 5)'))
    parser.add_argument('-H', '--height', type=float, default=3,
                        help=('Output flipbook frame height in inches (default 3'))
    parser.add_argument('-d', '--dpi', type=int, default=300,
                        help='DPI (dots per inch) for printing the flipbook (default 300)')
    # Get the list of options for paper type from the PaperType enum
    paper_types = [e.name.lower() for e in PaperType]
    parser.add_argument('-p', '--paper-type', choices=paper_types, default='letter')
    args = parser.parse_args()
    return args
