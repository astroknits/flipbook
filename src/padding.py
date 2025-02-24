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
        super().__init__(pad, 0, 0, 0)

class VerticalPadding(Padding):
    '''
    Add padding to be split between top and bottom
    '''
    def __init__(self, pad):
        top = pad//2
        bottom = pad//2
        if pad % 2 == 1:
            # if it's an odd number, put the extra pixel on the bottom
            bottom += 1
        super().__init__(0, 0, top, bottom)

class HorizontalPadding(Padding):
    '''
    Add padding to be split between left and right
    '''
    def __init__(self, pad):
        left = pad//2
        right = pad//2
        if pad % 2 == 1:
            # if it's an odd number, put the extra pixel on the left
            left += 1
        super().__init__(left, right, 0, 0)

class ZeroPadding(EqualPadding):
    '''
    Add zero padding
    '''
    def __init__(self):
        super().__init__(0)