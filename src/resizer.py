from src.size import Size
from src.padding import HorizontalPadding
from src.padding import VerticalPadding

class Resizer:
    def __init__(self, input_aspect: float, canvas_width: int, canvas_height: int):
        self.input_aspect = input_aspect
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.resize_size, self.padding = self._compute_resize()

    @property
    def aspect(self) -> float:
        return self.canvas_height / self.canvas_width

    @property
    def fit_to_height(self) -> bool:
        return self.input_aspect > self.aspect

    def _compute_resize(self):
        if self.fit_to_height:
            resize_height = self.canvas_height
            resize_width = int(resize_height / self.input_aspect)
            padding = HorizontalPadding(self.canvas_width - resize_width)
        else:
            resize_width = self.canvas_width
            resize_height = int(resize_width * self.input_aspect)
            padding = VerticalPadding(self.canvas_height - resize_height)

        return Size(resize_width, resize_height), padding
