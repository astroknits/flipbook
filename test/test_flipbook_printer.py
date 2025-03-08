import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from src.core.flipbook_printer import FlipbookPrinter
from src.core.frame import Frame
from src.core.flipbook_output import FlipbookOutput
from src.helpers.flipbook_helper import FlipbookHelper
from src.media.padding import HorizontalPadding, VerticalPadding
from src.media.resolution import Resolution
from src.media.size import Size
from src.paper.paper_format import PaperFormat
from src.paper.paper_type import PaperType


class TestFlipbookPrinter(unittest.TestCase):
    mock_paper_format_name = 'US Letter'
    frame_width_in = 5
    frame_height_in = 3
    page_width_in = 11
    page_height_in = 8.5
    dpi = 300

    def get_frame(self, frame_no):
        mock_frame = MagicMock(spec=Frame)
        mock_frame.frame_no = frame_no
        return mock_frame

    def setUp(self):
        self.mock_flipbook_output = MagicMock(spec=FlipbookOutput)
        self.mock_flipbook_output.size = Size(
                                         self.frame_width_in,
                                         self.frame_height_in
                                         )
        self.mock_flipbook_output.width = self.frame_width_in * self.dpi
        self.mock_flipbook_output.height = self.frame_height_in * self.dpi
        self.mock_flipbook_output.size = Size(
                                        self.frame_width_in * self.dpi,
                                        self.frame_height_in * self.dpi
                                        )
        self.mock_paper_format = MagicMock(spec=PaperFormat)
        self.mock_paper_format.name = self.mock_paper_format_name
        self.mock_paper_format.size = Size(
                                      self.page_width_in,
                                      self.page_height_in
                                      )
        self.mock_paper_type = MagicMock(spec=PaperType)
        self.mock_paper_type.format = self.mock_paper_format

        self.output_dir = "test_output"
        self.base_name = "flipbook_test"

        self.mock_frames = [self.get_frame(frame_no) for frame_no in range(10)]

        self.flipbook_printer = FlipbookPrinter(
            self.mock_frames,
            self.mock_flipbook_output,
            'letter',
            300,
            self.output_dir,
            self.base_name
        )

    @patch("os.listdir", return_value=[])
    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.is_dir", return_value=True)
    @patch("pathlib.Path.iterdir", return_value=[])  # Mocking the directory as empty
    def test_create_output_dir_exists_empty(self, mock_iterdir, mock_is_dir, mock_exists, mock_listdir):
        """Tests that an existing empty directory does not raise an exception."""
        self.flipbook_printer._FlipbookPrinter__create_output_dir()


    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.exists", return_value=False)
    def test_create_output_dir_not_exists(self, mock_mkdir, mock_exists):
        """Tests that a non-existent directory is created."""
        self.flipbook_printer._FlipbookPrinter__create_output_dir()
        mock_mkdir.assert_called_once()


    def test_get_output_name(self):
        """Tests that output file names are generated correctly."""
        self.assertEqual(
            FlipbookHelper.get_output_name(self.flipbook_printer.base_name, self.flipbook_printer.output_dir, 1),
            Path(self.output_dir) / "flipbook_test.1.pdf"
        )
        self.assertEqual(
            self.flipbook_printer.output_file,
            Path(self.output_dir) / "flipbook_test.pdf"
        )


    def test_get_offset(self):
        """Tests that frame offsets are calculated correctly."""
        offset_x, offset_y = self.flipbook_printer._FlipbookPrinter__get_offset(1)

        rel_frame_no = 1 % self.flipbook_printer.num_per_page

        row = rel_frame_no // self.flipbook_printer.ncols
        col = rel_frame_no % self.flipbook_printer.ncols

        horiz_padding = self.flipbook_printer.width - \
                        self.flipbook_printer.ncols * self.flipbook_printer.flipbook_output.width
        vert_padding = self.flipbook_printer.height - \
                       self.flipbook_printer.nrows * self.flipbook_printer.flipbook_output.height

        offset_width = HorizontalPadding(horiz_padding).left + \
                       self.flipbook_printer.flipbook_output.width * col
        offset_height = VerticalPadding(vert_padding).top + \
                        self.flipbook_printer.flipbook_output.height * row

        self.assertEqual(offset_x, offset_width)
        self.assertEqual(offset_y, offset_height)

    @patch("PIL.Image.new")
    @patch("PIL.Image.Image.paste")
    @patch("PIL.Image.Image.save")
    def test_write_page(self, mock_new, mock_paste, mock_save):
        """Tests that a page is generated and saved correctly."""
        self.flipbook_printer._FlipbookPrinter__write_page(self.mock_frames[:5], 1)
        mock_save.assert_called_once()

    @patch("os.remove")
    @patch("pypdf.PdfWriter.append")
    @patch("pypdf.PdfWriter.write")
    @patch("pypdf.PdfWriter.close")
    def test_combine_pdfs(self, mock_close, mock_write, mock_append, mock_remove):
        """Tests that PDF merging is performed correctly."""
        self.flipbook_printer._FlipbookPrinter__combine_pdfs()
        self.assertEqual(mock_append.call_count, 3)
        mock_write.assert_called_once()
        mock_close.assert_called_once()
        self.assertEqual(mock_remove.call_count, 3)

if __name__ == "__main__":
    unittest.main()
