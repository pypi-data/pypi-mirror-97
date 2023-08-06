"""A utility to find the nearest pyproject.toml file, in the ancestry."""

from pathlib import Path
from typing import Optional, Union

pyproject_toml = 'pyproject.toml'


def find_pyproject_toml(starting_directory: Union[Path, str]) -> Optional[Path]:
    current_path = Path(starting_directory)

    if not current_path.is_dir():
        current_path = current_path.parent

    for path in (current_path, *current_path.parents):
        possible_pyproject_file = path / pyproject_toml
        if possible_pyproject_file.is_file():
            return possible_pyproject_file

    return None
