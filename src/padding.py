class Padding:
    '''
    Class to store the padding for a given frame
    '''
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def __add__(self, other):
        return Padding(
            self.left + other.left,
            self.right + other.right,
            self.top + other.top,
            self.bottom + other.bottom)

class EqualPadding(Padding):
    '''
    Pad each side equally
    '''
    def __init__(self, pad):
        super().__init__(pad, pad, pad, pad)

class LeftPadding(Padding):
    '''
    Pad left side only
    '''
    def __init__(self, pad):
        super().__init__(pad, 0, 0, 0, 0)

