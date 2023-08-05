import logging
import re
from urllib import request
from xml.etree import ElementTree

import pytools

log = logging.getLogger(__name__)


def test_package_version():
    dev_version = pytools.__version__

    log.info(f"Test package version – version set to: {dev_version}")
    assert re.match(
        r"^(\d)+\.(\d)+\.(\d)+(rc\d+)?$", dev_version
    ), "pytools.__version__ is not in MAJOR.MINOR.PATCH[rcN] format."

    releases_uri = "https://pypi.org/rss/project/gamma-pytools/releases.xml"

    with request.urlopen(releases_uri) as response:
        assert response.getcode() == 200, "Error getting releases from PyPi"
        releases_xml = response.read()

    tree = ElementTree.fromstring(releases_xml)
    releases_nodes = tree.findall(path=".//channel//item//title")
    releases = [r.text for r in releases_nodes]

    log.info(f"Found these releases on PyPi:{releases}")

    assert (
        dev_version not in releases
    ), f"Current package version {dev_version} already on PyPi"
