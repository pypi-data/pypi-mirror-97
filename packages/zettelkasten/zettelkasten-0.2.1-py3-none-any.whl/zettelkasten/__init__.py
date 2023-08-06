# type: ignore[attr-defined]
"""x reference system and emacs org-mode file zettels"""

try:
    from importlib.metadata import PackageNotFoundError, version
    import pkg_resources
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version


try:
    __version__ = version(__name__)
    __version__ = pkg_resources.get_distribution('zettelkasten').version
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
