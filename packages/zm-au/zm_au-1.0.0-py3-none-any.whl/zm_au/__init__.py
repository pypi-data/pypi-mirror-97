from .base_au import BaseAU
from .pip_github_au import PipGitHubAU
from .pip_au import PipAU

from reequirements import Requirement

REQUIREMENTS = [
    Requirement("GitHub CLI", ["gh", "--version"])
]

for requirement in REQUIREMENTS:
    requirement.check()

__version__ = "1.0.0"
