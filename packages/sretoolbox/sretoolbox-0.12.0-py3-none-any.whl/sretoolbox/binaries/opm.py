"""
Abstractions around the OPM binary.
"""

import os

from semver import VersionInfo
from sretoolbox.binaries.base import Binary


class Opm(Binary):
    """
    Defines the properties of OPM.
    """
    binary_template = 'opm-{version}'
    download_url_template = ('https://github.com/operator-framework/'
                             'operator-registry/releases/download/'
                             'v{major}.{minor}.{patch}/'
                             'linux-amd64-opm')

    def get_version_command(self):
        """
        Gets the command and its option(s) to check the version.

        :return: version command
        :rtype: list
        """
        return [self.command, 'version']

    def parse_version(self, version):
        """
        Parses version string as returned by the command execution
        to a VersionInfo instance.

        :param version: the return from the version command
        :type version: str

        :return: the parsed version as a VersionInfo object
        :rtype: VersionInfo
        """
        opm_version = version.split('"')[1].split('v', 1)[1]
        return VersionInfo.parse(version=opm_version)

    def process_download(self, path):
        """
        Processes a downloaded file and returns the executable binary path.

        :param path: The downloaded file path
        :return: The executable binary path.
        """
        os.chmod(path, 0o777)
        return path
