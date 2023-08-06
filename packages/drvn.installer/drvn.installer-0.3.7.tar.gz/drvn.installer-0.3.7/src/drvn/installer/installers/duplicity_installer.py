import logging
import os
import os.path
import subprocess

import drvn.installer._utils as utils


def install(is_install_drvn_configs):
    logging.info("Installing duplicity ...")
    _install_prerequisites()
    _install_duplicity()
    if is_install_drvn_configs:
        _install_drvn_configs()


def _install_prerequisites():
    apt_dependencies = [
        "git",
        "build-essential",
        "libssl-dev",
        "libffi-dev",
        "apt-utils",
        "python3-dev",
        "python3-pip",
        "python3-distutils-extra",
        "librsync-dev",
    ]
    utils.try_cmd(f"sudo apt-get install -y {' '.join(apt_dependencies)}")

    pip_dependencies = ["future>=0.18.2", "fasteners>=0.15"]
    utils.try_cmd(f"python3 -m pip install --user {' '.join(pip_dependencies)}")


def _install_duplicity():
    if not os.path.exists(os.path.expanduser("~/duplicity")):
        utils.try_cmd(
            "git clone https://gitlab.com/duplicity/duplicity.git",
            cwd=os.path.expanduser("~"),
        )
    utils.try_cmd(
        "sudo python3 setup.py install", cwd=os.path.expanduser("~/duplicity"),
    )


def _install_drvn_configs():
    pass
