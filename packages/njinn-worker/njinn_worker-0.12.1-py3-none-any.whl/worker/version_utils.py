"""
We use get_worker_version both in our code and in setup.py,
so we can't put it in a file with external dependencies.
"""
import os


def get_worker_version() -> str:
    """
    Gets the worker version
    """
    version_file = open(os.path.join(os.path.dirname(__file__), "VERSION"))
    return version_file.read().strip()
