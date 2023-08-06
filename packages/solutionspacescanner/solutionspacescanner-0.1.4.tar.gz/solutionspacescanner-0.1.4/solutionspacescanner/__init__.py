"""
SolutionSpaceScanner
Python package to perform solution state scanning and generate ABSINTH parameter files
"""
import os

# Add imports here
from .solutionspacescanner import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions


_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
    return os.path.join(_ROOT, 'data', path)
