
import cv2

from src.frame import Frame
from src.input import Input
from src.output import Output
from src.flipbook_printer import FlipbookPrinter

class Flipbook:
    def __init__(self,
                 input_file,
                 output_fps,
                 output_width,
                 output_height,
                 frame_border_padding=50,
                 frame_left_padding=260):
        self.input = Input(input_file)
        self.base_name = self.input.get_base_name()
        self.output = Output(output_fps, output_width, output_height, frame_border_padding, frame_left_padding)
        self.n_flipbook_frames = None
        self.frames = None

    def extract_frames(self):
        '''
        Step through the input video frames and extract
        at the desired output frame rate, saving as
        self.frames
        '''

        # Input and output frame rates
        fps_in = self.input.frame_rate
        fps_out = self.output.frame_rate

        # Open the file and open stream
        cam = cv2.VideoCapture(self.input.filename)

        # Cycle through the frames
        self.n_flipbook_frames = 0
        self.frames = []
        for index_in in range(self.input.total_frames):
            # Read the frame
            success, data = cam.read()

            if not success:
                # Before breaking, update with the accurate number of frames
                self.input.total_frames = index_in
                break

            # otherwise we process the frame
            out_due = int(index_in / fps_in * fps_out)
            if out_due > self.n_flipbook_frames:
                success, data = cam.retrieve()
                if not success:
                    # Before breaking, update with the accurate number of frames
                    self.total_frames = index_in
                    break
                # otherwise we process the frame
                frame = Frame(data,
                              self.n_flipbook_frames,
                              self.input.width,
                              self.input.height,
                              self.output.frame_output_width,
                              self.output.frame_output_height,
                              self.output.frame_border_padding,
                              self.output.frame_left_padding)
                self.frames.append(frame)
                self.n_flipbook_frames += 1

        cam.release()
        cv2.destroyAllWindows()

    def save(self, paper_type, dpi, output_dir):
        printer = FlipbookPrinter(
            self.frames,
            self.output,
            paper_type,
            dpi,
            output_dir,
            self.base_name
        )

        printer.save()







