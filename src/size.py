from dataclasses import dataclass
from typing import Tuple

from src.resolution import Resolution


@dataclass
class Size:
    width: float
    height: float

    def __repr__(self):
        return f'{self.width}x{self.height}'

    @property
    def tuple(self) -> Tuple[float, float]:
        return self.width, self.height

    @property
    def aspect(self) -> float:
        return float(self.height) / float(self.width)

    def get_resolution(self, dpi: int) -> Resolution:
        return Resolution(int(self.width * dpi), int(self.height * dpi))
