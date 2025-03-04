from dataclasses import dataclass

@dataclass
class Padding:
    '''
    Class to store the padding for a given frame
    '''
    left: int
    right: int
    top: int
    bottom: int

    def __add__(self, other: "Padding") -> "Padding":
        if not isinstance(other, Padding):
            raise TypeError(f'Cannot add {type(other).__name__} to Padding')

        return Padding(
            self.left + other.left,
            self.right + other.right,
            self.top + other.top,
            self.bottom + other.bottom)

    def __repr__(self) -> str:
        return (f"Padding(left={self.left}, right={self.right}, "
                f"top={self.top}, bottom={self.bottom})")


class EqualPadding(Padding):
    '''
    Pad each side equally
    '''
    def __init__(self, pad: int) -> None:
        super().__init__(pad, pad, pad, pad)


class LeftPadding(Padding):
    '''
    Pad left side only
    '''
    def __init__(self, pad: int) -> None:
        super().__init__(pad, 0, 0, 0)


class VerticalPadding(Padding):
    '''
    Add padding to be split between top and bottom
    '''
    def __init__(self, pad: int) -> None:
        top = pad//2
        bottom = pad//2
        if pad % 2 == 1:
            # if it's an odd number, put the extra pixel on the bottom
            bottom += 1
        super().__init__(0, 0, top, bottom)


class HorizontalPadding(Padding):
    '''
    Add padding horizontally to flipbook.
    For flipbook, keep the image as close as possible
    to the right edge, so add the horizontal padding
    to left side only
    '''
    def __init__(self, pad: int) -> None:
        super().__init__(pad, 0, 0, 0)


class ZeroPadding(EqualPadding):
    '''
    Add zero padding
    '''
    def __init__(self) -> None:
        super().__init__(0)