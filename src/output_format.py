
class OutputFormat:
    '''
    Settings for the layout of the output images
    intended to be printed.

    Note there is a lot here that is still pretty rough/ad hoc
    and is intended to be be streamlined/automated in the future

    e.g. right now we specify the number of rows and/or columns
    per sheet, but eventually we would like to specify an output
    flipbook dimension and work backwards to calculate how many frames
    will fit per page,
    '''
    def __init__(self, nrows, ncols, frame_rate, paper_format, frame_border_padding=50, left_binding_padding=260):
        # Number of rows and columns to arrange flipbook frames in a page
        self.nrows = nrows
        self.ncols = ncols

        # Output frame rate for downsampling the video
        self.frame_rate = frame_rate

        # Select output paper format for printing
        self.paper_format = paper_format

        # How many pixels border padding to add around each frame (default 50)
        # TODO calculate automatically based on more meaningful params
        self.frame_border_padding = frame_border_padding

        # How many additional pixels to pad on the left hand side of the frame
        # (for the binding)
        # TODO calculate automatically based on more meaningful params
        self.left_binding_padding = left_binding_padding

    def print(self):
        print(f'ncols: {self.ncols}')
        print(f'nrows: {self.nrows}')
        print(f'Frame rate: {self.frame_rate:.2f} fps')
        print(f'Page format: {self.paper_format.value.name}')
        print(f'Page aspect ratio: {self.paper_format.value.aspect:.2f}')
        print(f'Frame border padding: {self.frame_border_padding}')
        print(f'Left binding padding: {self.left_binding_padding}')
