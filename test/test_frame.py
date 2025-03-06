from unittest.mock import MagicMock

from src.flipbook import Flipbook


def test_frame_generator():
    # Fake frame data
    fake_frames = ["frame1", "frame2", "frame3", "frame4"]

    # Mock video_source and flipbook_output
    mock_video_source = MagicMock()
    mock_video_source.frame_rate = 30
    mock_flipbook_output = MagicMock()
    mock_flipbook_output.frame_rate = 10

    flipbook = Flipbook(mock_video_source, mock_flipbook_output)

    # Call frame_generator with fake frames
    frames = list(flipbook.frame_generator(fake_frames))

    # Verify correct number of frames are processed
    assert len(frames) == 3  # Expecting frames at 10 FPS from 30 FPS source
    assert frames[0].data == "frame1"
    assert frames[1].data == "frame2"
    assert frames[2].data == "frame4"
