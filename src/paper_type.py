from enum import Enum
from src.paper_format import PaperFormat

class PaperType(Enum):
    '''
    Type of paper on which the flipbook will be printed.
    Enum members store (name, width, height) and return a PaperFormat instance.
    '''
    LETTER = ("US Letter", 11.0, 8.5)
    LEGAL = ("US Legal", 14.0, 8.5)

    @property
    def format(self) -> PaperFormat:
        '''Return a PaperFormat instance for the given paper type.'''
        return PaperFormat(*self.value)

    @staticmethod
    def get(key: str) -> "PaperType":
        '''Helper method to get enum from a lowercase string, handling errors.'''
        try:
            return PaperType[key.upper()]
        except KeyError:
            raise ValueError(f"Invalid paper type: {key}")

    def __repr__(self) -> str:
        return f"PaperType.{self.name} (format={self.format})"

