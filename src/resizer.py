from src.resolution import Resolution
from src.padding import HorizontalPadding
from src.padding import VerticalPadding

class Resizer:
    def __init__(self,
                 input_aspect: float,
                 canvas_res: Resolution
                 ):
        self.input_aspect = input_aspect
        self.canvas_res = canvas_res
        self.resize_res, self.padding = self._compute_resize()

    @property
    def aspect(self) -> float:
        return self.canvas_res.aspect

    @property
    def fit_to_height(self) -> bool:
        return self.input_aspect > self.aspect

    def _compute_resize(self):
        if self.fit_to_height:
            resize_height = self.canvas_res.height
            resize_width = int(resize_height / self.input_aspect)
            padding = HorizontalPadding(self.canvas_res.width - resize_width)
        else:
            resize_width = self.canvas_res.width
            resize_height = int(resize_width * self.input_aspect)
            padding = VerticalPadding(self.canvas_res.height - resize_height)

        return Resolution(resize_width, resize_height), padding
