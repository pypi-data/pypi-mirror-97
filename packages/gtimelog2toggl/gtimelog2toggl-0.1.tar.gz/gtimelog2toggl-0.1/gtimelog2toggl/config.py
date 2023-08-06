"""
Utility for getting configurations.
"""

import pathlib
import shutil
import subprocess
import sys

import appdirs
from box import Box


config_directory = pathlib.Path(appdirs.user_config_dir("gtimelog2toggl"))
config_directory.mkdir(exist_ok=True)
config_file_path = config_directory / "config.yml"


def load():
    """Loads configuration."""
    if not config_file_path.exists():
        orig_config_file_path = pathlib.Path(__file__).parent / "config.yml"
        shutil.copy(orig_config_file_path, config_file_path)
        assert config_file_path.exists()
    return Box.from_yaml(filename=config_file_path)


def open():
    """Opens up configuration file for editing."""
    subprocess.call(["xdg-open", str(config_file_path)])
