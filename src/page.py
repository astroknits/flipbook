from PIL import Image
from src.frame import Frame


class Page:
    def __init__(self,
                 paper_type,
                 output,
                 frame_border_padding=50,
                 left_frame_padding=260,
                 dpi=300
                 ):

        # Select output paper format for printing
        self.paper_type = paper_type

        self.output = output

        # dots per inch
        self.dpi = dpi

        # frame width in pixels
        self.frame_width = self.output.width_inches * dpi

        # frame height in pixels
        self.frame_height = self.output.height_inches * dpi

        # Number of rows and columns to arrange flipbook frames in a page
        self.nrows = self.get_nrows()
        self.ncols = self.get_ncols()

        self.frame_border_padding = frame_border_padding

        self.left_frame_padding = left_frame_padding

    def get_nrows(self):
        return int(self.paper_type.value.height_inches // self.output.height_inches)

    def get_ncols(self):
        return int(self.paper_type.value.width_inches // self.output.width_inches)

    def get_frames_per_page(self):
        return self.nrows * self.ncols

    def print_info(self):
        print(f'ncols: {self.ncols}')
        print(f'nrows: {self.nrows}')
        print(f'Page format: {self.paper_type.value.name}')

    def get_offset(self, frame_no):
        # Get the offset on which to paste the whole frame on the page including padding
        rel_frame_no = frame_no % self.get_frames_per_page()

        row = rel_frame_no // self.nrows
        col = rel_frame_no % self.nrows

        offset_width = self.frame_width * col
        offset_height = self.frame_height * row

        return offset_width, offset_height

    def write_page(self, frames, page_filename, input_width, input_height):
        page = Image.new('RGB', (self.paper_type.value.frame_width, self.paper_type.value.frame_height), 'white')

        for (frame_no, data) in frames:
            # create frame object based on image data,
            # frame number, and input/output dimensions
            # and desired padding
            frame = Frame(
                data,
                frame_no,
                input_width,
                input_height,
                self.frame_width,
                self.frame_height,
                self.frame_border_padding,
                self.left_frame_padding,
            )

            # get image data for full frame including padding
            img = frame.get_frame()

            # determine global pixel offset on the page
            # based on the frame number, ie. the row/column where the
            # frame should be tiled
            offset = self.get_offset(frame_no)

            # paste the image on the page
            page.paste(img, offset)

        page.save(page_filename)

