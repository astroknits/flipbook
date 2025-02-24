from PIL import Image

from src.frame import Frame


class Page:
    def __init__(self):
        self.page = None

    def write(self, frames, filename, input, output):
        grid = Image.new('RGB', (output.output_width, output.output_height), 'white')

        for (frame_no, data) in frames:
            frame = Frame(data, frame_no, input, output)
            img = frame.get_frame()
            offset = frame.get_offset() # tuple wxh
            grid.paste(img, offset)

        grid.save(filename)

