import logging
import os
import os.path
import argparse
import json
import subprocess
from pathlib import Path

import drvn.installer._utils as utils
import drvn.installer._dotfile_repository as dotfile_repository


def install(is_install_drvn_configs):
    logging.info("Installing tmux ...")
    _install_prerequisites()
    _install_tmux()
    if is_install_drvn_configs:
        _install_drvn_configs()


def _install_prerequisites():
    apt_dependencies = ["libevent-dev", "libncurses5-dev", "curl", "git"]
    utils.try_cmd(f"sudo apt-get install -y {' '.join(apt_dependencies)}")


def _install_tmux():
    latest_release_url = _find_url_to_latest_release()
    _install_tmux_from_url(latest_release_url)


def _install_tmux_from_url(tarball_url):
    version_tag = _find_version_tag_of_latest_release()
    tarball_file_name = f"tmux-{version_tag}.tar.gz"

    tarball_download_location = f"{os.environ['HOME']}/{tarball_file_name}"

    utils.try_cmd(
        f"cd ~ && "
        + f"curl -L -o {tarball_download_location} {tarball_url} && "
        + f"tar -xzf {tarball_file_name} && "
        + f"cd {tarball_file_name.replace('.tar.gz', '')} && "
        + f"./configure && "
        + f"make && "
        + f"sudo make install",
    )


def _install_drvn_configs():
    if not dotfile_repository.is_cloned():
        dotfile_repository.clone()
    _symlink_configs_to_dotfile_repository()


def _symlink_configs_to_dotfile_repository():
    dotfile_relative_path = Path(".tmux.conf")
    real_path = dotfile_repository.get_path(dotfile_relative_path)
    symlink_path = Path("~").expanduser() / dotfile_relative_path
    utils.cmd(f"rm {symlink_path}")
    utils.try_cmd(f"ln -s '{real_path}' '{symlink_path}'")


def _find_url_to_latest_release():
    version_tag = _find_version_tag_of_latest_release()
    url_to_latest_release_tarball = _calculate_url_to_latest_release_tarball(
        version_tag
    )
    return url_to_latest_release_tarball


def _get_project_root_dir():
    dn = os.path.dirname
    project_root_dir = dn(os.path.abspath(__file__))
    return project_root_dir


def _find_version_tag_of_latest_release():
    response = utils.open_url(
        "https://api.github.com/repos/tmux/tmux/releases/latest"
    )
    response_dict = json.loads(response)
    version_tag = response_dict["tag_name"]
    return version_tag


def _calculate_url_to_latest_release_tarball(version_tag):
    url_to_latest_release_tarball = (
        f"https://github.com/tmux/tmux/releases/download"
        f"/{version_tag}/tmux-{version_tag}.tar.gz"
    )
    return url_to_latest_release_tarball
