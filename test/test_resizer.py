import unittest
from unittest.mock import Mock
from src.media.resolution import Resolution
from src.media.padding import VerticalPadding, LeftPadding
from src.media.resizer import Resizer


class TestResizer(unittest.TestCase):
    def test_fit_to_height_true(self):
        """Test when input aspect is greater than canvas aspect (fit to height)."""
        canvas_res = Mock(width=800, height=600, aspect=800 / 600)
        resizer = Resizer(input_aspect=16 / 9, canvas_res=canvas_res)

        expected_width = int(600 / (16 / 9))  # height / aspect ratio
        expected_height = 600  # matches canvas height
        expected_padding = LeftPadding(canvas_res.width - expected_width)

        self.assertEqual(resizer.resize_res, Resolution(expected_width, expected_height))
        self.assertEqual(resizer.padding, expected_padding)
        self.assertTrue(resizer.fit_to_height)

    def test_fit_to_width_true(self):
        """Test when input aspect is less than canvas aspect (fit to width)."""
        canvas_res = Mock(width=800, height=600, aspect=800 / 600)
        resizer = Resizer(input_aspect=3 / 4, canvas_res=canvas_res)

        expected_width = 800  # matches canvas width
        expected_height = int(800 * (3 / 4))  # width * aspect ratio
        expected_padding = VerticalPadding(canvas_res.height - expected_height)

        self.assertEqual(resizer.resize_res, Resolution(expected_width, expected_height))
        self.assertEqual(resizer.padding, expected_padding)
        self.assertFalse(resizer.fit_to_height)

    def test_exact_match(self):
        """Test when input aspect exactly matches canvas aspect."""
        canvas_res = Resolution(width=800, height=600)
        resizer = Resizer(input_aspect=3 / 4, canvas_res=canvas_res)

        expected_width = 800  # matches canvas width
        expected_height = 600  # matches canvas height
        expected_padding = VerticalPadding(0)  # No padding needed

        self.assertEqual(resizer.resize_res, Resolution(expected_width, expected_height))
        self.assertEqual(resizer.padding, expected_padding)
        self.assertFalse(resizer.fit_to_height)


if __name__ == "__main__":
    unittest.main()
