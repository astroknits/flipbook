from typing import List, Optional

import cv2

from src.canvas import Canvas
from src.frame import Frame
from src.video_source import VideoSource
from src.flipbook_output import FlipbookOutput
from src.flipbook_printer import FlipbookPrinter

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
            print(f"Frame {index_in} could not be retrieved. Stopping extraction.")
            return None

        success, data = cam.retrieve()
        if not success:
            print(f"Frame {index_in} could not be retrieved. Stopping extraction.")
            return None

        return data

    def video_frame_source(self, cam):
        """
        Extract raw video frames from an OpenCV capture object.

        :param cam: The cv2.VideoCapture object.
        :return: list of raw frame data.
        """
        frame_data = []
        for index_in in range(self.video_source.total_frames):
            data = self.capture_frame(cam, index_in)
            if data is None:
                break
            frame_data.append(data)
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

    def extract_frames(self) -> None:
        """
        Extracts frames from the input video at the specified output frame rate.
        """
        print((f"Extracting frames from {self.video_source.filename} '"
               f"'at {self.flipbook_output.frame_rate} FPS"))

        cam = self.video_capture or cv2.VideoCapture(self.video_source.filename)
        if not cam.isOpened():
            raise RuntimeError(f"Failed to open video file: {self.video_source.filename}")

        self.frames.clear()
        for frame in self.frame_generator(self.video_frame_source(cam)):
            self.frames.append(frame)

        self.video_source.total_frames = len(self.frames)
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

        print(f"Saving flipbook to {output_dir} with paper type {paper_type} at {dpi} DPI.")

        printer = FlipbookPrinter(
            self.frames,
            self.flipbook_output,
            paper_type,
            dpi,
            output_dir,
            self.base_name
        )

        printer.save()








