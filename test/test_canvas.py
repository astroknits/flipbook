import unittest
from unittest.mock import MagicMock
from src.canvas import Canvas
from src.resizer import Resizer
from src.resolution import Resolution
from src.padding import Padding


class TestCanvas(unittest.TestCase):
    def setUp(self):
        self.mock_resolution = Resolution(800, 600)
        self.mock_resizer = MagicMock(spec=Resizer)
        self.mock_resizer.resize_res = Resolution(640, 480)
        self.mock_resizer.padding = Padding(10, 10, 5, 5)

    def test_canvas_initialization(self):
        canvas = Canvas(16 / 9, self.mock_resolution)
        self.assertEqual(canvas.input_aspect, 16 / 9)
        self.assertEqual(canvas.res, self.mock_resolution)
        self.assertIsInstance(canvas.resizer, Resizer)

    def test_canvas_resize_res(self):
        with unittest.mock.patch('src.canvas.Resizer', return_value=self.mock_resizer):
            canvas = Canvas(16 / 9, self.mock_resolution)
            self.assertEqual(canvas.resize_res, Resolution(640, 480))

    def test_canvas_padding(self):
        with unittest.mock.patch('src.canvas.Resizer', return_value=self.mock_resizer):
            canvas = Canvas(16 / 9, self.mock_resolution)
            self.assertEqual(canvas.padding, Padding(10, 10, 5, 5))


if __name__ == "__main__":
    unittest.main()
