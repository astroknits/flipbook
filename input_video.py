from pathlib import Path
import cv2


class InputVideo:
    SUPPORTED_VIDEO_FORMATS = ['mov', 'mp4']

    def __init__(self, filename):
        self.filename = self.validate_video_file(filename)
        self.get_video_metadata()

    def print(self):
        print(f'Input file: {self.filename}')
        print(f'Resolution: {self.get_resolution()}')
        print(f'Frame rate: {self.frame_rate:.2f} fps')

    def validate_video_file(self, filename):
        '''
        Check that the file provided exists on disk
        Raise exception if it doesn't exist, otherwise return True
        '''
        filepath = Path(filename)
        if not filepath.exists():
            print('file not found')
            raise FileNotFoundError(f'Video file provided does not exist: {filename}')
        if filepath.suffix.strip('.') not in self.SUPPORTED_VIDEO_FORMATS:
            msg = f'Video file type {filepath.suffix} not supported (not one of {self.SUPPORTED_VIDEO_FORMATS})'
            raise Exception(msg)
        return filename

    def get_resolution(self):
        return f'{self.width}x{self.height}'

    def get_video_metadata(self):
        # Open the file and open stream
        cam = cv2.VideoCapture(self.filename)

        self.frame_rate = cam.get(cv2.CAP_PROP_FPS)
        self.width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))

        cam.release()
        cv2.destroyAllWindows()
