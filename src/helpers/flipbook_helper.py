from pathlib import Path


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