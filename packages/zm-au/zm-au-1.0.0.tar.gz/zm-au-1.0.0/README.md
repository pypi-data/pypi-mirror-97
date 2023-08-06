# `zm-au`

`zm-au` is a developer tool that provides an auto-updating API for programs. Note that this can be a bad idea for many reasons, so you should probably ask the user first.

Sorry for prefixing the name with "zm", but I'm sure I'll have to do that again as I have no creative names for anything anymore.

## Usage

`zm-au` comes with two useful auto-updaters, `PipAU` and `PipGitHubAU`, and a class to base an auto-updater off of.

Let's say you are creating a Python package called `skippitybop` and you want it to notify the user when there is an update available on PyPI for it. Simply insert this code where you want the update check to happen.

```python
from zm_au import PipAU

updater = PipAU("skippitybop")
updater.update(prompt=True)
```

When the code is run, if there is an update available on PyPI, the user will be prompted to install it via `pip`. If the user chooses to install it, the program will exit on success. Or failure, for that matter.

Take a guess what `prompt=False` would do.

Let's say you are creating a Python package called `boppityskip` on "bigboi"'s GitHub repo and you want it to notify the user when there is an update available on GitHub releases for it, probably because the package is private and not on PyPI. Insert this code where you want the update check to happen.

```python
from zm_au import PipGitHubAU

updater = PipGitHubAU("boppityskip", "bigboi/boppityskip", check_prerelease=True, dist="whl")
updater.update(prompt=True)
```

When the code is run, if there is an update available on GitHub releases (including prereleases) that is a `whl` file, the user will be prompted to install it via `pip`. Again, if the user chooses to install it, the program will exit on success or failure.

You can build your own AUs by making a class that inherits from `BaseAU`. Override the following functions as such.

- `_get_current_version` - Must return the current version of the package
- `_get_latest_version` - Must return the latest version of the package
- `_download` - Must download the package and return the filename of the downloaded file
- `_update` - Must install a package whose location is passed via the only parameter of this function

Be smart about how you use this!
