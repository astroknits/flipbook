import os
from pathlib import Path
from math import ceil
from argparse import ArgumentParser
import cv2
from PIL import Image
import PyPDF2

def parse_args():
    '''
    Parse command line arguments using argparse
    '''
    parser = ArgumentParser()
    parser.add_argument('filename', help='Path of the video file to use')
    parser.add_argument('output_dir', help='Directory to write output')
    parser.add_argument('output_base_name', nargs='?', default=None,
                        help=('Base name for output PDF files '
                              '(default None -> use stem of the input video file)'))
    args = parser.parse_args()
    return args

class InputVideo:
    SUPPORTED_VIDEO_FORMATS = ['mov', 'mp4']

    def __init__(self, filename):
        self.filename = self.validate_video_file(filename)
        self.get_video_metadata()

    def print(self):
        print(f'Input file: {self.filename}')
        print(f'Resolution: {self.get_resolution()}')
        print(f'Frame rate: {self.frame_rate:.2f} fps')

    def validate_video_file(self, filename):
        '''
        Check that the file provided exists on disk
        Raise exception if it doesn't exist, otherwise return True
        '''
        filepath = Path(filename)
        if not filepath.exists():
            print('file not found')
            raise FileNotFoundError(f'Video file provided does not exist: {filename}')
        if filepath.suffix.strip('.') not in self.SUPPORTED_VIDEO_FORMATS:
            msg = f'Video file type {filepath.suffix} not supported (not one of {self.SUPPORTED_VIDEO_FORMATS})'
            raise Exception(msg)
        return filename

    def get_resolution(self):
        return f'{self.width}x{self.height}'

    def get_video_metadata(self):
        # Open the file and open stream
        cam = cv2.VideoCapture(self.filename)

        self.frame_rate = cam.get(cv2.CAP_PROP_FPS)
        self.width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))

        cam.release()
        cv2.destroyAllWindows()

class OutputFormat:
    def __init__(self, ncols, nrows, frame_rate):
        self.ncols = ncols
        self.nrows = nrows
        self.frame_rate = frame_rate

    def print(self):
        print(f'ncols: {self.ncols}')
        print(f'nrows: {self.nrows}')
        print(f'Frame rate: {self.frame_rate:.2f} fps')


class Flipbook:
    '''
    Class to create frames for flipbook from video file
    '''
    FRAME_BASE_NAME = 'video_frame'

    def __init__(self, filename, output_dir, output_base_name=None, ncols=3, nrows=3, output_frame_rate=0):
        # video file name
        self.input_video = InputVideo(filename)
        self.output_format = OutputFormat(nrows, ncols, output_frame_rate)

        # output directory for output for flipbook
        self.output_dir = output_dir

        # base name for output files for flipbook
        # (default -> same base as the input video)
        self.output_base_name = self.validate_base_name(output_base_name)

        self.to_process = self.get_frames_to_process()

        # Initialize number of frames in flipbook
        self.n_flipbook_frames = self.input_video.total_frames // self.to_process

    def print_info(self):
        print('\n\n----------------------------')
        print(f'Input Video Info')
        print('----------------------------')
        self.input_video.print()
        print('\n----------------------------')
        print(f'Output Formatting Info')
        print('----------------------------')
        self.output_format.print()
        print('\n----------------------------\n\n')


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

    def get_frames_to_process(self):
        '''
        Will effectively be downsampling the video frame rate
        by only processing one of every X frames.

        TODO: add better logic to determine what this value should be
              instead of the current ad hoc logic
        '''
        frame_rate = self.input_video.frame_rate
        if frame_rate >= 30:
            # keep every 10th frame
            return 10
        elif frame_rate >= 20:
            # keep every 8th frame
            return 8
        else:
            # keep every 3rd frame
            return 3

    def extract_frames(self):
        # from https://www.geeksforgeeks.org/extract-images-from-video-in-python/

        # Open the file and open stream
        cam = cv2.VideoCapture(self.input_video.filename)

        # Create a directory for the extracted frames
        self.create_data_dir()

        # Cycle through the frames
        self.cur_flipbook_frame = 0
        self.frames = []
        for cur_video_frame in range(self.input_video.total_frames):
            # Read the frame
            frame_exists, frame = cam.read()

            if not frame_exists:
                # if there is no more frame being returned, we've hit the end
                # of the frames with none left to process
                # Before breaking, update with the accurate number of frames
                self.n_flipbook_frames = self.cur_flipbook_frame
                self.input_video.total_frames = cur_video_frame
                break

            # otherwise we process the frame
            if cur_video_frame % self.to_process == 0:
                self.frames.append(frame)
                self.cur_flipbook_frame += 1
            cur_video_frame += 1

        cam.release()
        cv2.destroyAllWindows()

    def get_output_name(self, batch_no):
        return Path(self.output_dir).joinpath(Path(f'{self.output_base_name}.{str(batch_no)}.pdf'))

    def write_tiled_batch(self, frames, batch_no):
        # Get file name for batch
        batch_filename = self.get_output_name(batch_no)
        print(f'Writing {batch_filename}')
        for i, frame in enumerate(frames):
            pass

    def write_output(self):
        # total number of images per page
        num_per_page = self.output_format.nrows * self.output_format.ncols

        # number of pages to write
        num_pages_to_print = ceil(self.n_flipbook_frames/num_per_page)
        print(f'Num pages: {num_pages_to_print}')

        for batch_no in range(num_pages_to_print):
            # Get subarray of frames
            frames_batch = self.frames[batch_no * num_per_page: (batch_no + 1) * num_per_page]
            self.write_tiled_batch(frames_batch, batch_no)

    def run(self):
        # Read the video and extract the frames
        self.extract_frames()

        # Write the PDFs to output files
        self.write_output()


def main():
    # Parse command line arguments
    args = parse_args()

    # Get the vide file name from the command line arguments
    filename = args.filename

    # Get output directory from command line args
    output_dir = args.output_dir

    # Get base name for output PDF files
    output_base_name = args.output_base_name

    flipbook = Flipbook(filename, output_dir, output_base_name=output_base_name)
    flipbook.print_info()

    flipbook.run()


if __name__ == '__main__':
    main()