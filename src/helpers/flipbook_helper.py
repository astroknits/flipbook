from pathlib import Path
from typing import Optional


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
