from typing import Tuple

import cv2
from PIL import Image, ImageOps
from PIL import ImageDraw
from PIL import ImageFont

from src.helpers.flipbook_helper import FlipbookHelper
from src.media.canvas import Canvas
from src.helpers.flipbook_constants import FlipbookConstants
from src.core.flipbook_output import FlipbookOutput


class Frame:
    def __init__(self,
                 data: cv2.UMat,
                 frame_no: int,
                 flipbook_output: FlipbookOutput,
                 canvas: Canvas,
                 ) -> None:
        '''
        Initializes a Frame object.

        :param data: The image frame data (from OpenCV).
        :param frame_no: The frame number in the sequence.
        :param video_source: Object for input video data
        :param FlipbookOutput: Object for flipbook output params
        '''
        self.data = data
        self.frame_no = frame_no
        self.flipbook_output = flipbook_output
        self.canvas = canvas
        self.padding = self.flipbook_output.padding + self.canvas.padding

    @property
    def input_aspect(self) -> float:
        # aspect ratio of the canvas
        return self.canvas.input_aspect

    @property
    def output_width(self) -> int:
        # width of the flipbook frames in pixels
        return self.flipbook_output.width

    @property
    def output_height(self) -> int:
        # height of the flipbook frames in pixels
        return self.flipbook_output.height

    @property
    def frame_border_line_width(self) -> int:
        # width in pixels of the line drawn around
        # the border of each frame
        return self.flipbook_output.border_line_width

    def get_frame(self) -> Image.Image:
        '''
        Generates and returns a frame with correct padding, aspect ratio adjustments, and watermark.
        '''

        adjusted_width = self.output_width - 2 * self.frame_border_line_width
        adjusted_height = self.output_height - 2 * self.frame_border_line_width
        frame = Image.new('RGB', (adjusted_width, adjusted_height), 'white')

        # Convert OpenCV image (BGR) to PIL Image (RGB)
        img = cv2.cvtColor(self.data, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img.astype('uint8'), 'RGB')
        img = img.resize(self.canvas.resize_res.tuple)

        # Paste the image based on left, bottom padding
        frame.paste(img, (self.padding.left, self.padding.bottom))

        # Add thin border
        frame = ImageOps.expand(frame, border=self.frame_border_line_width, fill='black')

        # Add watermark to the frame
        self.__add_watermark_to_img(frame)
        return frame

    def __get_fontsize(self) -> int:
        return FlipbookHelper.get_fontsize(self.flipbook_output.res)

    def __get_watermark_location(self, text_width: int, text_height: int) \
            -> Tuple[int, int]:
        # Position at bottom left-hand corner of the image
        # Add left padding to match the bottom padding
        x_pos = int(self.padding.right / 2.0)
        y_pos = int(self.flipbook_output.height - self.padding.bottom/2.0)
        y_pos = y_pos - 2 * text_height
        return x_pos, y_pos

    def __add_watermark_to_img(self, img: Image.Image) -> None:
        '''
        Add the frame number as a watermark text on the bottom left corner
        '''
        watermark_text = str(self.frame_no + 1)
        draw = ImageDraw.Draw(img)

        # Load font, with fallback
        try:
            font = ImageFont.truetype(
                FlipbookConstants.Font.DEFAULT,
                self.__get_fontsize())
        except (OSError, IOError):
            print((f'Unable to load font {FlipbookConstants.Font.DEFAULT}.'
                  '  loading default font'))
            font = ImageFont.load_default() # fallback font

        # Get the text width/height (for help to calculate location to print)
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # position at bottom left-hand corner of frame
        position = self.__get_watermark_location(text_width, text_height)

        # Draw the watermark
        draw.text(position, watermark_text, font=font, fill='black')

