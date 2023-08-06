from pathlib import Path

import drvn.installer._utils as utils


def is_cloned():
    path = _get_repository_path()
    return path.is_dir()


def clone():
    cwd = _get_repository_path().parent
    utils.try_cmd(
        "git clone https://github.com/hallgrimur1471/.dotfiles.git", cwd=cwd
    )


def get_path(path_relative_to_repository):
    repository_path = _get_repository_path()
    return repository_path / path_relative_to_repository


def _get_repository_path():
    return Path("~/.dotfiles").expanduser()
