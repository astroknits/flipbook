from pathlib import Path
import cv2
from src.flipbook_constants import FlipbookConstants


class Input:
    '''
    Class owning info about the input video file
    including file validation and metadata gathering
    '''
    def __init__(self, filename):
        '''
        Validate existence of input video file and check format.
        Also gather metadata from input video
        '''
        self.filename = self.validate_video_file(filename)

        '''
        Read the video properties
        See opencv docs page for more info
        https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html
        '''
        cam = cv2.VideoCapture(self.filename)

        # Video frame rate in frames per second
        self.frame_rate = cam.get(cv2.CAP_PROP_FPS)

        # Video width in pixels
        self.width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)

        # Height of the frames in the video stream (in pixels)
        self.height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Total number of frames in the video file
        self.total_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))

        cam.release()
        cv2.destroyAllWindows()

    def aspect(self):
        return self.height/self.width

    def validate_video_file(self, filename):
        '''
        Check that the file provided exists on disk
        Raise exception if it doesn't exist, otherwise return True
        '''
        filepath = Path(filename)
        if not filepath.exists():
            print('file not found')
            raise FileNotFoundError(f'Video file provided does not exist: {filename}')
        if filepath.suffix.strip('.') not in FlipbookConstants.Video.SUPPORTED_FORMATS:
            msg = (f'Video file type {filepath.suffix} not supported '
                   f'(not one of {FlipbookConstants.Video.SUPPORTED_FORMATS})')
            raise Exception(msg)
        return filename

    def get_resolution(self):
        '''
        Simple helper function to return wxh resolution
        '''
        return f'{self.width}x{self.height}'

    def print(self):
        print(f'Input file: {self.filename}')
        print(f'Resolution: {self.get_resolution()}')
        print(f'Frame rate: {self.frame_rate:.2f} fps')


