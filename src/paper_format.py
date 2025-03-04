

class PaperFormat:
    '''
    Class owning information about the paper
    type on which the flipbook will be printed
    '''
    def __init__(self, name, width, height, dpi=300):
        self.name = name
        self.width_inches = width
        self.height_inches = height
        self.width = int(width * dpi)
        self.height = int(height * dpi)
        self.aspect = self.height_inches / self.width_inches
        self.dpi = dpi

