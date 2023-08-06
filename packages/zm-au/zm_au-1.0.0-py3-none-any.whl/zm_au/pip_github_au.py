import importlib
import json
import os
import subprocess
import sys

from zetuptools import PipPackage

from .base_au import BaseAU, UpdateException


class PipGitHubAU(BaseAU):

    def __init__(self, name, github_location, check_prerelease=False, dist="whl", silent=False):
        # If silent, redirect output of pip to the null device
        # Other parameters tell which uploads to look for and where (note that github_location's format is like "zmarffy/au")
        self._pip_package = PipPackage(name)
        self.github_location = github_location
        self.check_prerelease = check_prerelease
        self.dist = dist
        self.silent = silent
        super().__init__()

    @property
    def _o(self):
        # Determines what to redirect output to
        if self.silent:
            return subprocess.DEVNULL
        else:
            return None

    def _get_current_version(self):
        return self._pip_package.version

    def _get_latest_version(self):
        # Uses `gh api` to find the latest version
        try:
            d = json.loads(subprocess.check_output(
                ["gh", "api", f"repos/{self.github_location}/releases"]))
        except subprocess.CalledProcessError:
            raise UpdateException(
                f"Either {self.name} doesn't exist or you need to authorize with GitHub (run `gh auth login`) before attempting to check for updates for it")
        if not self.check_prerelease:
            latest = next(x for x in d if not x["prerelease"])
        else:
            latest = next(x for x in d)
        return latest["tag_name"]

    def _download(self):
        # Uses `gh release download` to download the version found from _get_latest_version (doesn't blindly install the latest version to avoid weird race conditions)
        subprocess.run(["gh", "release", "download", self.latest_version,
                        "-R", self.github_location, "-p", f"*.{self.dist}"], stdout=self._o)
        files = os.listdir()
        if len(files) != 1:
            raise ValueError(
                f"Ambiguous install instructions as multiple files were downloaded. Files: {files}")
        return files[0]

    def _update(self, update_file):
        # Installs a file with `pip install`
        subprocess.run([sys.executable, "-m", "pip",
                        "install", update_file], stdout=self._o)
        try:
            importlib.import_module(
                f"{self._pip_package.name}.install_directives")
            has_id = True
        except ModuleNotFoundError:
            has_id = False
        if has_id:
            subprocess.run(
                ["install-directives", self._pip_package.name, "install"])
