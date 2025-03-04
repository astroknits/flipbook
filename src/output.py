
class Output:
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

    def print_info(self):
        print(f'Flipbook frame size: {self.frame_output_width}x{self.frame_output_height}')
        print(f'frame_border_padding: {self.frame_border_padding}')
        print(f'frame_left_padding: {self.frame_left_padding}')
