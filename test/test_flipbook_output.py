import unittest
from src.media.padding import EqualPadding, LeftPadding
from src.media.resolution import Resolution
from src.media.size import Size
from src.core.flipbook_output import FlipbookOutput

class TestFlipbookOutput(unittest.TestCase):
    def setUp(self):
        self.output_fps = 24.0
        self.width = 6.0  # inches
        self.height = 4.0  # inches
        self.border_padding = 10  # pixels
        self.left_padding = 5  # pixels
        self.border_line_width = 2  # pixels
        self.dpi = 300
        self.flipbook_output = FlipbookOutput(
            self.output_fps, self.width, self.height,
            self.border_padding, self.left_padding,
            self.border_line_width, self.dpi
        )

    def test_frame_rate(self):
        self.assertEqual(self.flipbook_output.frame_rate, self.output_fps)

    def test_size(self):
        self.assertEqual(self.flipbook_output.size.width, self.width)
        self.assertEqual(self.flipbook_output.size.height, self.height)

    def test_resolution(self):
        expected_res = Size(self.width, self.height).get_resolution(self.dpi)
        self.assertEqual(self.flipbook_output.res, expected_res)

    def test_padding(self):
        border_padding = max(0, self.border_padding - self.border_line_width)
        expected_padding = EqualPadding(border_padding) + LeftPadding(self.left_padding)
        self.assertEqual(self.flipbook_output.padding, expected_padding)

    def test_canvas_res(self):
        horiz_padding = self.flipbook_output.padding.left + \
                        self.flipbook_output.padding.right + \
                        2 * self.border_line_width
        vert_padding = self.flipbook_output.padding.top + \
                       self.flipbook_output.padding.bottom + \
                       2 * self.border_line_width
        expected_width = self.flipbook_output.res.width - horiz_padding
        expected_height = self.flipbook_output.res.height - vert_padding

        self.assertEqual(
            self.flipbook_output.canvas_res,
            Resolution(expected_width, expected_height)
        )

    def test_print_info(self):
        self.flipbook_output.print_info()  # Just checking it runs without errors

if __name__ == '__main__':
    unittest.main()
