from pathlib import Path
from typing import Optional
import math

from src.helpers.flipbook_constants import FlipbookConstants
from src.media.resolution import Resolution


class FlipbookHelper:

    @staticmethod
    def validate_output_dir(pathname: Path) -> None:
        '''
        Ensures that the output directory exists and is empty.
        '''
        if pathname.exists():
            if not pathname.is_dir():
                raise IsADirectoryError(f'Output directory {pathname} exists but is not a directory.')
            if any(pathname.iterdir()):
                raise FileExistsError(f'Output directory {pathname} exists and is nonempty.')

    @staticmethod
    def create_output_dir(output_dir) -> None:
        '''
        Ensures that the output directory exists and is empty.
        '''
        output_dir_path = Path(output_dir)

        # Validate the output directory before creating it
        FlipbookHelper.validate_output_dir(output_dir_path)

        # If the directory does not exist, create it (and all parent directories if necessary)
        output_dir_path.mkdir(parents=True, exist_ok=True)
        return

    @staticmethod
    def get_output_name(base_name, output_dir, page_no: Optional[int] = None) -> Path:
        '''
        Returns the filename for a given page number,
        or the final PDF if no page number is given.
        '''
        if page_no is None:
            filename = f'{base_name}.pdf'
        else:
            filename = f'{base_name}.{str(page_no)}.pdf'
        return Path(output_dir).joinpath(Path(filename))

    @staticmethod
    def get_fontsize(output_res: Resolution) -> int:
        '''
        Return the font size for frame # watermark, appropriately scaled
        Scale using sqrt of height or width ratio to prevent drastic scaling
        '''
        reference_res = FlipbookConstants.Font.REF_RES
        if reference_res.aspect >= output_res.aspect:
            # compare heights
            scale_factor = math.sqrt(output_res.height / reference_res.height)
        else:
            # compare widths
            scale_factor = math.sqrt(output_res.width / reference_res.width)
        return int(FlipbookConstants.Font.SIZE * scale_factor)

