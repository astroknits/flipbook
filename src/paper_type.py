from enum import Enum
from src.paper_format import PaperFormat

class PaperType(Enum):
    '''
    Type of paper on which the flipbook will be printed
    '''
    LETTER = PaperFormat('US Letter', 8.5, 11.0)
    LEGAL = PaperFormat('US Legal', 8.5, 14.0)

    @staticmethod
    def get(key):
        # Helper method to get enum from lower case string
        return PaperType[key.upper()]

