import os

from math import ceil
from typing import List, Tuple

from PIL import Image
from pypdf import PdfWriter
from tqdm import tqdm

from src.core.frame import Frame
from src.core.flipbook_output import FlipbookOutput
from src.helpers.flipbook_helper import FlipbookHelper
from src.media.padding import Padding, HorizontalPadding, VerticalPadding
from src.paper.paper_type import PaperType


class FlipbookPrinter:
    def __init__(self,
                 frames: List[Frame],
                 flipbook_output: FlipbookOutput,
                 paper_type: str,
                 dpi: int,
                 output_dir: str,
                 base_name: str
                 ) -> None:
        '''
        Initializes the FlipbookPrinter.

        :param frames: List of Frame objects to be printed
        :param flipbook_output: Flipbook output configuration
        :param paper_type: Type of paper used
        :param dpi: Dots per inch for printing
        :param output_dir: Directory to store output PDFs
        :param base_name: Base name for output files
        '''

        # full list of frames
        self.frames = frames

        # output parameters
        self.flipbook_output = flipbook_output
        # paper parameters
        self.paper_type = PaperType.get(paper_type)
        # dots per inch for printing
        self.dpi = dpi

        # output directory and base file name for output PDFs
        self.output_dir = output_dir
        self.base_name = base_name

    def save(self) -> None:
        """Generates and saves the flipbook PDF."""
        self.print_info()
        self.__create_output_dir()
        self.__write_pages()
        self.__combine_pdfs()

    @property
    def nrows(self):
        return int(self.height // self.flipbook_output.height)

    @property
    def ncols(self):
        return int(self.width // self.flipbook_output.width)

    @property
    def num_per_page(self):
        # Compute the number of rows and columns that fit on a page
        return self.nrows * self.ncols

    @property
    def num_pages_to_print(self):
        # Calculate the total number of pages required
        return ceil(len(self.frames) / self.num_per_page)

    @property
    def width(self):
        return self.paper_type.format.width

    @property
    def height(self):
        return self.paper_type.format.height

    @property
    def output_file(self):
        return FlipbookHelper.get_output_name(self.base_name, self.output_dir)

    @property
    def page_padding(self) -> Padding:
        horiz_padding = self.width - self.ncols * self.flipbook_output.width
        vert_padding = self.height - self.nrows * self.flipbook_output.height
        return HorizontalPadding(horiz_padding) + VerticalPadding(vert_padding)

    def __create_output_dir(self):
        return FlipbookHelper.create_output_dir(self.output_dir)

    def __get_offset(self, frame_no: int) -> Tuple[int, int]:
        '''Computes the offset position for a frame on the page.'''
        rel_frame_no = frame_no % self.num_per_page

        row = rel_frame_no // self.ncols
        col = rel_frame_no % self.ncols

        offset_width = self.page_padding.left + self.flipbook_output.width * col
        offset_height = self.page_padding.top + self.flipbook_output.height * row

        return offset_width, offset_height

    def __write_page(self, frames: List[Frame], frame_no: int) -> None:
        '''Generates and saves an individual page with the given frames.'''
        page_filename = FlipbookHelper.get_output_name(self.base_name, self.output_dir, frame_no)
        page = Image.new('RGB', (self.width, self.height), 'white')

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
                total=self.num_pages_to_print,
                desc='Saving printable flipbook'):
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
        output_frames = [FlipbookHelper.get_output_name(self.base_name, self.output_dir, page_no)\
                         for page_no in range(self.num_pages_to_print)]
        output_file_name = self.output_file
        merger = PdfWriter()
        for page in output_frames:
            merger.append(page)

        merger.write(output_file_name)
        merger.close()
        for page in output_frames:
            os.remove(page)
        print(f'\nWrote {output_file_name}\n\n')

    def print_info(self):
        print('----------------------------')
        print('Printable Flipbook Specs')
        print('----------------------------')
        print(f'Printed page type: {self.paper_type.format.name}')
        print(f'Printed page size (inches): {self.paper_type.format.size}')
        print(f'Printed page size (pixels): {self.paper_type.format.res}')
        print(f'Printed page dpi: {self.dpi}')
        print(f'Frames per page: {self.nrows}x{self.ncols}')
        print(f'Pages to print: {self.num_pages_to_print}')
        print(f'Output file: {self.output_file}')
        print('----------------------------')
        print('\n')
