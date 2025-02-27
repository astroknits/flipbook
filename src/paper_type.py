from enum import Enum
from src.paper_format import PaperFormat

class PaperType(Enum):
    '''
    Type of paper on which the flipbook will be printed
    '''
    LETTER = PaperFormat('US Letter',  11.0, 8.5)
    LEGAL = PaperFormat('US Legal', 14.0, 8.5)

    @staticmethod
    def get(key):
        # Helper method to get enum from lower case string
        return PaperType[key.upper()]

