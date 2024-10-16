from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("aymara_ai")
except PackageNotFoundError:
    # package is not installed
    __version__ = "unknown"
