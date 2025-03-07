from src.media.padding import Padding
from src.media.resizer import Resizer
from src.media.resolution import Resolution

class Canvas:
    def __init__(self,
                 input_aspect: float,
                 canvas_res: Resolution
                 ):
        self.input_aspect = input_aspect
        self.res = canvas_res
        self.resizer = Resizer(input_aspect, canvas_res)

    @property
    def resize_res(self) -> Resolution:
        return self.resizer.resize_res

    @property
    def padding(self) -> Padding:
        return self.resizer.padding
