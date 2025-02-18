

class OutputFormat:
    def __init__(self, ncols, nrows, frame_rate):
        self.ncols = ncols
        self.nrows = nrows
        self.frame_rate = frame_rate

    def print(self):
        print(f'ncols: {self.ncols}')
        print(f'nrows: {self.nrows}')
        print(f'Frame rate: {self.frame_rate:.2f} fps')
