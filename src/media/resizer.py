from src.media.resolution import Resolution
from src.media.padding import LeftPadding, Padding
from src.media.padding import VerticalPadding

class Resizer:
    def __init__(self,
                 input_aspect: float,
                 canvas_res: Resolution
                 ):
        self.input_aspect = input_aspect
        self.canvas_res = canvas_res
        self.resize_res, self.padding = self.__compute_resize()

    @property
    def aspect(self) -> float:
        # aspect ratio of the canvas area
        return self.canvas_res.aspect

    @property
    def fit_to_height(self) -> bool:
        # fit the input image to the canvas height?
        # (True -> means fit to height; False -> means fit to width)
        return self.input_aspect > self.aspect

    def __compute_resize(self) -> tuple[Resolution, Padding]:
        '''
        return the parameters for resizing the input video frames
        to the size of the output frame canvas
        '''
        if self.fit_to_height:
            resize_height = self.canvas_res.height
            resize_width = int(resize_height / self.input_aspect)
            # When fitting to height, we want the image to be as far
            # to the right of the book as possible (for left-bound book)
            # so use LeftPadding instead of HorizontalPadding
            padding = LeftPadding(self.canvas_res.width - resize_width)
        else:
            resize_width = self.canvas_res.width
            resize_height = int(resize_width * self.input_aspect)
            padding = VerticalPadding(self.canvas_res.height - resize_height)

        return Resolution(resize_width, resize_height), padding
