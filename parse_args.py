from argparse import ArgumentParser

def parse_args():
    '''
    Parse command line arguments using argparse
    '''
    parser = ArgumentParser()
    parser.add_argument('filename', help='Path of the video file to use')
    parser.add_argument('output_dir', help='Directory to write output')
    parser.add_argument('output_base_name', nargs='?', default=None,
                        help=('Base name for output PDF files '
                              '(default None -> use stem of the input video file)'))
    parser.add_argument('-fr', '--output-frame-rate', type=float, default=3.0,
                        help=('Output frame rate for flipbook in fps (default 3.0fps)'))
    args = parser.parse_args()
    return args
