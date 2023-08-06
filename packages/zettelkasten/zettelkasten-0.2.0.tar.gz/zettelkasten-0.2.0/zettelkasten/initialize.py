# zettelkasten/initialize.py
"""
Module handling zettelkasten creation and recreation. Used before most of the
commands coming from the cli are executed to ensure the zettelkasten looks like
it is expected to.
"""

import logging
import os
import pathlib

from . import defaults

logger = logging.getLogger(__name__)


def structure_zettelkasten(dummy_location=None):
    """Utility to (re)structure the zettelkasten.

    :attr:`defaults.location <zettelkasten.defaults.location>` is used for
    the zettelkasten main directory and
    :attr:`defaults.initial_folder_structure
    <zettelkasten.defaults.initial_folder_structure>` for toplevel directories
    inside the zettelkasten.

    Designed to be called before executing any other command to ensure
    the zettelkasten is structured like expected by the rest of the api.

    Parameters
    ----------
    dummy_location: str, pathlib.Path, None, default=None
        Dummy location used for testing. Design usage is to fallback on
        :attr:`zettelkasten.defaults.location`.

    Examples
    --------
    Create a zettelkasten at the default location (tests directory of
    'zettelkasten'):


    >>> structure_zettelkasten()

    Check if the main directory is present:

    >>> import zettelkasten.defaults
    >>> import os
    >>> os.path.isdir(zettelkasten.defaults.location)
    True
    """
    # create zettelkasten directory
    if dummy_location:
        location = dummy_location
    else:
        location = defaults.location

    if not os.path.isdir(location):
        logger.debug(
            f"The zettelkasten directory ('{location}'"
            + "is not an existing directory"
        )
        logger.debug("... so it's created")
    else:
        logger.debug(f"Zettelkasten directory in '{location}' already exsits.")
        logger.debug("Reastablishing initial folder structure")
        logger.debug("without deleting any existing structures.")

    for directory in defaults.initial_folder_structure:
        pathlib.Path(os.path.join(location, directory)).mkdir(
            parents=True, exist_ok=True
        )

    # create the zettelkasten bib file
    zk_bib_file = os.path.join(
        location,
        defaults.sources_directory,
        defaults.zettelkasten_bib_file,
    )

    with open(zk_bib_file, "a"):
        pass
