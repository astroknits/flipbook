from pathlib import Path
from math import ceil
from tqdm import tqdm
import numpy as np
import cv2
from PIL import Image
from input_video import InputVideo
from output_format import OutputFormat
from output_format import PaperFormat


class Flipbook:
    '''
    Class to create frames for flipbook from video file
    '''
    FRAME_BASE_NAME = 'video_frame'

    def __init__(self, filename, output_dir, output_base_name=None, ncols=3, nrows=3, output_frame_rate=0):
        # video file name
        self.n_flipbook_frames = None
        self.input_video = InputVideo(filename)
        self.output_format = OutputFormat(nrows, ncols, output_frame_rate, PaperFormat.LETTER)

        # output directory for output for flipbook
        self.output_dir = output_dir

        # base name for output files for flipbook
        # (default -> same base as the input video)
        self.output_base_name = self.validate_base_name(output_base_name)

        # Initialize number of frames in flipbook
        # self.n_flipbook_frames = self.input_video.total_frames // self.to_process

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


    def validate_base_name(self, output_base_name):
        if output_base_name is not None:
            return output_base_name
        return Path(self.input_video.filename).stem

    def create_data_dir(self):
        output_dir_path = Path(self.output_dir)
        if Path.exists(output_dir_path):
            if output_dir_path.is_dir():
                return True
            raise Exception(f'Expected data output directory path {self.output_dir} exists but is not a directory.')
        # If the data_dir does not exist, crate it
        output_dir_path.mkdir()
        del output_dir_path
        return True

    def get_frame_jpg_name(self, frame_no):
        return Path(self.output_dir).joinpath(Path(f'{self.FRAME_BASE_NAME}.{str(frame_no)}.jpg'))

    def get_frame_pdf_name(self, frame_no):
        return Path(self.output_dir).joinpath(Path(f'{self.FRAME_BASE_NAME}.{str(frame_no)}.pdf'))

    def extract_frames(self):
        # Input and output frame rates
        fps_in = self.input_video.frame_rate
        fps_out = self.output_format.frame_rate

        # Open the file and open stream
        cam = cv2.VideoCapture(self.input_video.filename)

        # Create a directory for the extracted frames
        self.create_data_dir()

        # Cycle through the frames
        index_out = 0
        self.frames = []
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
                self.frames.append(frame)
                index_out += 1

        self.n_flipbook_frames = index_out
        cam.release()
        cv2.destroyAllWindows()

    def get_output_name(self, batch_no):
        return Path(self.output_dir).joinpath(Path(f'{self.output_base_name}.{str(batch_no)}.pdf'))

    def write_tiled_batch(self, frames, batch_no):
        # Get file name for batch
        batch_filename = self.get_output_name(batch_no)

        # https://stackoverflow.com/questions/37921295/python-pil-image-make-3x3-grid-from-sequence-images
        grid = Image.new('RGB', (self.grid_width(), self.grid_height()), (255, 255, 255, 255))

        for frame_no, frame in enumerate(frames):
            row = frame_no // self.output_format.ncols
            col = frame_no % self.output_format.nrows
            # https://stackoverflow.com/questions/10965417/how-to-convert-a-numpy-array-to-pil-image-applying-matplotlib-colormap
            img = Image.fromarray(frame.astype('uint8'),'RGB')
            offset_width = int((self.frame_width() + 2 * self.pad()) * col + self.pad())
            offset_height = int((self.frame_height() + 2 * self.pad()) * row + self.pad())
            grid.paste(img, (offset_width, offset_height))
        grid.save(batch_filename)

    def pad(self):
        return self.output_format.frame_border_padding

    def frame_width(self):
        return self.input_video.width

    def frame_height(self):
        return self.input_video.height

    def ncols(self):
        return self.output_format.ncols

    def nrows(self):
        return self.output_format.nrows

    def grid_width(self):
        return int((self.frame_width() + 2 * self.pad()) * self.ncols())

    def grid_height(self):
        return int((self.frame_height() + 2 * self.pad()) * self.nrows())

    def write_output(self):
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
            frames_in_batch = self.frames[batch_no * num_per_page: (batch_no + 1) * num_per_page]
            self.write_tiled_batch(frames_in_batch, batch_no)
        del self.frames
        filenames = '\n'.join([str(self.get_output_name(batch_no)) for batch_no in range(num_pages_to_print)])
        print(f'\n\nWrote the following pages:\n{filenames}')

    def run(self):
        # Read the video and extract the frames
        self.extract_frames()

        # Write the PDFs to output files
        self.write_output()
