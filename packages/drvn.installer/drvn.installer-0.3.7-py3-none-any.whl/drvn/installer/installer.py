import logging

from drvn.installer.installers import (
    ultimate_vim_installer,
    tmux_installer,
    duplicity_installer,
)


def install(software, is_install_drvn_configs):
    if software not in get_installable_software():
        raise RuntimeError(
            f"Installing '{software}' is not supported by this installer."
        )

    install_function = _get_install_function(software)
    install_function(is_install_drvn_configs)

    logging.info("Install successful")


def get_installable_software():
    installable_software = [
        software
        for software, install_function in _SOFTWARE_TO_INSTALL_FUNCTION.items()
    ]
    return installable_software


def _get_install_function(software):
    return _SOFTWARE_TO_INSTALL_FUNCTION[software]


_SOFTWARE_TO_INSTALL_FUNCTION = {
    "tmux": tmux_installer.install,
    "ultimate_vim": ultimate_vim_installer.install,
    "duplicity": duplicity_installer.install,
}
