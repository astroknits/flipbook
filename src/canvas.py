
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
        canvas_res = flipbook_output.canvas_res
        if canvas_res is None:
            raise ValueError("flipbook_output.canvas_res cannot be None")
        self.resizer = Resizer(input_aspect, canvas_res)

    @property
    def res(self) -> Resolution:
        return self.flipbook_output.canvas_res

    @property
    def resize_res(self) -> Resolution:
        return self.resizer.resize_res

    @property
    def padding(self) -> Padding:
        return self.resizer.padding
