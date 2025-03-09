from typing import List, Optional

import cv2
from tqdm import tqdm

from src.media.canvas import Canvas
from src.core.frame import Frame
from src.core.video_source import VideoSource
from src.core.flipbook_output import FlipbookOutput
from src.core.flipbook_printer import FlipbookPrinter

class Flipbook:
    def __init__(self,
                 video_source: VideoSource,
                 flipbook_output: FlipbookOutput,
                 video_capture: Optional[cv2.VideoCapture] = None
                 ) -> None:
        '''
        Initializes the Flipbook object.

        :param video_source: VideoSource object containing input video info
        :param flipbook_output: FlipbookOutput object containing output flipbook params
        :param video_capture: Optional cv2.VideoCapture object for injecting in tests
        '''
        self.video_source = video_source
        self.flipbook_output = flipbook_output
        self.video_capture = video_capture  # Allows injecting a mock or fake capture source

        # Initialize self.frames (to be updated later)
        self.frames: List[Frame] = []

    @property
    def input_file(self):
        # input file name of video source
        return self.video_source.filename

    @property
    def base_name(self) -> str:
        # Base name for output files
        return self.video_source.get_base_name()

    @property
    def input_frame_rate(self) -> float:
        # frame rate of input video source
        return self.video_source.frame_rate

    @property
    def output_frame_rate(self) -> float:
        # frame rate of extracted frames
        return self.flipbook_output.frame_rate

    def capture_frame(self, cam, index_in) -> Optional:
        """
        Captures a frame from the video stream.

        :param cam: The video capture object.
        :param index_in: The index of the frame being captured.
        :return: The frame data if successful, otherwise None.
        """
        success = cam.grab()
        if not success:
            return None

        success, data = cam.retrieve()
        if not success:
            return None

        return data

    def video_frame_source(self, cam):
        """
        Extract raw video frames from an OpenCV capture object.

        :param cam: The cv2.VideoCapture object.
        :return: list of raw frame data.
        """
        frame_data = []
        for frame_no, index_in in enumerate(tqdm(range(self.video_source.total_frames))):
            data = self.capture_frame(cam, index_in)
            if data is None:
                break
            frame_data.append(data)
        if frame_no < self.video_source.total_frames:
            print(f"   ...Stopping extraction at frame {frame_no}.")
        print(f'   ...Done extracting frames.\n\n')
        return frame_data

    def process_frame(self, data, cur_frame_no, canvas) -> Frame:
        '''
        Processes a frame and returns a Frame object.

        :param data: The raw frame data from the video.
        :param cur_frame_no: The current frame number in sequence.
        :param canvas: The canvas object for resizing.
        :return: A processed Frame object.
        '''
        return Frame(data, cur_frame_no, self.flipbook_output, canvas)

    def frame_generator(self, frame_data):
        """
        Generator that yields extracted frames.

        :param frame_source: list of video frame source data.
        :yield: Processed Frame objects.
        """
        canvas = Canvas(self.video_source.aspect, self.flipbook_output.canvas_res)
        frame_interval = self.video_source.frame_rate / self.flipbook_output.frame_rate
        cur_frame_no = 0
        next_capture_frame = 0

        for index_in, data in enumerate(frame_data):
            if index_in >= next_capture_frame:
                yield self.process_frame(data, cur_frame_no, canvas)
                cur_frame_no += 1
                next_capture_frame += frame_interval

    def print_info(self):
        print('----------------------------')
        print('Input Video Info')
        print('----------------------------')
        self.video_source.print_info()
        print('\n----------------------------')
        print('Output Flipbook Format')
        print('----------------------------')
        self.flipbook_output.print_info()
        print('\n')
        print((f'Extracting frames from {self.video_source.filename} '
               f'at {self.flipbook_output.frame_rate} FPS'))


    def extract_frames(self) -> None:
        """
        Extracts frames from the input video at the specified output frame rate.
        """
        self.print_info()

        cam = self.video_capture or cv2.VideoCapture(self.video_source.filename)
        if not cam.isOpened():
            raise RuntimeError(f"Failed to open video file: {self.video_source.filename}")

        # expected number of frames after resampling
        output_frames = round(self.video_source.total_frames * self.output_frame_rate / self.input_frame_rate)
        self.frames.clear()
        for frame in self.frame_generator(self.video_frame_source(cam)):
            self.frames.append(frame)

        cam.release()
        cv2.destroyAllWindows()

    def save(self,
             paper_type: str,
             dpi: int,
             output_dir: str) -> None:
        '''
        Saves the extracted frames into a flipbook-style PDF.

        :param paper_type: The type of paper for printing.
        :param dpi: The print resolution in dots per inch.
        :param output_dir: The directory where the output should be saved.
        '''
        if not self.frames:
            raise ValueError("No frames extracted. Run extract_frames() before saving.")

        print(f"Saving printable flipbook to {output_dir} with paper type {paper_type} at {dpi} DPI.")

        printer = FlipbookPrinter(
            self.frames,
            self.flipbook_output,
            paper_type,
            dpi,
            output_dir,
            self.base_name
        )

        printer.save()








