import cv2
from PIL import Image, ImageOps
from PIL import ImageDraw
from PIL import ImageFont

from src.flipbook_constants import FlipbookConstants
from src.padding import EqualPadding, LeftPadding, ZeroPadding, HorizontalPadding, VerticalPadding


class Frame:
    def __init__(self,
                 img,
                 frame_no,
                 input_width,
                 input_height,
                 output_width,
                 output_height,
                 frame_border_padding,
                 left_frame_padding
                 ):
        self.frame_no = frame_no
        self.input_width = input_width
        self.input_height = input_height
        self.input_aspect = input_height/input_width
        self.output_width = output_width
        self.output_height = output_height

        # Get the padding values in each dimension
        self.padding = self.get_frame_border_padding(frame_border_padding) + \
                       self.get_left_frame_padding(left_frame_padding)

        # Initialize frame padding to zero
        self.canvas_padding = ZeroPadding()

        self.frame = self.__set_frame(img)

    def get_frame_border_padding(self, pad):
        return EqualPadding(pad)

    def get_left_frame_padding(self, pad):
        return LeftPadding(pad)

    def canvas_width(self):
        return self.output_width - self.padding.left - self.padding.right

    def canvas_height(self):
        return self.output_height - self.padding.top - self.padding.bottom

    def print(self):
        print(f'Frame border padding: {self.get_frame_border_padding()}')
        print(f'Left binding padding: {self.get_left_frame_padding()}')

    def get_frame(self):
        return self.frame

    def canvas_aspect(self):
        return self.canvas_height()/self.canvas_width()

    def __set_frame(self, img):
        frame = Image.new('RGB', (self.output_width, self.output_height), 'white')

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img.astype('uint8'), 'RGB')

        # resize based on output size
        # Check which dimension to fit to the canvas
        if self.input_aspect > self.canvas_aspect():
            # rel input_height >= rel canvas_height
            # input frame aspect ratio is taller than canvas
            # fit to canvas height
            resize_height = self.canvas_height()
            resize_width = int(resize_height / self.input_aspect)
            self.canvas_padding = HorizontalPadding(self.canvas_width() - resize_width)
        else:
            # rel input_height < rel canvas_height
            # input frame aspect ratio is shorter than canvas
            # fit to canvas width
            resize_width = self.canvas_width()
            resize_height = int(resize_width / self.input_aspect)
            self.canvas_padding = VerticalPadding(self.canvas_height() - resize_height)

        img = img.resize((resize_width, resize_height))

        # Combine the frame padding with canvas padding
        padding = self.padding + self.canvas_padding

        # Paste the image based on left, bottom padding
        frame.paste(img, (padding.left, padding.bottom))

        # Add thin border
        frame = ImageOps.expand(frame, border=3, fill='black')

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

        # Get the text width/height (for help calculating location to print)
        text_width, text_height = draw.textsize(watermark_text, font)

        # Position at bottom left-hand corner of the image
        # Add left padding to match the bottom padding
        x_pos = self.padding.bottom
        y_pos = self.output_height - (self.padding.bottom + text_height)
        position = (x_pos, y_pos)

        # Draw the watermark
        draw.text(position, watermark_text, font=font, fill='black')


