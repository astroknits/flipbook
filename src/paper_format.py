from enum import Enum

class PaperSize:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.aspect = self.height/self.width

    def get_resolution(self, dpi):
        # Given a printer's dpi (dots per inch),
        # provide the resolution (pixels wide x pixels high)
        return (self.width * dpi, self.height * dpi)


class PaperFormat(Enum):
    '''
    Type of paper on which the flipbook will be printed
    '''
    LETTER = PaperSize('US Letter', 8.5, 11.0)
    LEGAL = PaperSize('US Legal', 8.5, 14.0)
