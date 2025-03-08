import unittest
from unittest.mock import MagicMock, patch
import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont
from src.core.frame import Frame
from src.core.flipbook_output import FlipbookOutput
from src.media.canvas import Canvas
from src.media.padding import Padding


class TestFrame(unittest.TestCase):
    input_width = 350
    input_height = 700

    def setUp(self):
        # Create mock objects for dependencies
        self.mock_flipbook_output = MagicMock(spec=FlipbookOutput)
        self.mock_canvas = MagicMock(spec=Canvas)

        # Define mock attributes
        self.mock_flipbook_output.width = 800
        self.mock_flipbook_output.height = 600
        self.mock_flipbook_output.padding = Padding(left=150, right=20, bottom=20, top=20)
        self.mock_flipbook_output.border_line_width = 5

        self.mock_canvas.padding = Padding(left=255, right=0, bottom=0, top=0)
        self.mock_canvas.input_aspect = 1.5
        self.mock_canvas.resize_res.tuple = (370, 555)

        # Create a dummy OpenCV image (BGR format)
        img = self.get_zeros_of_dim(self.input_width, self.input_height)
        self.dummy_image = cv2.UMat(img)

        # Create Frame instance
        self.frame = Frame(self.dummy_image, frame_no=1,
                           flipbook_output=self.mock_flipbook_output,
                           canvas=self.mock_canvas)

    def get_zeros_of_dim(self, xdim, ydim) -> np.array:
        return np.zeros((xdim, ydim, 3), dtype=np.uint8)

    def test_properties(self):
        self.assertEqual(self.frame.input_aspect, 1.5)
        self.assertEqual(self.frame.output_width, 800)
        self.assertEqual(self.frame.output_height, 600)
        self.assertEqual(self.frame.frame_border_line_width, 5)

    @patch("cv2.cvtColor")
    @patch("PIL.ImageOps.expand")
    @patch("PIL.Image.fromarray")
    def test_get_frame(self, mock_fromarray, mock_expand, mock_cvtColor):
        mock_cvtColor.return_value = self.get_zeros_of_dim(self.input_width, self.input_height)

        image = Image.new('RGB', (self.input_width, self.input_height), 'white')

        expanded_image = Image.new('RGB', (self.mock_flipbook_output.width, self.mock_flipbook_output.height), 'white')

        mock_fromarray.return_value = image
        mock_expand.return_value = expanded_image

        result = self.frame.get_frame()

        mock_cvtColor.assert_called_once()
        mock_fromarray.assert_called_once()
        mock_expand.assert_called_once()
        self.assertIsInstance(result, Image.Image)

    def side_effect_truetype(*args, **kwargs):
        '''
        Raise OSError only if not calling the default font
        '''
        font_arg = args[0]  # First argument to truetype

        if isinstance(font_arg, str):
            if "DejaVuSans" in font_arg or "default" in font_arg.lower():
                return ImageFont.load_default()  # Allow loading default font
        elif isinstance(font_arg, bytes) or hasattr(font_arg, "read"):  # Handle BytesIO
            return ImageFont.load_default()  # Allow loading if it's a stream

        raise OSError  # Simulate missing custom font

    @patch("PIL.ImageDraw.Draw")
    @patch("PIL.ImageFont.truetype", side_effect=side_effect_truetype)
    def test_add_watermark_to_img_fallback_font(self, mock_truetype, mock_draw):
        mock_img = MagicMock(spec=Image.Image)

        mock_draw_instance = MagicMock()
        mock_draw.return_value = mock_draw_instance

        self.frame._Frame__add_watermark_to_img(mock_img, (50, 50))

        mock_truetype.assert_called_once()
        mock_draw.assert_called_once()
        mock_draw_instance.text.assert_called_once()


if __name__ == "__main__":
    unittest.main()
