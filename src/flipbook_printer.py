import os

from math import ceil
from pathlib import Path
from typing import Optional, List, Tuple

from PIL import Image
from pypdf import PdfWriter
from tqdm import tqdm

from src.frame import Frame
from src.output import Output
from src.paper_type import PaperType


class FlipbookPrinter:
    def __init__(self,
                 frames: List[Frame],
                 output: Output,
                 paper_type: str,
                 dpi: int,
                 output_dir: str,
                 base_name: str
                 ):
        '''
        Initializes the FlipbookPrinter.

        :param frames: List of Frame objects to be printed
        :param output: Output configuration
        :param paper_type: Type of paper used
        :param dpi: Dots per inch for printing
        :param output_dir: Directory to store output PDFs
        :param base_name: Base name for output files
        '''

        # full list of frames
        self.frames = frames

        # output parameters
        self.output = output
        # paper parameters
        self.paper_type = PaperType.get(paper_type)
        # dots per inch for printing
        self.dpi = dpi

        # output directory and base file name for output PDFs
        self.output_dir = output_dir
        self.base_name = base_name

        # Compute the number of rows and columns that fit on a page
        self.nrows = int(self.paper_type.format.height //
                         self.output.frame_output_height)
        self.ncols = int(self.paper_type.format.width //
                         self.output.frame_output_width)
        self.num_per_page = self.nrows * self.ncols

        # Calculate the total number of pages required
        self.num_pages_to_print = ceil(len(self.frames) / self.num_per_page)

    def save(self) -> None:
        """Generates and saves the flipbook PDF."""
        self.__create_output_dir()
        self.__write_pages()
        self.__combine_pdfs()

    def __create_output_dir(self) -> None:
        """Ensures that the output directory exists and is empty."""
        output_dir_path = Path(self.output_dir)
        if Path.exists(output_dir_path):
            if output_dir_path.is_dir():
                if os.listdir(self.output_dir):
                    raise Exception((f'Output directory {self.output_dir} '
                                     'already exists and is nonempty.'))
                return
            raise Exception((f'Expected data output directory path {self.output_dir}'
                             ' exists but is not a directory.'))
        # If the data_dir does not exist, crate it
        output_dir_path.mkdir()
        return

    def get_output_name(self, page_no: Optional[int] = None) -> Path:
        '''
        Returns the filename for a given page number,
        or the final PDF if no page number is given.
        '''
        if page_no is None:
            filename = f'{self.base_name}.pdf'
        else:
            filename = f'{self.base_name}.{str(page_no)}.pdf'
        return Path(self.output_dir).joinpath(Path(filename))

    def __get_offset(self, frame_no: int) -> Tuple[int, int]:
        '''Computes the offset position for a frame on the page.'''
        rel_frame_no = frame_no % self.num_per_page

        row = rel_frame_no // self.ncols
        col = rel_frame_no % self.ncols

        offset_width = self.output.frame_output_width * col
        offset_height = self.output.frame_output_height * row

        return offset_width, offset_height

    def __write_page(self, frames: List[Frame], frame_no: int) -> None:
        '''Generates and saves an individual page with the given frames.'''
        page_filename = self.get_output_name(frame_no)
        page = Image.new('RGB',
                         (self.paper_type.format.width, self.paper_type.format.height),
                         'white')

        for frame in frames:
            # get image data for full frame including padding
            img = frame.get_frame()

            # determine global pixel offset on the page
            # based on the frame number, ie. the row/column where the
            # frame should be tiled
            offset = self.__get_offset(frame.frame_no)

            # paste the image on the page
            page.paste(img, offset)

        page.save(page_filename)

    def __write_pages(self) -> None:
        '''
        Writes all pages containing the flipbook frames.
        '''
        for page_no in tqdm(
                range(self.num_pages_to_print),
                total=self.num_pages_to_print):
            # Get subset of frames for the batch
            start_frame = page_no * self.num_per_page
            end_frame = (page_no + 1) * self.num_per_page - 1

            frames_in_batch = self.frames[start_frame: end_frame + 1]
            self.__write_page(frames_in_batch, page_no)

        print()

    def __combine_pdfs(self) -> None:
        '''
        Combines all individual pages into a single PDF
        and cleans up temporary files.
        '''
        output_frames = [self.get_output_name(page_no) for page_no in range(self.num_pages_to_print)]
        output_file_name = self.get_output_name(None)
        merger = PdfWriter()
        for page in output_frames:
            merger.append(page)

        merger.write(output_file_name)
        merger.close()
        for page in output_frames:
            os.remove(page)
        print(f'\nWrote {output_file_name}\n\n')
