import cv2
from PIL import Image, ImageOps
from PIL import ImageDraw
from PIL import ImageFont

from src.flipbook_constants import FlipbookConstants
from src.input_format import InputFormat
from src.output_format import OutputFormat
from src.padding import EqualPadding, LeftPadding, ZeroPadding, HorizontalPadding, VerticalPadding
from src.paper_type import PaperType


class FrameSettings:
    def __init__(self,
                 filename,
                 output_width,
                 output_height,
                 output_frame_rate,
                 paper_type,
                 ):

        # video file name
        self.input_format = InputFormat(filename)

        self.output_format = OutputFormat(
            output_width,
            output_height,
            output_frame_rate,
            PaperType.get(paper_type),
        )

        # Get the padding values in each dimension
        self.padding = self.get_frame_border_padding() + self.get_left_binding_padding()

    def frames_per_page(self):
        return self.output_format.frames_per_page()

    def get_frame_border_padding(self):
        # TODO add logic
        equal_padding = 50
        return EqualPadding(equal_padding)

    def get_left_binding_padding(self):
        # TODO add logic
        left_binding_padding = 260
        return LeftPadding(left_binding_padding)

    def input_width(self):
        return self.input_format.width

    def input_height(self):
        return self.input_format.height

    def output_width(self):
        return self.output_format.xres()

    def output_height(self):
        return self.output_format.yres()

    def canvas_width(self):
        return self.output_width() - self.padding.left - self.padding.right

    def canvas_height(self):
        return self.output_height() - self.padding.top - self.padding.bottom

    def print(self):
        print(f'Frame border padding: {self.get_frame_border_padding()}')
        print(f'Left binding padding: {self.get_left_binding_padding()}')




class Frame:
    def __init__(self, img, frame_no, frame_settings):
        self.frame_no = frame_no
        self.settings = frame_settings
        self.frame = self.__set_frame(img)

        # Initialize frame padding to zero
        self.canvas_padding = ZeroPadding()

    def get_frame(self):
        return self.frame

    def __set_frame(self, img):
        frame = Image.new('RGB', (self.settings.output_width(), self.settings.output_height()), 'white')

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img.astype('uint8'), 'RGB')

        # resize based on output size
        canvas_width = self.settings.canvas_width()
        canvas_height = self.settings.canvas_height()

        input_width = self.settings.input_width()
        input_height = self.settings.input_height()

        input_aspect = input_height/input_width
        print(f'input_aspect: {input_aspect}')
        canvas_aspect = canvas_height/canvas_width
        print(f'canvas_aspect: {canvas_aspect}')

        resize_width = input_width
        resize_height = input_height

        # Check which dimension to fit to the canvas
        if input_aspect > canvas_aspect:
            # rel input_height >= rel canvas_height
            # input frame aspect ratio is taller than canvas
            # fit to canvas height
            resize_height = canvas_height
            resize_width = int(input_aspect * resize_height)
            self.canvas_padding = HorizontalPadding(canvas_width - resize_width)
        else:
            # rel input_height < rel canvas_height
            # input frame aspect ratio is shorter than canvas
            # fit to canvas width
            resize_width = canvas_width
            resize_height = int(resize_width / input_aspect)
            self.canvas_padding = VerticalPadding(canvas_height - resize_height)

        img = img.resize((resize_width, resize_height))

        padding = self.settings.padding + self.canvas_padding

        # offset:
        x_offset = padding.left
        y_offset = padding.bottom

        frame.paste(img, (x_offset, y_offset))

        frame = ImageOps.expand(frame, border=3, fill='black')
        # then add watermark to the frame
        self.add_watermark_to_img(frame)
        return frame

    def get_offset(self):
        rel_frame_no = self.frame_no % self.settings.frames_per_page()

        row = rel_frame_no // self.settings.output_format.nrows
        col = rel_frame_no % self.settings.output_format.nrows

        width = self.settings.output_width()
        height = self.settings.output_height()

        offset_width = width * col
        offset_height = height * row

        return offset_width, offset_height

    def add_watermark_to_img(self, img):
        watermark_text = str(self.frame_no)
        # https://www.tutorialspoint.com/python_pillow/python_pillow_creating_a_watermark.htm
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FlipbookConstants.Font.DEFAULT, FlipbookConstants.Font.SIZE)
        text_width, text_height = draw.textsize(watermark_text, font)

        # Position at bottom left-hand corner of the image
        height_pos = self.settings.output_height() - text_height - self.settings.padding.bottom
        height_pos = self.settings.output_height() - (self.settings.padding.bottom + text_height)
        position = (0, height_pos)
        print(f'adding watermark to image. {self.frame_no}, at {position}')
        draw.text(position, watermark_text, font=font, fill='black')


