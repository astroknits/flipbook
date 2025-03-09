from enum import Enum

from src.paper.orientation import Orientation
from src.paper.paper_format import PaperFormat

class PaperType(Enum):
    '''
    Type of paper on which the flipbook will be printed.
    Enum members store (name, width, height) and return a PaperFormat instance.
    '''
    LETTER = ("US Letter", 8.5, 11.0)
    LEGAL = ("US Legal", 8.5, 14.0)

    @property
    def format(self, orientation: Orientation = Orientation.PORTRAIT) -> PaperFormat:
        '''Return a PaperFormat instance for the given paper type.'''
        return PaperFormat(*self.value, orientation=orientation)

    @staticmethod
    def get(key: str) -> "PaperType":
        '''Helper method to get enum from a lowercase string, handling errors.'''
        try:
            return PaperType[key.upper()]
        except KeyError:
            raise ValueError(f"Invalid paper type: {key}")

    def __repr__(self) -> str:
        return f"PaperType.{self.name} (format={self.format})"

