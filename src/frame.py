import cv2
from PIL import Image, ImageOps
from PIL import ImageDraw
from PIL import ImageFont

from src.flipbook_constants import FlipbookConstants
from src.flipbook_output import FlipbookOutput
from src.padding import EqualPadding, Padding
from src.padding import LeftPadding
from src.padding import ZeroPadding
from src.padding import HorizontalPadding
from src.padding import VerticalPadding
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
        self.padding = self.flipbook_output.padding

        # Initialize canvas padding (to be updated later)
        self.canvas_padding = ZeroPadding()

    def get_frame(self) -> Image.Image:
        '''
        Generates and returns a frame with correct padding, aspect ratio adjustments, and watermark.
        '''
        input_aspect = self.video_source.aspect

        canvas_width = self.flipbook_output.canvas_width
        canvas_height = self.flipbook_output.canvas_height
        canvas_aspect = self.flipbook_output.canvas_aspect

        # resize based on output size
        # Check which dimension to fit to the canvas
        if input_aspect > canvas_aspect:
            # rel input_height >= rel canvas_height
            # input frame aspect ratio is taller than canvas
            # fit to canvas height
            resize_height = canvas_height
            resize_width = int(resize_height / input_aspect)
            pad = canvas_width - resize_width
            self.canvas_padding = HorizontalPadding(pad)
        else:
            # rel input_height < rel canvas_height
            # input frame aspect ratio is shorter than canvas
            # fit to canvas width
            resize_width = canvas_width
            resize_height = int(resize_width * input_aspect)
            pad = canvas_height - resize_height
            self.canvas_padding = VerticalPadding(pad)

        output_width = self.flipbook_output.frame_output_width
        output_height = self.flipbook_output.frame_output_height

        frame = Image.new('RGB', (output_width, output_height), 'white')

        # Convert OpenCV image (BGR) to PIL Image (RGB)
        img = cv2.cvtColor(self.data, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img.astype('uint8'), 'RGB')

        img = img.resize((resize_width, resize_height))

        # Combine the frame padding with canvas padding
        padding = self.padding + self.canvas_padding

        # Paste the image based on left, bottom padding
        frame.paste(img, (padding.left, padding.bottom))

        # Add thin border
        frame = ImageOps.expand(frame, border=self.flipbook_output.frame_border_line_width, fill='black')

        # Add watermark to the frame
        self.add_watermark_to_img(frame)
        return frame

    def add_watermark_to_img(self, img: Image.Image) -> None:
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

        # Position at bottom left-hand corner of the image
        # Add left padding to match the bottom padding
        x_pos = self.padding.bottom
        y_pos = self.flipbook_output.frame_output_height - (self.padding.bottom + text_height)
        position = (x_pos, y_pos)

        # Draw the watermark
        draw.text(position, watermark_text, font=font, fill='black')


