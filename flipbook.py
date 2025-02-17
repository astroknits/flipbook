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
    args = parser.parse_args()
    return args


class Flipbook:
    '''
    Class to create frames for flipbook from video file
    '''
    SUPPORTED_VIDEO_FORMATS = ['mov', 'mp4']
    FRAME_BASE_NAME = 'video_frame'

    def __init__(self, filename, output_dir, output_base_name=None):
        # video file name
        self.filename = self.validate_video_file(filename)

        # output directory for output for flipbook
        self.output_dir = output_dir

        # base name for output files for flipbook
        # (default -> same base as the input video)
        self.output_base_name = self.validate_base_name(output_base_name)

        # Initialize list of frame paths
        self.frames = []

    def validate_video_file(self, filename):
        '''
        Check that the file provided exists on disk
        Raise exception if it doesn't exist, otherwise return True
        '''
        filepath = Path(filename)
        if not filepath.exists():
            print('file not found')
            raise FileNotFoundError(f'Video file provided does not exist: {filename}')
        if filepath.suffix not in self.SUPPORTED_VIDEO_FORMATS:
            print(f'Video file type {filepath.suffix} not supported (not one of {self.SUPPORTED_VIDEO_FORMATS})')
        return filename

    def validate_base_name(self, output_base_name):
        if output_base_name is not None:
            return output_base_name
        return Path(self.filename).stem

    def create_data_dir(self):
        output_dir_path = Path(self.output_dir)
        if Path.exists(output_dir_path):
            if output_dir_path.is_dir():
                return True
            raise Exception(f'Expected data output directory path {self.data_dir} exists but is not a directory.')
        # If the data_dir does not exist, crate it
        output_dir_path.mkdir()
        del output_dir_path
        return True

    def get_frame_jpg_name(self, frame_no):
        return Path(self.output_dir).joinpath(Path(f'{self.FRAME_BASE_NAME}.{str(frame_no)}.jpg'))

    def get_frame_pdf_name(self, frame_no):
        return Path(self.output_dir).joinpath(Path(f'{self.FRAME_BASE_NAME}.{str(frame_no)}.pdf'))

    def get_frames_to_process(self, frame_rate):
        '''
        Will effectively be downsampling the video frame rate
        by only processing one of every X frames.
        '''
        if frame_rate >= 30:
            # keep every 10th frame
            return 10
        elif frame_rate >= 20:
            # keep every 8th frame
            return 8
        else:
            # keep every 3rd frame
            return 3

    def create_frames(self):
        # from https://www.geeksforgeeks.org/extract-images-from-video-in-python/

        # Open the file and open stream
        cam = cv2.VideoCapture(self.filename)

        frame_rate = cam.get(cv2.CAP_PROP_FPS)
        print(f'frame rate: {frame_rate} frames per second')
        print(f'')
        to_process = self.get_frames_to_process(frame_rate)
        print(f'Processing one for every {to_process} frames')

        # Create a directory for the extracted frames
        self.create_data_dir()

        # Cycle through the frames
        frame_no = 0
        self.frames = []
        while(True):
            # Read the frame
            frame_exists, frame = cam.read()

            if not frame_exists:
                # if there is no more frame being returned, we've hit the end
                # of the frames with none left to process
                break

            # otherwise we process the frame
            if frame_no % to_process == 0:
                jpg_name = self.get_frame_jpg_name(frame_no)
                print(f'Creating {jpg_name}')

                # Write out the extracted jpg image
                cv2.imwrite(jpg_name, frame)

                image = Image.open(jpg_name)
                size = image.size

                name = self.get_frame_pdf_name(frame_no)
                print(f'Creating {name}')

                # Write out the extracted pdf image
                image.save(name, 'PDF', resolution=100.0)
                image.close()

                os.remove(jpg_name)
                self.frames.append(name)
            frame_no += 1

        print(f'Extracted {frame_no} frames from {self.filename}')
        cam.release()
        cv2.destroyAllWindows()

    def get_output_name(self, batch_no):
        return Path(self.output_dir).joinpath(Path(f'{self.output_base_name}.{str(batch_no)}.pdf'))

    def write_pdf(self, frames, pdf_name):
        pdf_merger = PyPDF2.PdfMerger()
        for frame in frames:
            pdf_merger.append(frame)
        pdf_merger.write(pdf_name)
        pdf_merger.close()
        for frame in frames:
            os.remove(frame)

    def write_pdfs(self, num_per_page=9):
        num_pages = ceil(len(self.frames)/num_per_page)
        print(f'Num pages: {num_pages}')
        for batch_no in range(num_pages):
            batch = self.frames[batch_no * num_per_page: (batch_no + 1) * num_per_page]
            batch_name = self.get_output_name(batch_no)
            print(f'Writing {batch_name}')
            self.write_pdf(batch, batch_name)


def main():
    # Parse command line arguments
    args = parse_args()

    # Get the vide file name from the command line arguments
    filename = args.filename

    # Get output directory from command line args
    output_dir = args.output_dir

    flipbook = Flipbook(filename, output_dir, output_base_name=None)

    # Read the video and extract the frames
    flipbook.create_frames()

    # Write the PDFs to output files
    flipbook.write_pdfs()


if __name__ == '__main__':
    main()