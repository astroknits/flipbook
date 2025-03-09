from pathlib import Path
import cv2
from src.helpers.flipbook_constants import FlipbookConstants


class VideoSource:
    '''
    Class representing an input video file.
    Handles file validation and metadata extraction.
    '''
    def __init__(self, filename: str) -> None:
        '''
        Validate existence of the input video file and check format.
        Also gathers metadata from input video

        :param filename: Path to the input video file.
        '''
        self.filename = self.validate_video_file(filename)

        '''
        Read the video properties
        See opencv docs page for more info
        https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html
        '''
        cam = cv2.VideoCapture(self.filename)
        if not cam.isOpened():
            raise RuntimeError(f"Failed to open video file: {self.filename}")

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

    def validate_video_file(self, filename: str) -> Path:
        '''
        Validates that the file exists and is of a supported format.

        :param filename: Path to the input video file.
        :raises FileNotFoundError: If the file does not exist.
        :raises ValueError: If the file type is not supported.
        :return: The validated file path as a Path object.
        '''
        filepath = Path(filename)
        if not filepath.exists():
            raise FileNotFoundError(f'Video file not found: {filename}')
        if filepath.suffix.strip('.') not in FlipbookConstants.Video.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported video format '{filepath.suffix}'. "
                f"Supported formats: {FlipbookConstants.Video.SUPPORTED_FORMATS}")
        return filename

    @property
    def aspect(self) -> float:
        # aspect ratio of the source video file
        return float(self.height)/float(self.width)

    def get_base_name(self) -> str:
        '''
        Base file name is based on input file name
        '''
        return Path(self.filename).stem

    def print_info(self) -> None:
        print(f'Input file: {self.filename}')
        print(f'Resolution: {self.width}x{self.height}')
        print(f'Frame rate: {self.frame_rate:.2f} fps')


