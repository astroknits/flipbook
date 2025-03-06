from typing import List

import cv2

from src.frame import Frame
from src.video_source import VideoSource
from src.flipbook_output import FlipbookOutput
from src.flipbook_printer import FlipbookPrinter

class Flipbook:
    def __init__(self,
                 video_source: VideoSource,
                 flipbook_output: FlipbookOutput
                 ) -> None:
        '''
        Initializes the Flipbook object.

        :param video_source: VideoSource object containing input video info
        :param flipbook_output: FlipbookOutput object containing output flipbook params
        '''
        self.video_source = video_source
        self.flipbook_output = flipbook_output

        # Initialize self.frames (to be updated later)
        self.frames: List[Frame] = []

    @property
    def input_file(self):
        return self.video_source.filename

    @property
    def base_name(self) -> str:
        # Base name for output files
        return self.video_source.get_base_name()

    def extract_frames(self) -> None:
        '''
        Extracts frames from the input video at the specified
        output frame rate.
        The extracted frames are stored in self.frames.
        '''
        # Input and output frame rates
        fps_in = self.video_source.frame_rate
        fps_out = self.flipbook_output.frame_rate

        # Open the file and open stream
        cam = cv2.VideoCapture(self.input_file)
        if not cam.isOpened():
            raise RuntimeError(f"Failed to open video file: {self.input_file}")

        frame_interval = fps_in / fps_out  # Interval between frames to extract
        print(f"Extracting frames from {self.input_file} at {fps_out} FPS")

        # Cycle through the frames
        self.frames.clear()
        cur_frame_no = 0
        next_capture_frame = 0 # the next frame index to capture

        for index_in in range(self.video_source.total_frames):
            # Read the frame
            success = cam.grab()

            if not success:
                print(f"Frame {index_in} could not be retrieved. Stopping extraction.")
                break

            if index_in >= next_capture_frame:
                success, data = cam.retrieve()
                if not success:
                    print(f"Frame {index_in} could not be retrieved. Stopping extraction.")
                    break
                # otherwise we process the frame
                frame = Frame(data,
                              cur_frame_no,
                              self.video_source,
                              self.flipbook_output)
                self.frames.append(frame)
                cur_frame_no += 1
                # The index of the next frame to capture based on output FPS
                next_capture_frame += frame_interval

        self.video_source.total_frames = cur_frame_no
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








