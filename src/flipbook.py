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

    def grid_width(self):
        return self.output.paper_type.value.xres()

    def grid_height(self):
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

        # Input and output frame rates
        fps_in = self.input.frame_rate
        fps_out = self.output.frame_rate

        # Open the file and open stream
        cam = cv2.VideoCapture(self.input.filename)

        # Cycle through the frames
        index_out = 0
        frames = []
        for index_in in range(self.input.total_frames):
            # Read the frame
            success, frame = cam.read()

            if not success:
                # Before breaking, update with the accurate number of frames
                self.input.total_frames = index_in
                break

            # otherwise we process the frame
            out_due = int(index_in / fps_in * fps_out)
            if out_due > index_out:
                success, frame = cam.retrieve()
                if not success:
                    # Before breaking, update with the accurate number of frames
                    self.input.total_frames = index_in
                    break
                # otherwise we process the frame
                frames.append(Frame(frame, index_out, self.input, self.output))
                index_out += 1

        self.n_flipbook_frames = index_out
        cam.release()
        cv2.destroyAllWindows()
        return frames

    def get_base_output_name(self):
        '''
        Base file name is based on input file name
        '''
        return Path(self.input.filename).stem

    def get_output_name(self, batch_no=None):
        if batch_no is None:
            filename = f'{self.get_base_output_name()}.pdf'
        else:
            filename = f'{self.get_base_output_name()}.{str(batch_no)}.pdf'
        return Path(self.output_dir).joinpath(Path(filename))


    def write_tiled_batch(self, frames, batch_no):
        # Get file name for batch
        batch_filename = self.get_output_name(batch_no)

        # https://stackoverflow.com/questions/37921295/python-pil-image-make-3x3-grid-from-sequence-images
        grid = Image.new('RGB', (self.grid_width(), self.grid_height()), (255, 255, 255, 255))

        for frame in frames:
            img = frame.get_frame()
            offset = frame.get_offset() # tuple wxh
            grid.paste(img, offset)

        grid.save(batch_filename)

    def write_output_pdfs(self, frames):
        # total number of images per page
        num_per_page = self.output.frames_per_page()

        # number of pages to write
        num_pages_to_print = ceil(self.n_flipbook_frames/num_per_page)

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
