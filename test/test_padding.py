import unittest
from src.padding import Padding
from src.padding import EqualPadding
from src.padding import LeftPadding
from src.padding import VerticalPadding
from src.padding import HorizontalPadding
from src.padding import ZeroPadding


class TestPadding(unittest.TestCase):
    def test_padding(self):
        padding = Padding(1, 4, 2, 33)
        self.assertEqual(padding.left, 1)
        self.assertEqual(padding.right, 4)
        self.assertEqual(padding.top, 2)
        self.assertEqual(padding.bottom, 33)

    def test_equal_padding(self):
        padding = EqualPadding(5)
        self.assertEqual(padding.left, 5)
        self.assertEqual(padding.right, 5)
        self.assertEqual(padding.top, 5)
        self.assertEqual(padding.bottom, 5)

    def test_left_padding(self):
        padding = LeftPadding(5)
        self.assertEqual(padding.left, 5)
        self.assertEqual(padding.right, 0)
        self.assertEqual(padding.top, 0)
        self.assertEqual(padding.bottom, 0)

    def test_vertical_padding(self):
        padding = VerticalPadding(7)
        self.assertEqual(padding.left, 0)
        self.assertEqual(padding.right, 0)
        self.assertEqual(padding.top, 3)
        self.assertEqual(padding.bottom, 4)

    def test_horizontal_padding(self):
        padding = HorizontalPadding(7)
        self.assertEqual(padding.left, 7)
        self.assertEqual(padding.right, 0)
        self.assertEqual(padding.top, 0)
        self.assertEqual(padding.bottom, 0)

    def test_zero_padding(self):
        padding = ZeroPadding()
        self.assertEqual(padding.left, 0)
        self.assertEqual(padding.right, 0)
        self.assertEqual(padding.top, 0)
        self.assertEqual(padding.bottom, 0)

class TestAddPadding(unittest.TestCase):
    def test_add_padding(self):
        padding1 = Padding(1, 4, 2, 33)
        padding2 = Padding(2, 17, 2, 3)

        result = padding1 + padding2
        self.assertEqual(result.left, 3)
        self.assertEqual(result.right, 21)
        self.assertEqual(result.top, 4)
        self.assertEqual(result.bottom, 36)





if __name__ == '__main__':
    unittest.main()

