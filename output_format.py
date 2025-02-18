from enum import Enum


class Resolution:
    def __init__(self, name, aspect):
        self.name = name
        self.aspect = aspect


class PaperFormat(Enum):
    LETTER = Resolution('US Letter', 11.0/8.5)
    LEGAL = Resolution('US Legal', 14.0/8.5)


class OutputFormat:
    def __init__(self, ncols, nrows, frame_rate, paper_format, frame_border_padding=20):
        self.ncols = ncols
        self.nrows = nrows
        self.frame_rate = frame_rate
        self.paper_format = paper_format
        # How many pixels border padding to add around each frame (default 20)
        self.frame_border_padding = frame_border_padding

    def print(self):
        print(f'ncols: {self.ncols}')
        print(f'nrows: {self.nrows}')
        print(f'Frame rate: {self.frame_rate:.2f} fps')
        print(f'Page format: {self.paper_format.value.name}')
        print(f'Page aspect ratio: {self.paper_format.value.aspect:.2f}')
