
from src.flipbook_output import FlipbookOutput
from src.resizer import Resizer
from src.size import Size

class Canvas:
    def __init__(self,
                 input_aspect: float,
                 flipbook_output: FlipbookOutput
                 ):
        self.flipbook_output = flipbook_output
        self.resizer = Resizer(input_aspect, self.size)

    @property
    def size(self) -> Size:
        return self.flipbook_output.canvas_size

    @property
    def resize_size(self) -> Size:
        return self.resizer.resize_size

    @property
    def padding(self):
        return self.resizer.padding
