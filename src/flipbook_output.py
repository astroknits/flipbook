from src.padding import EqualPadding, LeftPadding, Padding, HorizontalPadding, VerticalPadding


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

    def fit_to_height(self, input_aspect):
        # Determine whether input height is greater than canvas height
        return input_aspect > self.canvas_aspect

    def get_resize_res(self, input_aspect):
        # resize based on output size
        # Check which dimension to fit to the canvas
        if self.fit_to_height(input_aspect):
            # rel input_height >= rel canvas_height
            # input frame aspect ratio is taller than canvas
            # fit to canvas height
            resize_height = self.canvas_height
            resize_width = int(resize_height / input_aspect)
        else:
            # rel input_height < rel canvas_height
            # input frame aspect ratio is shorter than canvas
            # fit to canvas width
            resize_width = self.canvas_width
            resize_height = int(resize_width * input_aspect)
        return resize_width, resize_height

    def get_padding(self, input_aspect) -> Padding:
        # Calculate how much padding we need to add to the
        # canvas to accommodate the newly resized source image
        # to get the dimensions of the final flipbook frame
        resize_width, resize_height = self.get_resize_res(input_aspect)

        if self.fit_to_height(input_aspect):
            return self.padding + HorizontalPadding(self.canvas_width - resize_width)
        else:
            return self.padding + VerticalPadding(self.canvas_height - resize_height)


    def print_info(self):
        print(f'Flipbook frame size: {self.frame_output_width}x{self.frame_output_height}')
        print(f'frame_border_padding: {self.frame_border_padding}')
        print(f'frame_left_padding: {self.frame_left_padding}')

