from PIL import Image
from src.frame import Frame


class Output:
    def __init__(self,
                 paper_type,
                 frame_output_width,
                 frame_output_height,
                 frame_border_padding=50,
                 left_frame_padding=260,
                 dpi=300
                 ):

        # Select output paper format for printing
        self.paper_type = paper_type

        # dots per inch
        self.dpi = dpi

        # frame width in pixels
        self.frame_output_width = int(frame_output_width * dpi)

        # frame height in pixels
        self.frame_output_height = int(frame_output_height * dpi)

        # Number of rows and columns to arrange flipbook frames in a page
        self.nrows = self.get_nrows()
        self.ncols = self.get_ncols()

        self.frame_border_padding = frame_border_padding

        self.left_frame_padding = left_frame_padding

    def print_info(self):
        print(f'Flipbook frame size: {self.frame_output_width}x{self.frame_output_height}')
        print(f'Paper type: {self.paper_type.value.name}')
        print(f'Printer dpi: {self.dpi}')
        print(f'nrows x ncols: {self.nrows}x{self.ncols}')
        print(f'frame_border_padding: {self.frame_border_padding}')
        print(f'left_frame_padding: {self.left_frame_padding}')

    def get_nrows(self):
        return int(self.paper_type.value.height // self.frame_output_height)

    def get_ncols(self):
        return int(self.paper_type.value.width // self.frame_output_width)

    def get_frames_per_page(self):
        return self.nrows * self.ncols

    def get_offset(self, frame_no):
        # Get the offset on which to paste the whole frame on the page including padding
        rel_frame_no = frame_no % self.get_frames_per_page()

        row = rel_frame_no // self.nrows
        col = rel_frame_no % self.nrows

        offset_width = self.frame_output_width * col
        offset_height = self.frame_output_height * row

        return offset_width, offset_height

    def write_page(self, frames, page_filename, frame_input_width, frame_input_height):
        page = Image.new('RGB',
                         (self.paper_type.value.width, self.paper_type.value.height),
                         'white')

        for (frame_no, data) in frames:
            # create frame object based on image data,
            # frame number, and input/output dimensions
            # and desired padding
            frame = Frame(
                data,
                frame_no,
                frame_input_width,
                frame_input_height,
                self.frame_output_width,
                self.frame_output_height,
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

