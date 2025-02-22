from src.padding import EqualPadding, LeftPadding

class Frame:
    def __init__(self, img, equal_padding, left_padding):
        self.img = img
        self.padding = EqualPadding(equal_padding) + LeftPadding(left_padding)

