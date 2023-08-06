# pylint: disable=no-self-use, protected-access
import drvn.installer.installers.tmux_installer as installer

import pytest
from unittest.mock import MagicMock, patch


class TestCalculateUrlToLatestReleaseTarball:
    def test_normal(self):
        calculated_url = installer._calculate_url_to_latest_release_tarball("2.9a")
        assert (
            calculated_url
            == "https://github.com/tmux/tmux/releases/download/2.9a/tmux-2.9a.tar.gz"
        )


@patch("drvn.installer._utils.open_url")
class TestFindUrlToLatestRelease:
    def test_normal(self, open_url):
        open_url.return_value = '{"tag_name":"3.0a"}'
        assert "https" in installer._find_url_to_latest_release()
