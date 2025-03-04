from src.padding import EqualPadding, LeftPadding


class FlipbookOutput:
    def __init__(self,
                 output_fps,
                 frame_output_width,
                 frame_output_height,
                 frame_border_padding,
                 frame_left_padding,
                 frame_border_line_width
                 ):

        # output frame rate
        self.frame_rate = output_fps

        # frame width in pixels
        self.frame_output_width = frame_output_width

        # frame height in pixels
        self.frame_output_height = frame_output_height

        # padding around the frame
        self.frame_border_padding = frame_border_padding

        # padding on left side
        self.frame_left_padding = frame_left_padding

        # width of border to draw around the frame
        self.frame_border_line_width = frame_border_line_width

    @property
    def padding(self):
        # Adjust padding to avoid double application of border padding
        adjusted_padding = max(0, self.frame_border_padding - self.frame_border_line_width)

        # Compute frame padding
        return EqualPadding(adjusted_padding) + LeftPadding(self.frame_left_padding)

    @property
    def canvas_width(self) -> int:
        '''
        Returns the drawable canvas width, accounting for padding and border width.
        '''
        horiz_padding = self.padding.left + self.padding.right + 2 * self.frame_border_line_width
        return self.frame_output_width - horiz_padding

    @property
    def canvas_height(self) -> int:
        '''
        Returns the drawable canvas height, accounting for padding and border width.
        '''
        vert_padding = self.padding.top + self.padding.bottom + 2 * self.frame_border_line_width
        return self.frame_output_height - vert_padding

    @property
    def canvas_aspect(self) -> float:
        '''
        Returns the aspect ratio of the canvas area
        '''
        return float(self.canvas_height)/float(self.canvas_width)

    def print_info(self):
        print(f'Flipbook frame size: {self.frame_output_width}x{self.frame_output_height}')
        print(f'frame_border_padding: {self.frame_border_padding}')
        print(f'frame_left_padding: {self.frame_left_padding}')

    '''
        def get_frame_border_padding(self, pad: int) -> Padding:
        ''
        Returns equal padding applied to all sides.
        ''
        return EqualPadding(pad)

    def get_left_frame_padding(self, pad: int) -> Padding:
        ''
        Returns left padding to account for the flipbook binding
        ''
        return LeftPadding(pad)

    def canvas_width(self) -> int:
        ''
        Returns the drawable canvas width, accounting for padding and border width.
        ''
        horiz_padding = self.padding.left + self.padding.right + 2 * self.frame_border_line_width
        return self.output_width - horiz_padding

    def canvas_height(self) -> int:
        ''
        Returns the drawable canvas height, accounting for padding and border width.
        ''
        vert_padding = self.padding.top + self.padding.bottom + 2 * self.frame_border_line_width
        return self.output_height - vert_padding

    def canvas_aspect(self) -> float:
        ''
        Returns the aspect ratio of the canvas area
        ''
        return self.canvas_height()/self.canvas_width()

    '''