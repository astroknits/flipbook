import cv2
from PIL import Image, ImageOps
from PIL import ImageDraw
from PIL import ImageFont

from src.flipbook_constants import FlipbookConstants
from src.padding import EqualPadding
from src.padding import LeftPadding
from src.padding import ZeroPadding
from src.padding import HorizontalPadding
from src.padding import VerticalPadding


class Frame:
    def __init__(self,
                 data,
                 frame_no,
                 input_width,
                 input_height,
                 output_width,
                 output_height,
                 frame_border_padding,
                 left_frame_padding,
                 frame_border_line_width=3,
                 ):
        self.data = data
        self.frame_no = frame_no
        self.input_width = input_width
        self.input_height = input_height
        self.input_aspect = input_height/input_width
        self.output_width = output_width
        self.output_height = output_height

        # decrease the frame_border_padding value by frame_border_line_width
        # as this gets added after the frame has been created
        frame_border_padding -= frame_border_line_width

        # Get the padding values in each dimension
        self.padding = self.get_frame_border_padding(frame_border_padding) + \
                       self.get_left_frame_padding(left_frame_padding)

        # Border line width, gets added after the fact
        self.frame_border_line_width = frame_border_line_width

        # Initialize frame padding to zero
        self.canvas_padding = ZeroPadding()

    def get_frame_border_padding(self, pad):
        return EqualPadding(pad)

    def get_left_frame_padding(self, pad):
        return LeftPadding(pad)

    def canvas_width(self):
        return self.output_width - self.padding.left - self.padding.right - 2 * self.frame_border_line_width

    def canvas_height(self):
        return self.output_height - self.padding.top - self.padding.bottom - 2 * self.frame_border_line_width

    def canvas_aspect(self):
        return self.canvas_height()/self.canvas_width()

    def get_frame(self):
        frame = Image.new('RGB', (self.output_width, self.output_height), 'white')

        img = cv2.cvtColor(self.data, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img.astype('uint8'), 'RGB')

        # resize based on output size
        # Check which dimension to fit to the canvas
        if self.input_aspect > self.canvas_aspect():
            # rel input_height >= rel canvas_height
            # input frame aspect ratio is taller than canvas
            # fit to canvas height
            resize_height = self.canvas_height()
            resize_width = int(resize_height / self.input_aspect)
            pad = self.canvas_width() - resize_width
            self.canvas_padding = HorizontalPadding(pad)
        else:
            # rel input_height < rel canvas_height
            # input frame aspect ratio is shorter than canvas
            # fit to canvas width
            resize_width = self.canvas_width()
            resize_height = int(resize_width / self.input_aspect)
            pad = self.canvas_height() - resize_height
            self.canvas_padding = VerticalPadding(pad)

        img = img.resize((resize_width, resize_height))

        # Combine the frame padding with canvas padding
        padding = self.padding + self.canvas_padding

        # Paste the image based on left, bottom padding
        frame.paste(img, (padding.left, padding.bottom))

        # Add thin border
        frame = ImageOps.expand(frame, border=self.frame_border_line_width, fill='black')

        # Add watermark to the frame
        self.add_watermark_to_img(frame)
        return frame

    def add_watermark_to_img(self, img):
        # Add the frame number as a watermark text on the bottom left corner
        watermark_text = str(self.frame_no)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(
            FlipbookConstants.Font.DEFAULT,
            FlipbookConstants.Font.SIZE)

        # Get the text width/height (for help to calculate location to print)
        text_width, text_height = draw.textsize(watermark_text, font)

        # Position at bottom left-hand corner of the image
        # Add left padding to match the bottom padding
        x_pos = self.padding.bottom
        y_pos = self.output_height - (self.padding.bottom + text_height)
        position = (x_pos, y_pos)

        # Draw the watermark
        draw.text(position, watermark_text, font=font, fill='black')


