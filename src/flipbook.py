from typing import List

import cv2

from src.frame import Frame
from src.input import Input
from src.output import Output
from src.flipbook_printer import FlipbookPrinter

class Flipbook:
    def __init__(self,
                 input_file: str,
                 output_fps: int,
                 output_width: int,
                 output_height: int,
                 frame_border_padding: int = 50,
                 frame_left_padding: int = 260,
                 frame_border_line_width: int = 3) -> None:
        '''
        Initializes the Flipbook object.

        :param input_file: Path to the input video file.
        :param output_fps: Frames per second for the output.
        :param output_width: Width of each output frame.
        :param output_height: Height of each output frame.
        :param frame_border_padding: Padding around frames (default: 50).
        :param frame_left_padding: Left padding for frames (default: 260)
        :param frame_border_line_width: border line width for frames (default: 3)
        '''
        # instantiate Input object with input video path and metadata
        self.input = Input(input_file)

        # instantiate Output object with output frame parameters
        self.output = Output(
            output_fps,
            output_width,
            output_height,
            frame_border_padding,
            frame_left_padding,
            frame_border_line_width
        )

        # Initialize self.frames (to be updated later)
        self.frames: List[Frame] = []

    @property
    def base_name(self) -> str:
        # Base name for output files
        return self.input.get_base_name()

    def extract_frames(self):
        '''
        Extracts frames from the input video at the specified
        output frame rate.
        The extracted frames are stored in self.frames.
        '''

        # Input and output frame rates
        fps_in = self.input.frame_rate
        fps_out = self.output.frame_rate

        # Open the file and open stream
        cam = cv2.VideoCapture(self.input.filename)
        if not cam.isOpened():
            raise RuntimeError(f"Failed to open video file: {self.input.filename}")

        frame_interval = fps_in / fps_out  # Interval between frames to extract
        print(f"Extracting frames from {self.input.filename} at {fps_out} FPS")

        # Cycle through the frames
        self.frames.clear()
        n_flipbook_frames = 0
        next_capture_frame = 0 # the next frame index to capture

        for index_in in range(self.input.total_frames):
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
                              n_flipbook_frames,
                              self.input.width,
                              self.input.height,
                              self.output.frame_output_width,
                              self.output.frame_output_height,
                              self.output.frame_border_padding,
                              self.output.frame_left_padding,
                              self.output.frame_border_line_width)
                self.frames.append(frame)
                n_flipbook_frames += 1
                # The index of the next frame to capture based on output FPS
                next_capture_frame += frame_interval

        self.input.total_frames = n_flipbook_frames
        cam.release()
        cv2.destroyAllWindows()

    def save(self, paper_type, dpi, output_dir):
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
            self.output,
            paper_type,
            dpi,
            output_dir,
            self.base_name
        )

        printer.save()








