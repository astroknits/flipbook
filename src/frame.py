from typing import Tuple

import cv2
from PIL import Image, ImageOps
from PIL import ImageDraw
from PIL import ImageFont

from src.canvas import Canvas
from src.flipbook_constants import FlipbookConstants
from src.flipbook_output import FlipbookOutput
from src.padding import HorizontalPadding, VerticalPadding
from src.video_source import VideoSource


class Frame:
    def __init__(self,
                 data: cv2.UMat,
                 frame_no: int,
                 video_source: VideoSource,
                 flipbook_output: FlipbookOutput
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
        self.video_source = video_source
        self.flipbook_output = flipbook_output

    @property
    def input_aspect(self):
        return self.video_source.aspect

    @property
    def output_width(self):
        return self.flipbook_output.width

    @property
    def output_height(self):
        return self.flipbook_output.height

    @property
    def frame_border_line_width(self):
        return self.flipbook_output.border_line_width

    def get_frame(self) -> Image.Image:
        '''
        Generates and returns a frame with correct padding, aspect ratio adjustments, and watermark.
        '''
        canvas = Canvas(self.input_aspect, self.flipbook_output)

        resize_res = canvas.resize_res
        padding = self.flipbook_output.padding + canvas.padding

        frame = Image.new('RGB', (self.output_width, self.output_height), 'white')

        # Convert OpenCV image (BGR) to PIL Image (RGB)
        img = cv2.cvtColor(self.data, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img.astype('uint8'), 'RGB')
        img = img.resize(resize_res)

        # Paste the image based on left, bottom padding
        frame.paste(img, (padding.left, padding.bottom))

        # Add thin border
        frame = ImageOps.expand(frame, border=self.frame_border_line_width, fill='black')

        # Add watermark to the frame

        # Position at bottom left-hand corner of the image
        # Add left padding to match the bottom padding
        x_pos = padding.bottom
        y_pos = self.flipbook_output.height - padding.bottom

        self.add_watermark_to_img(frame, (x_pos, y_pos))
        return frame

    def add_watermark_to_img(self, img: Image.Image, loc: Tuple[int, int]) -> None:
        # Add the frame number as a watermark text on the bottom left corner
        watermark_text = str(self.frame_no)
        draw = ImageDraw.Draw(img)

        # Load font, with fallback
        try:
            font = ImageFont.truetype(
                FlipbookConstants.Font.DEFAULT,
                FlipbookConstants.Font.SIZE)
        except (OSError, IOError):
            print((f'Unable to load font {FlipbookConstants.Font.DEFAULT}.'
                  '  loading default font'))
            font = ImageFont.load_default() # fallback font

        # Get the text width/height (for help to calculate location to print)
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # position at bottom left-hand corner of frame
        position = (loc[0], loc[1] - text_height)

        # Draw the watermark
        draw.text(position, watermark_text, font=font, fill='black')

