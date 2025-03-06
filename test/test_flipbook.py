import unittest
from unittest.mock import MagicMock, patch

from src.flipbook import Flipbook
from src.frame import Frame
from src.canvas import Canvas
from src.resolution import Resolution
from src.video_source import VideoSource
from src.flipbook_output import FlipbookOutput


class TestFlipbook(unittest.TestCase):
    mock_frame_data = "frame_data"
    mock_directory = "/path/to/output"

    def get_mock_capture(self,
                         frame_data,
                         is_opened=True,
                         success=True):
        mock_capture = MagicMock()
        mock_capture.isOpened.return_value = is_opened
        mock_capture.grab.return_value = success
        mock_capture.retrieve.return_value = (success, frame_data)
        return mock_capture

    def get_mock_video_source(self,
                              filename="test_video.mp4",
                              frame_rate=30,
                              aspect=16/9,
                              total_frames=100):
        mock_video_source = MagicMock(spec=VideoSource)
        mock_video_source.filename = filename
        mock_video_source.frame_rate = frame_rate
        mock_video_source.aspect = aspect
        mock_video_source.total_frames = total_frames
        return mock_video_source

    def get_mock_flipbook_output(self,
                                 frame_rate=10,
                                 width=800,
                                 height=600):
        mock_flipbook_output = MagicMock(spec=FlipbookOutput)
        mock_flipbook_output.frame_rate = frame_rate
        mock_flipbook_output.canvas_res = Resolution(width, height)
        return mock_flipbook_output

    @patch("cv2.VideoCapture")
    def test_extract_frames_success(self, MockVideoCapture):
        # Mock the video source and flipbook output attributes
        mock_video_source = self.get_mock_video_source()
        mock_flipbook_output = self.get_mock_flipbook_output()

        # set up mock video capture
        mock_capture = self.get_mock_capture(self.mock_frame_data)

        # Simulate that the VideoCapture object returns mock data
        MockVideoCapture.return_value = mock_capture

        # Create an instance of Flipbook
        flipbook = Flipbook(mock_video_source, mock_flipbook_output, mock_capture)

        # Call the method to test
        flipbook.extract_frames()

        # Check if frames were extracted
        self.assertEqual(len(flipbook.frames), 34)  # Adjust based on the test scenario

    @patch("cv2.VideoCapture")
    def test_extract_frames_fail(self, MockVideoCapture):
        # Same setup as above
        mock_video_source = self.get_mock_video_source()
        mock_flipbook_output = self.get_mock_flipbook_output()

        # Simulate the failure scenario (e.g., VideoCapture cannot open the file)
        mock_capture = self.get_mock_capture(self.mock_frame_data, is_opened=False)

        # Simulate that the VideoCapture object returns mock data
        MockVideoCapture.return_value = mock_capture
        flipbook = Flipbook(mock_video_source, mock_flipbook_output, mock_capture)

        with self.assertRaises(RuntimeError):
            flipbook.extract_frames()

    def test_process_frame(self):
        # Setup
        mock_video_source = self.get_mock_video_source()
        mock_flipbook_output = self.get_mock_flipbook_output()
        mock_canvas = MagicMock(spec=Canvas)

        # Test that process_frame returns a Frame object
        flipbook = Flipbook(mock_video_source, mock_flipbook_output)
        frame = flipbook.process_frame(self.mock_frame_data, 0, mock_canvas)

        self.assertIsInstance(frame, Frame)
        self.assertEqual(frame.data, self.mock_frame_data)

    def test_video_frame_source(self):
        # Setup
        total_frames = 5
        mock_video_source = self.get_mock_video_source(total_frames=total_frames)
        mock_flipbook_output = self.get_mock_flipbook_output()
        mock_capture = self.get_mock_capture(self.mock_frame_data) # MagicMock(spec=cv2.VideoCapture)
        flipbook = Flipbook(mock_video_source, mock_flipbook_output)

        # Mock capture_frame
        with patch.object(flipbook, 'capture_frame', return_value=self.mock_frame_data):
            frame_data = flipbook.video_frame_source(mock_capture)

        # Test that the correct number of frames are returned
        self.assertEqual(len(frame_data), total_frames)

    @patch("cv2.VideoCapture")
    def test_frame_generator(self, MockVideoCapture):
        # Setup as before
        mock_video_source = self.get_mock_video_source()
        mock_flipbook_output = self.get_mock_flipbook_output()

        flipbook = Flipbook(mock_video_source, mock_flipbook_output)

        # Mock frame data for generator
        mock_frame_data = [self.mock_frame_data] * 100

        frame_gen = flipbook.frame_generator(mock_frame_data)

        # Test the frame generator output
        frames = list(frame_gen)
        self.assertEqual(len(frames), 34)  # Expected number of frames

    @patch("src.flipbook.FlipbookPrinter")
    def test_save(self, MockFlipbookPrinter):
        # Setup
        mock_video_source = self.get_mock_video_source()
        mock_flipbook_output = self.get_mock_flipbook_output()

        # Mock frame data
        flipbook = Flipbook(mock_video_source, mock_flipbook_output)
        flipbook.frames = ["frame1", "frame2", "frame3"]

        # Test that save calls FlipbookPrinter and saves the flipbook
        flipbook.save(paper_type="Letter", dpi=300, output_dir=self.mock_directory)

        MockFlipbookPrinter.assert_called_once_with(
            flipbook.frames,
            mock_flipbook_output,
            "Letter",
            300,
            "/path/to/output",
            flipbook.base_name
        )

    def test_invalid_save(self):
        # Setup
        mock_video_source = self.get_mock_video_source(total_frames=0)
        mock_flipbook_output = self.get_mock_flipbook_output()

        # Flipbook with no frames should raise an error when saving
        flipbook = Flipbook(mock_video_source, mock_flipbook_output)

        with self.assertRaises(ValueError):
            flipbook.save(paper_type="A4", dpi=300, output_dir=self.mock_directory)
