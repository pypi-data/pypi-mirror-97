# zettelkasten/setupy.py
"""
Module handling the very first use of the zettelkasten after installation.
"""

import logging
from pathlib import Path

from . import defaults

logger = logging.getLogger(__name__)


def create_config_folder(dummy_location=None):
    """
    Create the zettelkasten's tweaking folder for the configuration
    and rc files.

    Parameters
    ----------
    dummy_location: str, pathlib.Path, None, default=None
        Dummy location used for testing. Design usage is to fallback on
        :attr:`zettelkasten.defaults.config_folder`.

    Examples
    --------
    1. Manipulate the zettelkasten's defaults to not override any zk in use
       (zk does not override anything unless explicitly stated, but better
       safe than sorry in this case):

        >>> import zettelkasten.defaults as defaults
        >>> original_folder_loc = defaults.location
        >>> defaults.config_folder = 'tests/doctest_dir/.zettelkasten.d'

    2. Create the folder:

        >>> create_config_folder()

    3. Revert to default settings to not mess up any following tets

        >>> defaults.config_folder = original_folder_loc

    4. Check if is where you would expect it

        >>> from pathlib import Path
        >>> Path('tests/doctest_dir/.zettelkasten.d').is_dir()
        True
    """

    logger.debug("Initializing zettelkasten configuration file")

    if dummy_location:
        logger.debug("Config folder requested to be created at dummy location")
        logger.debug(f"{Path(dummy_location)}")

        config_folder_path = Path(dummy_location)
    else:

        logger.debug(
            "Config folder requested to be created at default location"
        )
        logger.debug(f"{defaults.config_folder}")
        config_folder_path = Path(defaults.config_folder)

    config_folder_path.mkdir(parents=True, exist_ok=True)
    logger.debug("Succesfully create zettelkasten config folder at")
    logger.debug(f"{Path(config_folder_path).resolve()}")


def create_config_file_lines():
    """ Wrapper for creating the initial config file content as lines. """
    lines = [
        "[default]\n",
        "config_folder = ~/.zettelkasten.d\n",
        "\n",
        "def_author = Ammon, Mathias\n",
        "def_title = Config Parsed Test Title\n",
        "def_location_specifier = None\n",
        "\n",
        "location = ~/zettelkasten\n",
        "\n",
        "initial_folder_structure = \n",
        "    lobby,\n",
        "    %(sources_directory)s,\n",
        "    _sources/audios,\n",
        "    _sources/images,\n",
        "    _sources/pdfs,\n",
        "    _sources/videos\n",
        "\n",
        "name_sep = /\n",
        "\n",
        "required_attributes = \n",
        "    uid,\n",
        "    category,\n",
        "    subcategory\n",
        "\n",
        "sources_directory = _sources\n",
        "\n",
        "zettelkasten_bib_file = zettelkasten.bib\n",
        "\n",
        "[source_file_formats]\n",
        "audios = \n",
        "    mp3,\n",
        "    wav\n",
        "images = \n",
        "    jpg,\n",
        "    png\n",
        "pdfs =\n",
        "    pdf,\n",
        "    odt\n",
        "videos =\n",
        "    mp4\n",
        "\n",
        "[zettel_meta_attribute_defaults]\n",
        "# required for zettel adding to work    \n",
        "category= None\n",
        "subcategory= None\n",
        "# optional\n",
        "author = Mathias Ammon\n",
        "topics =\n",
        "tags =\n",
        "doc = today\n",
        "\n",
        "[zettel_meta_attribute_labels]\n",
        "# required for zettel adding to work\n",
        "uid = #+Title:\n",
        "category = #+Category:\n",
        "subcategory = #+Subcategory:\n",
        "# optional\n",
        "author = #+Author:\n",
        "doc = #+DOC:\n",
        "dole = #+DOLE:\n",
        "topics = #+Topics:\n",
        "tags = #+Tags:\n",
    ]

    return lines


def create_config_file(dummy_location=None):
    """
    Create the zettelkasten's :ref:`cfile` for tweaking locations
    templates etc. Every attribute inside :mod:`zettelkasten.defaults` can be
    overridden/tweaked using it. The :ref:`config file's <cfile>` default
    location is ``~/.zettelkasten.d/zk.cfg``.

    Note
    ----
    The top level folder (``.zettelkasten.d/`` by default) must exist for
    this function to succeed.

    Parameters
    ----------
    dummy_location: str, pathlib.Path, None, default=None
        Dummy location used for testing. Design usage is to fallback on
        :attr:`zettelkasten.defaults.config_file`.

    Examples
    --------
    1. Manipulate the zettelkasten's defaults to not override any zk in use
       (zk does not override anything unless explicitly stated, but better
       sage than sorry in this case):

        >>> import zettelkasten.defaults as defaults
        >>> original_folder_loc = defaults.config_folder
        >>> original_file_loc = defaults.config_file
        >>> defaults.config_folder = 'tests/doctest_dir/.zettelkasten.d'
        >>> defaults.config_file = 'tests/doctest_dir/.zettelkasten.d/zk.cfg'

    2. Create the folder:

        >>> create_config_folder()
        >>> create_config_file()

    3. Revert to default settings to not mess up any following tets

        >>> defaults.config_folder = original_folder_loc
        >>> defaults.config_file = original_file_loc

    4. Check if is where you would expect it

        >>> from pathlib import Path
        >>> Path('tests/doctest_dir/.zettelkasten.d/zk.cfg').is_file()
        True
    """
    logger.debug("Initializing zettelkasten configuration file")

    if dummy_location:
        logger.debug("Config file requested to be created at dummy location")
        logger.debug(f"{Path(dummy_location)}")

        config_file_path = Path(dummy_location)
    else:

        logger.debug("Config file requested to be created at default location")
        logger.debug(f"{defaults.config_file}")
        config_file_path = Path(defaults.config_file)

    if config_file_path.is_file():
        logger.debug("Configuration file already present")
        logger.debug("Zettelkasten has been setup before.")
        logger.debug("Not overwriting the existing config.")
    else:
        with open(config_file_path, "w") as f:
            f.writelines(create_config_file_lines())

            logger.debug("Succesfully create zettelkasten config file at")
            logger.debug(f"{config_file_path}")
