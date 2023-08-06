# zettelkasten/defaults.py
from typing import List, Mapping, Optional, Union

import inspect
import os
from datetime import date
from pathlib import Path

config_overwrites = [
    "config_folder",
    "config_file",
    "def_author",
    "def_title",
    "def_year",
    "def_date",
    "def_location_specifier",
    "initial_folder_structure",
    "location",
    "name_sep",
    "required_attributes",
    "sources_directory",
    # dict of key, list
    "sources_file_formats",
    # dict of key stirng and key, list
    "zettel_meta_attribute_defaults",
    # dict of key, string
    "zettel_meta_attribute_labels",
    "zettelkasten_bib_file",
]
""" Default attributes that are designed to be
:mod:`monkeypatched <zettelkasten.monkeypatch>` during zettelkasten command
executions."""

location = os.path.normpath(
    os.path.join(
        inspect.getfile(inspect.currentframe()).split(  # type: ignore
            "defaults"
        )[0],
        "..",
        "tests",
        "testkasten",
    )
)
"""
Default location of the zettelkasten. For testing purposes this states a folder
inside the installation directory. Is to be :mod:`monkeypatched
<zettelkasten.monkeypatch>` during zettelkasten command executions.
"""

def_author = "Ammon, Mathias"
"""Default author name when creating a reference entry."""

def_title = "Test Title"
""" Default source title when creating a reference entry """

def_year = date.today().year
""" Default year when creating a reference entry """

def_date = date.today().strftime("%Y-%m-%d")
""" Default date when creating a reference entry """

def_location_specifier = None
""" Default location specifier inside the source (like ``page 5``) when
creating a reference entry """


def bibliography_entry(
    source_file,
    key,
    location_specifier=def_location_specifier,
    author=def_author,
    title=def_title,
    year=def_year,
    date=def_date,
):
    """
    Default utility for creating bib entries. Located here so a dedicated user
    can overwrite this. Not designed to be monkeypatched.
    """

    entry = [
        f"@misc{{{key},\n",
        f"  author   = {{{author}}},\n",
        f"  title    = {{{title}}},\n",
        f"  year     = {{{year}}},\n",
        f"  date     = {{{date}}},\n",
        f'  url      = "file://{os.path.abspath(source_file)}",\n',
        f"  keywords = {{{location_specifier}}},\n",
        "}%",
        "\n",
    ]

    return entry


config_folder = Path.home() / ".zettelkasten.d"
"""
Path the zettelkasten configuration and rc files reside in for userfriendly
tweaking.
"""

config_file = config_folder / "zk.cfg"
"""
Path the zettelkasten configuration file reside in for userfriendly tweaking.
"""

zettel_meta_attribute_labels = {
    "uid": "#+Title:",  # required for zettel adding to work
    "category": "#+Category:",  # required for zettel adding to work
    "subcategory": "#+Subcategory:",  # required for zettel adding to work
    # optional
    "author": "#+Author:",
    "doc": "#+DOC:",
    "dole": "#+DOLE:",
    "topics": "#+Topics:",
    "tags": "#+Tags:",
}
"""
Org mode tags, used for :mod:`zettelkasten.compile` mechanics.
"""

required_attributes = (
    "uid",
    "category",
    "subcategory",
)
"""
:attr:`Zettel meta attributes <zettel_meta_attribute_labels>` nedded by
:mod:`zettelkasten.compile` to generate zettelkasten meta information.
"""

zettel_meta_attribute_defaults: Mapping[
    str, Union[Optional[str], List[Optional[str]]]
] = {
    "category": None,  # required for zettel adding to work
    "subcategory": None,  # required for zettel adding to work
    # optional
    "author": "Mathias Ammon",
    "doc": None,
    "dole": None,
    "topics": [],
    "tags": [],
}
"""
Default values for initiating the :attr:`zettel_meta_attribute_labels`
"""

name_sep = "/"
"""
Seperator between category, subcategory and zetteluid.
See :func:`zettelkasten.add.parse_zettel_name` for more details.
"""

sources_directory = "_sources"
"""
Top level folder of all reference files.
"""

zettelkasten_bib_file = "zettelkasten.bib"
"""
The zettelkasten main bibliography location. All of the references ever added
are to be found inside this file.
"""

initial_folder_structure = [
    "lobby",
    f"{sources_directory}",
    "_sources/audios",
    "_sources/images",
    "_sources/pdfs",
    "_sources/videos",
]
"""
Folder created on the initial :ref:`setup <installation_setup>`.
"""

source_file_formats = {
    "audios": [
        "mp3",
    ],
    "images": [
        "jpg",
    ],
    "pdfs": [
        "pdf",
    ],
    "videos": [
        "mp4",
    ],
}
"""
Mapping used for infering file types and respective reference file sortings
(Video files beeing copied to ``_sources/videos/`` etc.).
"""


def infer_file_type(f):
    """ Tries to enfer the file type by looking at the file ending"""
    file_ending = f.split(".")[-1]

    for folder, file_endings in source_file_formats.items():
        if file_ending in file_endings:
            return folder


state = "hardcoded"
"""
State indicating if module contents are currently monkeypatched by
:mod:`zettelkasten.monkeypatch`.
"""
