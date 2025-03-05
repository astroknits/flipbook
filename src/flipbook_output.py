from src.padding import EqualPadding, LeftPadding, Padding
from src.resolution import Resolution
from src.size import Size


class FlipbookOutput:
    def __init__(self,
                 output_fps: float,
                 width: float,
                 height: float,
                 border_padding: int,
                 left_padding: int,
                 border_line_width: int,
                 dpi: int
                 ):

        # output frame rate
        self.frame_rate = output_fps

        # frame size in inches
        self.size = Size(width, height)

        # frame resolution in pixels
        self.res = self.size.get_resolution(dpi)

        # padding around the frame
        self.border_padding = border_padding

        # padding on left side
        self.left_padding = left_padding

        # width of border to draw around the frame
        self.border_line_width = border_line_width

        self.dpi = dpi

    @property
    def width(self):
        return self.res.width

    @property
    def height(self):
        return self.res.height

    @property
    def padding(self) -> Padding:
        # Adjust padding to avoid double application of border padding
        adjusted_padding = max(0, self.border_padding - self.border_line_width)

        # Compute frame padding
        return EqualPadding(adjusted_padding) + LeftPadding(self.left_padding)

    @property
    def canvas_size(self) -> Resolution:
        '''
        Returns the drawable canvas width, accounting for padding and border width.
        '''
        horiz_padding = self.padding.left + self.padding.right + 2 * self.border_line_width
        width = self.res.width - horiz_padding
        vert_padding = self.padding.top + self.padding.bottom + 2 * self.border_line_width
        height = self.res.height - vert_padding
        return Resolution(width, height)

    def print_info(self):
        print(f'Flipbook frame size: {self.res}')
        print(f'frame_border_padding: {self.border_padding}')
        print(f'frame_left_padding: {self.left_padding}')

