import cv2
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from src.flipbook_constants import FlipbookConstants
from src.input_format import InputFormat
from src.output_format import OutputFormat
from src.padding import EqualPadding, LeftPadding, ZeroPadding
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
        self.frame_settings = frame_settings
        self.frame = self.__set_frame(img)

        # Initialize frame padding to zero
        self.canvas_padding = ZeroPadding()

    def get_frame(self):
        return self.frame

    def __set_frame(self, img):
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame.astype('uint8'), 'RGB')

        # resize based on output size
        # How do we do this?
        # Do we want an absolute padding to be set by script?
        #    Yes.
        # Do we want absolute left padding to be set by script?
        #    Yes.
        # OK.  then, we need to do a calculation.
        # canvas_width = output width - padding.left - padding.right
        # canvas_height = output_height - padding.top - padding.bottom

        canvas_width = self.frame_settings.canvas_width()
        canvas_height = self.frame_settings.canvas_height()

        input_width = self.frame_settings.input_width()
        input_height = self.frame_settings.input_height()

        input_aspect = input_height/input_width
        print(f'input_aspect: {input_aspect}')
        canvas_aspect = canvas_height/canvas_width
        print(f'canvas_aspect: {canvas_aspect}')

        # Check which dimension to fit to the canvas
        if input_aspect >= canvas_aspect:
            # rel input_height >= rel canvas_height
            # input frame aspect ratio is taller than canvas
            # fit to canvas height
            resize_height = canvas_height
            resize_width = int(input_aspect * resize_height)
        else:
            # rel input_height < rel canvas_height
            # input frame aspect ratio is shorter than canvas
            # fit to canvas width
            resize_width = canvas_width
            resize_height = int(resize_width / input_aspect)

        print(f'input: {input_width}x{input_height}')
        print(f'canvas: {canvas_width}x{canvas_height}')
        print(f'resize: {resize_width}x{resize_height}')
        frame.resize((resize_width, resize_height))

        # then add watermark to the frame
        self.add_watermark_to_img(frame)
        return frame

    def get_offset(self):
        row = self.frame_no // self.frame_settings.output_format.ncols
        col = self.frame_no % self.frame_settings.output_format.nrows

        width = self.frame_settings.output_height()
        height = self.frame_settings.output_height()

        offset_width = width * col
        offset_height = height * row

        return offset_width, offset_height

    def draw_border(self):
        grid = None
        draw = ImageDraw.Draw(grid)
        # draw vertical and horizontal lines at end of each frame
        end_of_width = offset_width + self.frame_width() + self.pad()
        end_of_height = offset_height + self.frame_height() + self.pad()
        draw.line((end_of_width, 0, end_of_width, end_of_height), fill=0, width=2)
        draw.line((0, end_of_height, end_of_width, end_of_height), fill=0, width=2)

    def add_watermark_to_img(self, img):
        watermark_text = str(self.frame_no)
        # https://www.tutorialspoint.com/python_pillow/python_pillow_creating_a_watermark.htm
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FlipbookConstants.Font.DEFAULT, FlipbookConstants.Font.SIZE)
        text_color = (255, 255, 255)
        text_width, text_height = draw.textsize(watermark_text, font)

        # Position at bottom left-hand corner of the image
        height_pos = self.frame_settings.output_height() - text_height - self.frame_settings.padding.bottom
        height_pos = self.frame_settings.output_height() - (self.frame_settings.padding.bottom + text_height)
        position = (0, height_pos)
        print(f'adding watermark to image. {self.frame_no}, at {position}')
        draw.text(position, watermark_text, font=font, fill=text_color)


