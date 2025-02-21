

class PaperFormat:
    '''
    Class owning information about the paper
    type on which the flipbook will be printed
    '''
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.aspect = self.height/self.width

    def get_resolution(self, dpi):
        # Given a printer's dpi (dots per inch),
        # provide the resolution (pixels wide x pixels high)
        return (self.width * dpi, self.height * dpi)
