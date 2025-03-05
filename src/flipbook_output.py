from src.padding import EqualPadding, LeftPadding
from src.size import Size


class FlipbookOutput:
    def __init__(self,
                 output_fps,
                 width,
                 height,
                 border_padding,
                 left_padding,
                 border_line_width
                 ):

        # output frame rate
        self.frame_rate = output_fps

        # frame width in pixels
        self.width = width

        # frame height in pixels
        self.height = height

        # padding around the frame
        self.border_padding = border_padding

        # padding on left side
        self.left_padding = left_padding

        # width of border to draw around the frame
        self.border_line_width = border_line_width

    @property
    def padding(self):
        # Adjust padding to avoid double application of border padding
        adjusted_padding = max(0, self.border_padding - self.border_line_width)

        # Compute frame padding
        return EqualPadding(adjusted_padding) + LeftPadding(self.left_padding)

    @property
    def canvas_size(self) -> int:
        '''
        Returns the drawable canvas width, accounting for padding and border width.
        '''
        horiz_padding = self.padding.left + self.padding.right + 2 * self.border_line_width
        width = self.width - horiz_padding
        vert_padding = self.padding.top + self.padding.bottom + 2 * self.border_line_width
        height = self.height - vert_padding
        return Size(width, height)

    def print_info(self):
        print(f'Flipbook frame size: {self.width}x{self.height}')
        print(f'frame_border_padding: {self.border_padding}')
        print(f'frame_left_padding: {self.left_padding}')

