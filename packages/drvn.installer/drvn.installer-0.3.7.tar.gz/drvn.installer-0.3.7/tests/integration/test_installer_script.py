# pylint: disable=no-self-use, unused-argument, redefined-outer-name
import logging
from pathlib import Path

import pytest

import drvn.installer._utils as utils


@pytest.fixture(scope="class")
def workspace():
    workspace_path = _set_up_workspace()
    yield workspace_path
    _tear_down_workspace()


class TestDrvnInstallerScript:
    def test_help_exits_with_returncode_zero(self):
        _assert_returncode_zero("drvn_installer --help")

    def test_normal_run_exits_with_returncode_zero(self, workspace):
        _assert_returncode_zero("drvn_installer", cwd=workspace)

    # TODO: do some install testing in a docker container


_assert_returncode_zero = utils.try_cmd


def _set_up_workspace():
    workspace_path = _get_workspace_path()
    logging.debug("Setting up integration test workspace ...")
    utils.try_cmd(f"mkdir -p {workspace_path}")
    return workspace_path


def _tear_down_workspace():
    workspace_path = _get_workspace_path()
    logging.debug("Tearing down integration test workspace ...")
    utils.try_cmd(f"rm -rf {workspace_path}")


def _get_workspace_path():
    workspace_path = Path("/tmp/python_installer/integration_workspace")
    return workspace_path
