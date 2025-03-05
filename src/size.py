from dataclasses import dataclass


@dataclass
class Size:
    width: int
    height: int

    def __repr__(self):
        return f'{self.width}x{self.height}'

    @property
    def tuple(self):
        return self.width, self.height

    @property
    def aspect(self):
        return float(self.height) / float(self.width)

