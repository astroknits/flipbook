from src.flipbook_output import FlipbookOutput
from src.padding import VerticalPadding, HorizontalPadding


class Canvas:
    def __init__(self,
                 input_aspect: float,
                 flipbook_output: FlipbookOutput):
        self.input_aspect = input_aspect
        self.flipbook_output = flipbook_output
        self.__set_resize_info()

    @property
    def width(self):
        return self.flipbook_output.canvas_width

    @property
    def height(self):
        return self.flipbook_output.canvas_height

    @property
    def aspect(self) -> float:
        '''
        Returns the aspect ratio of the canvas area
        '''
        return float(self.height) / float(self.width)

    @property
    def fit_to_height(self) -> bool:
        # Determine whether input height is greater than canvas height
        return self.input_aspect > self.aspect

    @property
    def resize_res(self):
        return self.resize_width, self.resize_height

    def __set_resize_info(self) -> None:
        # resize based on output size
        # Check which dimension to fit to the canvas
        if self.fit_to_height:
            # rel input_height >= rel canvas_height
            # input frame aspect ratio is taller than canvas
            # fit to canvas height
            self.resize_height = self.height
            self.resize_width = int(self.resize_height / self.input_aspect)
            self.padding = HorizontalPadding(self.width - self.resize_width)
        else:
            # rel input_height < rel canvas_height
            # input frame aspect ratio is shorter than canvas
            # fit to canvas width
            self.resize_width = self.width
            self.resize_height = int(self.resize_width * self.input_aspect)
            self.padding = VerticalPadding(self.height - self.resize_height)

