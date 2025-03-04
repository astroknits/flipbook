

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
        self.width_inches = width
        self.height_inches = height
        self.width = int(width * dpi)
        self.height = int(height * dpi)
        self.dpi = dpi

    @property
    def aspect(self) -> float:
        return self.height_inches / self.width_inches
