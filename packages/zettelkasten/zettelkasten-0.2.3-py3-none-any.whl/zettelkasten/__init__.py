# type: ignore[attr-defined]
"""CLI interface for managing a folder based zettelkasten using emacs org-mode
file zettels and a bibtex reference system"""

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
