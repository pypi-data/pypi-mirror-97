# zettelkasten/monkeypatch.py
"""
Module aggregating all of the monkey patching functionalities.

Each time a command is executed via the command line,
zettelkasten monkey patches it's defaults as specified
in it's :ref:`cfile`.
"""

from typing import Any, MutableMapping, Optional, Type, Union

import configparser
import logging
from datetime import date

from . import defaults

logger = logging.getLogger(__name__)


def patch_defaults(config_file_path):
    """
    Main monkeypatching utility. Ensures the paramters inside the
    :ref:`cfile` are enforced by overwriting zettelkasten's defaults.
    """

    # create a config parse able to parse lists
    configs = configparser.ConfigParser(
        converters={"list": lambda x: [i.strip() for i in x.split(",")]}
    )

    # read in the config file
    configs.read(config_file_path)

    value: Optional[str] = None  # add typing hint for value
    for key, value in configs["default"].items():
        if key in defaults.config_overwrites:
            logger.debug(f"Monkeypatching {key}\n")
            logger.debug("with")
            logger.debug(f"{value}\n")
            if value == "None":
                value = None

            setattr(defaults, key, value)

    # parse pure list dict
    source_file_formats = {}
    for key in configs["source_file_formats"]:
        source_file_formats[key] = configs["source_file_formats"].getlist(key)

    logger.debug("Monkeypatching source_file_formats\n")
    logger.debug("with")
    logger.debug(f"{source_file_formats}\n")
    defaults.source_file_formats = source_file_formats

    # parse pure string dict
    zettel_meta_attribute_labels = {
        k: v for k, v in configs["zettel_meta_attribute_labels"].items()
    }

    logger.debug("Monkeypatching zettel_meta_attribute_labels\n")
    logger.debug("with")
    logger.debug(f"{zettel_meta_attribute_labels}\n")
    defaults.zettel_meta_attribute_labels = zettel_meta_attribute_labels

    # pare mixed dict
    zettel_meta_attribute_defaults: MutableMapping[str, Any] = {}
    values = ["category", "subcategory", "author", "doc", "dole"]
    for key in configs["zettel_meta_attribute_defaults"]:
        if key in values:
            v: Optional[str] = configs["zettel_meta_attribute_defaults"][key]
            if v == "None":
                v = None
                zettel_meta_attribute_defaults[key] = v
            if v in ["today", "now", "jetzt", "heute"]:

                date.today().strftime("%Y-%m-%d")
                d: Type[date] = date
                zettel_meta_attribute_defaults[key] = d

        else:
            lst = configs["zettel_meta_attribute_defaults"].getlist(key)
            if lst == [""]:
                lst = list()
            zettel_meta_attribute_defaults[key] = lst

    logger.debug("Monkeypatching zettel_meta_attribute_defaults\n")
    logger.debug("with")
    logger.debug(f"{zettel_meta_attribute_defaults}\n")
    defaults.zettel_meta_attribute_defaults = zettel_meta_attribute_defaults

    logger.debug("Set the defaults.state 'config_file_monkeypatched'")
    defaults.state = "config_file_monkeypatched"
