import unittest
from unittest.mock import patch, MagicMock
import cv2
from src.core.video_source import VideoSource
from src.helpers.flipbook_constants import FlipbookConstants


class TestVideoSource(unittest.TestCase):
    @patch("cv2.VideoCapture")
    @patch("pathlib.Path.exists", return_value=True)
    def test_video_source_initialization(self, mock_exists, mock_cv2):
        """Test successful initialization of VideoSource."""
        mock_cam = MagicMock()
        mock_cam.isOpened.return_value = True
        mock_cam.get.side_effect = [30.0, 1920, 1080, 100]  # FPS, Width, Height, Total Frames
        mock_cv2.return_value = mock_cam

        video_source = VideoSource("test.mp4")

        self.assertEqual(video_source.filename, "test.mp4")
        self.assertEqual(video_source.frame_rate, 30.0)
        self.assertEqual(video_source.width, 1920)
        self.assertEqual(video_source.height, 1080)
        self.assertEqual(video_source.total_frames, 100)
        self.assertAlmostEqual(video_source.aspect, 1080 / 1920)

        mock_cam.release.assert_called()
        cv2.destroyAllWindows()

    @patch("pathlib.Path.exists", return_value=False)
    def test_validate_video_file_not_found(self, mock_exists):
        """Test exception when video file does not exist."""
        with self.assertRaises(FileNotFoundError):
            VideoSource("nonexistent.mp4")

    @patch("pathlib.Path.exists", return_value=True)
    def test_validate_video_file_invalid_format(self, mock_exists):
        """Test exception when video format is not supported."""
        with patch.object(FlipbookConstants.Video, "SUPPORTED_FORMATS", {"mp4", "avi"}):
            with self.assertRaises(ValueError):
                VideoSource("test.mkv")

    @patch("cv2.VideoCapture")
    @patch("pathlib.Path.exists", return_value=True)
    def test_video_source_fails_to_open(self, mock_exists, mock_cv2):
        """Test exception when OpenCV fails to open the video file."""
        mock_cam = MagicMock()
        mock_cam.isOpened.return_value = False
        mock_cv2.return_value = mock_cam

        with self.assertRaises(RuntimeError):
            VideoSource("corrupt.mp4")

    @patch("cv2.VideoCapture")
    @patch("pathlib.Path.exists", return_value=True)
    def test_get_base_name(self, mock_exists, mock_cv2):
        """Test getting base name of video file."""
        mock_cam = MagicMock()
        mock_cam.isOpened.return_value = True
        mock_cv2.return_value = mock_cam

        video_source = VideoSource("/path/to/video.mp4")
        self.assertEqual(video_source.get_base_name(), "video")

    @patch("cv2.VideoCapture")
    @patch("pathlib.Path.exists", return_value=True)
    def test_print(self, mock_exists, mock_cv2):
        """Test print function output."""
        mock_cam = MagicMock()
        mock_cam.isOpened.return_value = True
        mock_cam.get.side_effect = [24.0, 1280, 720, 200]
        mock_cv2.return_value = mock_cam

        video_source = VideoSource("test.mp4")

        with patch("builtins.print") as mock_print:
            video_source.print_info()
            mock_print.assert_any_call("Input file: test.mp4")
            mock_print.assert_any_call("Resolution: 1280x720")
            mock_print.assert_any_call("Frame rate: 24.00 fps")


if __name__ == "__main__":
    unittest.main()
