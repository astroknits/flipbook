import os
from pathlib import Path
from math import ceil
from tqdm import tqdm
import cv2
from PIL import Image
from pypdf import PdfWriter

from src.frame import Frame
from src.input import Input
from src.output import Output
from src.page import Page
from src.paper_type import PaperType


class Flipbook:
    '''
    Class to create frames for flipbook from video file
    '''

    def __init__(
            self,
            filename,
            output_dir,
            output_width=5,
            output_height=3,
            output_frame_rate=0,
            paper_type='letter',
             ):

        # output_width, output_height in inches

        # output directory for output for flipbook
        self.output_dir = output_dir

        self.input = Input(filename)
        self.output = Output(
            output_width,
            output_height,
            output_frame_rate,
            PaperType.get(paper_type),
        )

        self.n_flipbook_frames = None

    def print_info(self):
        print('\n\n----------------------------')
        print(f'Input Video Info')
        print('----------------------------')
        self.input.print()
        print('\n----------------------------')
        print(f'Output Formatting Info')
        print('----------------------------')
        self.output.print()
        print('----------------------------\n\n')

    def page_xres(self):
        return self.output.paper_type.value.xres()

    def page_yres(self):
        return self.output.paper_type.value.yres()

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
        # Create a directory for the extracted frames
        self.create_output_dir()

        # extract the frames from the input video
        frames = self.input.extract_frames(self.output.frame_rate)

        self.n_flipbook_frames = len(frames)

        return frames

    def get_base_output_name(self):
        '''
        Base file name is based on input file name
        '''
        return Path(self.input.filename).stem

    def get_output_name(self, page_no=None):
        if page_no is None:
            filename = f'{self.get_base_output_name()}.pdf'
        else:
            filename = f'{self.get_base_output_name()}.{str(page_no)}.pdf'
        return Path(self.output_dir).joinpath(Path(filename))

    def write_page(self, frames, page_no):
        # Get file name for batch
        page_filename = self.get_output_name(page_no)

        grid = Image.new('RGB', (self.page_xres(), self.page_yres()), 'white')

        for (frame_no, data) in frames:
            frame = Frame(
                data,
                frame_no,
                self.input.width,
                self.input.height,
                self.output.xres(),
                self.output.yres(),
            )
            img = frame.get_frame()
            offset = self.output.get_offset(frame_no) # tuple wxh
            grid.paste(img, offset)

        grid.save(page_filename)

    def write_output_pdfs(self, frames):
        # total number of images per page
        num_per_page = self.output.frames_per_page()

        # number of pages to write
        num_pages_to_print = ceil(self.n_flipbook_frames/num_per_page)

        for page_no in tqdm(
                range(num_pages_to_print),
                total=num_pages_to_print,
                desc=f'Writing output to {self.output_dir}/'
            ):
            # Get subset of frames for the batch
            frames_in_batch = frames[page_no * num_per_page: (page_no + 1) * num_per_page]
            self.write_page(frames_in_batch, page_no)

        print()
        return [self.get_output_name(page_no) for page_no in range(num_pages_to_print)]

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
