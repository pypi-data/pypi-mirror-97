# pylint: disable=no-self-use, protected-access
import drvn.installer.installer as installer

import pytest


class TestGetInstallableSoftware:
    def test_returns_a_list(self):
        installable_software = installer.get_installable_software()

        assert type(installable_software) is list
