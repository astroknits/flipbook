

class PaperFormat:
    '''
    Class owning information about the paper
    type on which the flipbook will be printed
    '''
    def __init__(self, name, width, height, dpi=300):
        self.name = name
        self.width = width
        self.height = height
        self.aspect = self.height/self.width
        self.dpi = dpi

    def get_resolution(self):
        # Given a printer's dpi (dots per inch),
        # provide the resolution (pixels wide x pixels high)
        return (self.xres(), self.yres())

    def xres(self):
        # Given a printer's dpi (dots per inch),
        # provide the x resolution (pixels wide)
        return int(self.width * self.dpi)

    def yres(self):
        # Given a printer's dpi (dots per inch),
        # provide the y resolution (pixels high)
        return int(self.height * self.dpi)
