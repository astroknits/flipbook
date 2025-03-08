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
        self.dpi = dpi

    @property
    def res(self):
        return self.size.get_resolution(self.dpi)

    @property
    def aspect(self) -> float:
        return self.res.aspect

    @property
    def width(self):
        return self.res.width

    @property
    def height(self):
        return self.res.height