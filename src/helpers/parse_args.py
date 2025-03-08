from argparse import ArgumentParser
from src.paper.paper_type import PaperType

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

    group = parser.add_argument_group('frame-extraction-settings', 'Frame extraction settings')
    group.add_argument('-fr', '--output-frame-rate', type=float, default=3.0,
                        help=('Output frame rate for flipbook in fps (default 3.0fps)'))
    group.add_argument('-W', '--width', type=float, default=5,
                        help=('Output flipbook frame width in inches (default 5)'))
    group.add_argument('-H', '--height', type=float, default=3,
                        help=('Output flipbook frame height in inches (default 3'))

    group = parser.add_argument_group('paper-settings', 'Output Print and Paper Settings')
    group.add_argument('-d', '--dpi', type=int, default=300,
                        help='DPI (dots per inch) for printing the flipbook (default 300)')
    # Get the list of options for paper type from the PaperType enum
    paper_types = [e.name.lower() for e in PaperType]
    group.add_argument('-p', '--paper-type', choices=paper_types, default='letter')

    group = parser.add_argument_group('frame-formatting-settings', 'Flipbook frame formatting settings')
    group.add_argument('-bp', '--border-padding', type=int, default=50,
                        help=('Border padding for flipbook frames, applied equally to all sides'
                              ' (default 50)'))
    group.add_argument('-lp', '--left-padding', type=int, default=260,
                        help=('Left border padding for flipbook frames: space for binding'
                              ' (default 260'))
    group.add_argument('-lw', '--border-line-width', type=int, default=3,
                        help=('Width of line for border drawn around frame (default 3)'))

    args = parser.parse_args()
    return args
