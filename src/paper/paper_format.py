from src.media.size import Size

class PaperFormat:
    '''
    Class owning information about the paper
    type on which the flipbook will be printed
    '''
    def __init__(self,
                 name: str,
                 width: float,
                 height: float,
                 dpi: int = 300):
        self.name = name
        self.size = Size(width, height)
        self.res = self.size.get_resolution(dpi)
        self.dpi = dpi

    @property
    def aspect(self) -> float:
        return self.res.aspect

    @property
    def width(self):
        return self.res.width

    @property
    def height(self):
        return self.res.height