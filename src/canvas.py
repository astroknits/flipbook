
from src.flipbook_output import FlipbookOutput
from src.padding import Padding
from src.resizer import Resizer
from src.resolution import Resolution

class Canvas:
    def __init__(self,
                 input_aspect: float,
                 flipbook_output: FlipbookOutput
                 ):
        self.flipbook_output = flipbook_output
        self.resizer = Resizer(input_aspect, self.res)

    @property
    def res(self) -> Resolution:
        return self.flipbook_output.canvas_size

    @property
    def resize_res(self) -> Resolution:
        return self.resizer.resize_res

    @property
    def padding(self) -> Padding:
        return self.resizer.padding
