
class Output:
    '''
    Flipbook output parameters
    Right now we just need to know:
    * the flipbook output dimensions (w x h)
    * the flipbook frame rate
    '''
    def __init__(self,
                 width,
                 height,
                 frame_rate,
                 ):

        # width of output flipbook, in inches
        self.width_inches = width

        # height of output flipbook, in inches
        self.height_inches = height

        # Output frame rate for downsampling the video
        self.frame_rate = frame_rate

    def aspect(self):
        return self.height_inches / self.width_inches

    def print(self):
        print(f'Frame rate: {self.frame_rate:.2f} fps')
