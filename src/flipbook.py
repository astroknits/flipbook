import os
from pathlib import Path
from math import ceil
from tqdm import tqdm
import cv2
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from pypdf import PdfWriter

from src.flipbook_constants import FlipbookConstants
from src.input_format import InputFormat
from src.output_format import OutputFormat
from src.paper_type import PaperType


class Flipbook:
    '''
    Class to create frames for flipbook from video file
    '''

    def __init__(
            self,
            filename,
            output_dir,
            ncols=3,
            nrows=3,
            output_frame_rate=0,
            frame_border_padding=50,
            left_binding_padding=260,
             ):

        # video file name
        self.input_video = InputFormat(filename)

        # output directory for output for flipbook
        self.output_dir = output_dir

        self.output_format = OutputFormat(
                                nrows,
                                ncols,
                                output_frame_rate,
                                PaperType.LETTER,
                                frame_border_padding,
                                left_binding_padding,
                            )

        self.n_flipbook_frames = None


    def print_info(self):
        print('\n\n----------------------------')
        print(f'Input Video Info')
        print('----------------------------')
        self.input_video.print()
        print('\n----------------------------')
        print(f'Output Formatting Info')
        print('----------------------------')
        self.output_format.print()
        print('----------------------------\n\n')


    def pad(self):
        return self.output_format.frame_border_padding

    def left_pad(self):
        return self.output_format.left_binding_padding

    def frame_width(self):
        return self.input_video.width

    def frame_height(self):
        return self.input_video.height

    def ncols(self):
        return self.output_format.ncols

    def nrows(self):
        return self.output_format.nrows

    def grid_width(self):
        return int((self.frame_width() + 2 * self.pad() + self.left_pad()) * self.ncols())

    def grid_height(self):
        return int((self.frame_height() + 2 * self.pad()) * self.nrows())

    def create_output_dir(self):
        output_dir_path = Path(self.output_dir)
        if Path.exists(output_dir_path):
            if output_dir_path.is_dir():
                if os.listdir(self.output_dir):
                    raise Exception((f'Output directory {self.output_dir} '
                                     'already exists and is nonempty.'))
                return True
            raise Exception((f'Expected data output directory path {self.output_dir}'
                             ' exists but is not a directory.'))
        # If the data_dir does not exist, crate it
        output_dir_path.mkdir()
        return True

    def extract_frames(self):
        # Input and output frame rates
        fps_in = self.input_video.frame_rate
        fps_out = self.output_format.frame_rate

        # Open the file and open stream
        cam = cv2.VideoCapture(self.input_video.filename)

        # Create a directory for the extracted frames
        self.create_output_dir()

        # Cycle through the frames
        index_out = 0
        frames = []
        for index_in in range(self.input_video.total_frames):
            # Read the frame
            success, frame = cam.read()

            if not success:
                # Before breaking, update with the accurate number of frames
                self.input_video.total_frames = index_in
                break

            # otherwise we process the frame
            out_due = int(index_in / fps_in * fps_out)
            if out_due > index_out:
                success, frame = cam.retrieve()
                if not success:
                    # Before breaking, update with the accurate number of frames
                    self.input_video.total_frames = index_in
                    break
                # otherwise we process the frame
                frames.append(frame)
                index_out += 1

        self.n_flipbook_frames = index_out
        cam.release()
        cv2.destroyAllWindows()
        return frames

    def get_base_output_name(self):
        '''
        Base file name is based on input file name
        '''
        return Path(self.input_video.filename).stem

    def get_output_name(self, batch_no=None):
        if batch_no is None:
            filename = f'{self.get_base_output_name()}.pdf'
        else:
            filename = f'{self.get_base_output_name()}.{str(batch_no)}.pdf'
        return Path(self.output_dir).joinpath(Path(filename))

    def add_watermark_to_img(self, img, watermark_text):
        # https://www.tutorialspoint.com/python_pillow/python_pillow_creating_a_watermark.htm
        draw = ImageDraw.Draw(img)
        font_size = 50
        font = ImageFont.truetype(FlipbookConstants.Font.DEFAULT, font_size)
        text_color = (255, 255, 255)
        text_width, text_height = draw.textsize(watermark_text, font)

        # Position at bottom left-hand corner of the image
        position = (self.pad(), self.frame_height() - text_height - self.pad())
        draw.text(position, watermark_text, font=font, fill=text_color)


    def write_tiled_batch(self, frames, batch_no):
        # Get file name for batch
        batch_filename = self.get_output_name(batch_no)

        # https://stackoverflow.com/questions/37921295/python-pil-image-make-3x3-grid-from-sequence-images
        grid = Image.new('RGB', (self.grid_width(), self.grid_height()), (255, 255, 255, 255))

        for frame_no, frame in enumerate(frames):
            row = frame_no // self.output_format.ncols
            col = frame_no % self.output_format.nrows

            # https://stackoverflow.com/questions/10965417/how-to-convert-a-numpy-array-to-pil-image-applying-matplotlib-colormap
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame.astype('uint8'),'RGB')

            self.add_watermark_to_img(img, str(frame_no + batch_no * len(frames) + 1))

            offset_width = int((self.frame_width() + 2 * self.pad() + self.left_pad()) * col + self.pad() + self.left_pad())
            offset_height = int((self.frame_height() + 2 * self.pad()) * row + self.pad())
            grid.paste(img, (offset_width, offset_height))
            draw = ImageDraw.Draw(grid)

            # draw vertical and horizontal lines at end of each frame
            end_of_width = offset_width + self.frame_width() + self.pad()
            end_of_height = offset_height + self.frame_height() + self.pad()
            draw.line((end_of_width, 0, end_of_width, end_of_height), fill=0, width=2)
            draw.line((0, end_of_height, end_of_width, end_of_height), fill=0, width=2)

        grid.save(batch_filename)

    def write_output_pdfs(self, frames):
        # total number of images per page
        num_per_page = self.output_format.nrows * self.output_format.ncols

        # number of pages to write
        num_pages_to_print = ceil(self.n_flipbook_frames/num_per_page)
        print(f'Num pages: {num_pages_to_print}')

        for batch_no in tqdm(
                range(num_pages_to_print),
                total=num_pages_to_print,
                desc=f'Writing output to {self.output_dir}/'
            ):
            # Get subset of frames for the batch
            frames_in_batch = frames[batch_no * num_per_page: (batch_no + 1) * num_per_page]
            self.write_tiled_batch(frames_in_batch, batch_no)

        print()
        return [self.get_output_name(batch_no) for batch_no in range(num_pages_to_print)]

    def combine_pdfs(self, output_frames):
        output_file_name = self.get_output_name(None)
        merger = PdfWriter()
        for page in output_frames:
            merger.append(page)

        merger.write(output_file_name)
        merger.close()
        for page in output_frames:
            os.remove(page)
        print(f'\nWrote {output_file_name}\n\n')

    def write_output(self, frames):
        output_frames = self.write_output_pdfs(frames)
        self.combine_pdfs(output_frames)

    def run(self):
        # Read the video and extract the frames
        frames = self.extract_frames()

        # Write the PDFs to output files
        self.write_output(frames)
