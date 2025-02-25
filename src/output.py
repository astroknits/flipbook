from PIL import Image

from src.frame import Frame


class Output:
    '''
    Settings for the layout of the output images
    intended to be printed.

    Note there is a lot here that is still pretty rough/ad hoc
    and is intended to be be streamlined/automated in the future

    e.g. right now we specify the number of rows and/or columns
    per sheet, but eventually we would like to specify an output
    flipbook dimension and work backwards to calculate how many frames
    will fit per page,
    '''
    def __init__(self,
                 width,
                 height,
                 frame_rate,
                 paper_type,
                 frame_border_padding=50,
                 left_frame_padding=260,
                 dpi=300,
                 ):

        # width of output flipbook, in inches
        self.width = width

        # height of output flipbook, in inches
        self.height = height

        # dots per inch
        self.dpi = dpi

        # Output frame rate for downsampling the video
        self.frame_rate = frame_rate

        # Select output paper format for printing
        self.paper_type = paper_type

        # Number of rows and columns to arrange flipbook frames in a page
        self.nrows = self.get_nrows(height)
        self.ncols = self.get_ncols(width)

        self.frame_border_padding = frame_border_padding

        self.left_frame_padding = left_frame_padding

    def aspect(self):
        return self.height/self.width

    def get_nrows(self, height):
        return int(self.paper_type.value.height // height)

    def get_ncols(self, width):
        return int(self.paper_type.value.width // width)

    def frames_per_page(self):
        return self.nrows * self.ncols

    def xres(self):
        return self.width * self.dpi

    def yres(self):
        return self.height * self.dpi

    def print(self):
        print(f'ncols: {self.ncols}')
        print(f'nrows: {self.nrows}')
        print(f'Frame rate: {self.frame_rate:.2f} fps')
        print(f'Page format: {self.paper_type.value.name}')
        print(f'Page aspect ratio: {self.paper_type.value.aspect:.2f}')

    def get_offset(self, frame_no):
        # Get the offset on which to paste the whole frame on the page including padding
        rel_frame_no = frame_no % self.frames_per_page()

        row = rel_frame_no // self.nrows
        col = rel_frame_no % self.nrows

        offset_width = self.xres() * col
        offset_height = self.yres() * row

        return offset_width, offset_height

    def write(self, frames, page_filename, input_width, input_height):
        page = Image.new('RGB', (self.paper_type.value.xres(), self.paper_type.value.yres()), 'white')

        for (frame_no, data) in frames:
            # create frame object based on image data,
            # frame number, and input/output dimensions
            # and desired padding
            frame = Frame(
                data,
                frame_no,
                input_width,
                input_height,
                self.xres(),
                self.yres(),
                self.frame_border_padding,
                self.left_frame_padding,
            )

            # get image data for full frame including padding
            img = frame.get_frame()

            # determine global pixel offset on the page
            # based on the frame number, ie. the row/column where the
            # frame should be tiled
            offset = self.get_offset(frame_no) # tuple wxh

            # paste the image on the page
            page.paste(img, offset)

        page.save(page_filename)

