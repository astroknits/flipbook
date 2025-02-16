from pathlib import Path
from math import ceil
from argparse import ArgumentParser
import cv2
from PIL import Image
import PyPDF2

def parse_args():
    '''
    Parse command line arguments using argparse
    '''
    parser = ArgumentParser()
    parser.add_argument('filename', help='Path of the video file to use')
    args = parser.parse_args()
    return args


def validate_file(filename):
    '''
    Check that the file provided exists on disk
    Raise exception if it doesn't exist, otherwise return True
    '''
    if not Path(filename).exists():
        print('file not found')
        raise FileNotFoundError(f'Video file provided does not exist: {filename}')
    return True

def create_data_dir(data_dir):
    if Path(data_dir).exists():
        if Path(data_dir).is_dir():
            return True
        raise Exception(f'Expected data output directory path {data_dir} exists but is not a directory.')
    # If the data_dir does not exist, crate it
    Path(data_dir).mkdir()
    return True

def get_frame_jpg_name(data_dir, name_base, frame_no):
    return Path(data_dir).joinpath(Path(f'{name_base}.{str(frame_no)}.jpg'))

def get_frame_pdf_name(data_dir, name_base, frame_no):
    return Path(data_dir).joinpath(Path(f'{name_base}.{str(frame_no)}.pdf'))

def get_frames_to_process(frame_rate):
    '''
    Will effectively be downsampling the video frame rate
    by only processing one of every X frames.
    '''
    if frame_rate >= 30:
        # keep every 10th frame
        return 10
    elif frame_rate >= 20:
        # keep every 8th frame
        return 8
    else:
        # keep every 3rd frame
        return 3




def create_frames(filename, data_dir, name_base):
    # from https://www.geeksforgeeks.org/extract-images-from-video-in-python/

    # Open the file and open stream
    cam = cv2.VideoCapture(filename)

    frame_rate = cam.get(cv2.CAP_PROP_FPS)
    print(f'frame rate: {frame_rate} frames per second')
    print(f'')
    to_process = get_frames_to_process(frame_rate)
    print(f'Processing one for every {to_process} frames')

    # Create a directory for the extracted frames
    create_data_dir(data_dir)

    # Cycle through the frames
    frame_no = 0
    frame_paths = []
    while(True):
        # Read the frame
        frame_exists, frame = cam.read()

        if not frame_exists:
            # if there is no more frame being returned, we've hit the end
            # of the frames with none left to process
            break

        # otherwise we process the frame
        if frame_no % to_process == 0:
            name = get_frame_jpg_name(data_dir, name_base, frame_no)
            print(f'Creating {name}')

            # Write out the extracted jpg image
            cv2.imwrite(name, frame)

            image = Image.open(name)
            size = image.size

            name = get_frame_pdf_name(data_dir, name_base, frame_no)
            print(f'Creating {name}')

            # Write out the extracted pdf image
            image.save(name, 'PDF', resolution=100.0)
            image.close()

            frame_paths.append(name)
        frame_no += 1

    print(f'Extracted {frame_no} frames from {filename}')
    cam.release()
    cv2.destroyAllWindows()
    return frame_paths

def get_output_name(data_dir, output_name_base, batch_no):
    return Path(data_dir).joinpath(Path(f'{output_name_base}.{str(batch_no)}.pdf'))

def write_pdfs(frames, data_dir, output_name_base, num_per_page=9):
    num_pages = ceil(len(frames)/num_per_page)
    print(f'Num pages: {num_pages}')
    for batch_no in range(num_pages):
        batch = frames[batch_no * num_per_page: (batch_no + 1) * num_per_page]
        batch_name = get_output_name(data_dir, output_name_base, batch_no)
        print(f'Writing {batch_name}')
        write_pdf(batch, batch_name)


def write_pdf(frames, pdf_name):
    pdf_merger = PyPDF2.PdfMerger()
    for frame in frames:
        pdf_merger.append(frame)
    pdf_merger.write(pdf_name)
    pdf_merger.close()


def main():
    # Parse command line arguments
    args = parse_args()

    # Get the vide file name from the command line arguments
    # and validate it exists
    filename = args.filename
    validate_file(filename)

    # Read the video and extract the frames
    frames = create_frames(filename, 'data', 'video_frame')
    write_pdfs(frames, 'data', 'output')


if __name__ == '__main__':
    main()