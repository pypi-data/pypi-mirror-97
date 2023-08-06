# zettelkasten/add.py
import typing

import logging
import os
import pathlib
import shutil

from . import defaults

logger = logging.getLogger(__name__)


class ZettelName(typing.NamedTuple):
    """
    Zettel name consisting of ``category``, ``subcategory``, ``uid``

    Parameters
    ----------
    category: str
        String representing the top level folder inside the zettelkasten.
       ``None`` if Zettel is inside the :ref:`Lobby`.

    subcategory: str
        String representing the top sublevel folder inside the zettelkasten.
        ``None`` if no subcategory is given.

    uid: str
        String representing the top sublevel folder inside the zettelkasten.
        ``None`` if no subcategory is given.

    Return
    ------
    zettel_name: ~typing.NamedTuple
        Namedtuple instance object serving as zettel name.

    Examples
    --------
    >>> ZettelName('folder', 'subfolder', 'zettel')
    ZettelName(category='folder', subcategory='subfolder', uid='zettel')
    """

    category: str
    subcategory: str
    uid: str


def parse_zettel_name(name):
    r"""Zettel name parsing syntax

    Parameters
    ----------
    name : str
        Zettel name. Either a singular uid as in "my_zettel" or a
        folder/subfolder/uid syntax as in "woodturning/tools/chisel".

        Used to automatically sort new zettels either into the
        category/subcategory stated or into the :ref:`Lobby` if only an uid is
        given.

        The seperator used for uidentifying the different parts is specified
        using the :ref:`cfile`. It defaults to ``\``.

        If no complete name is given, then category and subcategory are set to
        their defaults as stated in the :ref:`cfile`.


    Examples
    --------
    1. Using a complete name to automatically sort the zettel:

        >>> parse_zettel_name("woodturning/tools/chisel")
        ZettelName(category='woodturning', subcategory='tools', uid='chisel')

    2. Using only an uid, puts the Zettel into the :ref:`Lobby`:

        >>> parse_zettel_name("my_zettel")
        ZettelName(category=None, subcategory=None, uid='my_zettel')

    3. Using the wrong syntax fails somewhat gracefully:

        >>> parse_zettel_name("wrong_syntax/°_^%$!§")
        ZettelName(category=None, subcategory=None, uid='°_^%$!§')

    Returns
    -------
    zettel_name: tuple
        Tuple consisting of ('category', 'subcategory', 'uid')
    """

    logger.debug("-------------------------------")
    logger.debug("Preparing to parse Zettel name")

    # is a complete name given?
    if defaults.name_sep in name:

        # yes, to parse it
        logger.debug(f"{defaults.name_sep} found in '{name}'")
        parts = name.split(defaults.name_sep)

        # syntax is only valid using 2 seperators:
        if len(parts) == 3:
            category, subcategory, uid = parts
            logger.debug(f"Succesfully dissassembled '{name}' into:")
            logger.debug(
                f"category: '{category}', subcategory: "
                + f"'{subcategory}', uid: '{uid}'"
            )

        # used wrong syntax. State a warning and fail gracefully
        else:
            uid = parts[-1]
            category = defaults.zettel_meta_attribute_defaults.get(
                "category", None
            )
            subcategory = defaults.zettel_meta_attribute_defaults.get(
                "category", None
            )

            logger.warning(f"'{name}' could not be dissassembled correctly")
            logger.warning(f"Dissassembling yielded '{parts}'. Parsing into:")
            logger.warning(
                f"category: '{category}', subcategory: "
                + f"'{subcategory}', uid: '{uid}'"
            )

    # No, only an uid was passed:
    else:
        uid = name
        category = defaults.zettel_meta_attribute_defaults.get("category", None)
        subcategory = defaults.zettel_meta_attribute_defaults.get(
            "category", None
        )

        logger.debug("Zettel name parsed.")
        logger.debug("-------------------------------\n")

    return ZettelName(category, subcategory, uid)


def parse_zettel_attributes(parsed_zettel_name, **kwargs):
    r"""
    Zettel attribute parsing utility.

    The attributes parsed are stated in the :ref:`cfile` along with a set
    of required attributes. These required attributes are made of the
    attributes of the :class:`ZettelName` and stem form this zettelkasten's
    dogma of having a ``zettelkasten/category/subcategory/zettel`` hierarchy.

    note
    ----
    Called by :meth:add_zettel during zettel creation.

    Parameters
    ----------
    parsed_zettel_name: ZettelName
        :class:`typing.NamedTuple` representing the zettel.

    **kwargs:
        The attributes to be parsed. Attributes are/need to be stated in the
        :ref:`cfile` along with a set of required attributes.

        Attributes will be added to the Zettel-Org-File as::

            # +Attribute_Name1: Attribute_Value1
                        .
                        .
            # +Attribute_NameN: Attribute_ValueN

    Return
    ------
    parsed_attributes: dict
        Dictionairy of the parsed attributes. The attributes parsed are stated
        in the :ref:`cfile`.

    Examples
    --------
    Building on the examples stated in :meth:`parse_zettel_name`

    >>> import pprint #imported for better doctest output

        1. Using a complete name to automatically sort the zettel:

        >>> zn = parse_zettel_name("woodturning/tools/chisel")
        >>> zattr = parse_zettel_attributes(zn)
        >>> pprint.pprint(zattr)
        {'#+Author:': 'Mathias Ammon',
         '#+Category:': 'woodturning',
         '#+DOC:': None,
         '#+DOLE:': None,
         '#+Subcategory:': 'tools',
         '#+Tags:': [],
         '#+Title:': 'chisel',
         '#+Topics:': []}


    2. Using only a uid, but adding tags and topics:

        >>> zn = parse_zettel_name("my_zettel")
        >>> zattr = parse_zettel_attributes(
        ...     zn,
        ...     tags=['#Rework', '#Pressurloss', '#Solarthermal'],
        ...     topics=['#EnergyConcept', '#Thermodynamics'])
        >>> pprint.pprint(zattr)
        {'#+Author:': 'Mathias Ammon',
         '#+Category:': None,
         '#+DOC:': None,
         '#+DOLE:': None,
         '#+Subcategory:': None,
         '#+Tags:': ['#Rework', '#Pressurloss', '#Solarthermal'],
         '#+Title:': 'my_zettel',
         '#+Topics:': ['#EnergyConcept', '#Thermodynamics']}


    3. Using the wrong syntax and using non supported attributes (unsupported):

        >>> zn = parse_zettel_name("wrong_syntax/°_^%$!§")
        >>> zattr = parse_zettel_attributes(
        ...     zn,
        ...     unsupported='This does not show')
        >>> pprint.pprint(zattr)
        {'#+Author:': 'Mathias Ammon',
         '#+Category:': None,
         '#+DOC:': None,
         '#+DOLE:': None,
         '#+Subcategory:': None,
         '#+Tags:': [],
         '#+Title:': '°_^%$!§',
         '#+Topics:': []}

    """

    logger.debug("-------------------------------")
    logger.debug("Preparing to parse zettel attributes")

    # map zettel atrributes
    zettel_attributes = dict()

    # start with the required ones using the zettel name:
    for req_at in defaults.required_attributes:

        zettel_attributes[
            defaults.zettel_meta_attribute_labels[req_at]
        ] = getattr(parsed_zettel_name, req_at)

    # add to that the optional ones as stated in the cfile
    for attribute, label in defaults.zettel_meta_attribute_labels.items():

        if attribute not in defaults.required_attributes:
            zettel_attributes[label] = kwargs.get(
                attribute, defaults.zettel_meta_attribute_defaults[attribute]
            )

    return zettel_attributes


def create_zettel_location(parsed_zettel_name, dummy_location=None):
    """
    Utility for making sure the requested zettel location exists.

    The zettelkasten location is stated in the :ref:`cfile`.

    In case the :paramref:`~create_zettel_location.parsed_zettel_name` states
    a :paramref:`~ZettelName.category` this serves as toplevel folder
    inside the zettelkasten folder and the :paramref:`~ZettelName.subcategory`
    serves as folder inside the toplevel folder.

    The Zettel itself is then represented as a folder inside this subcategory
    folder and storing all the necessary files for taking advantage of the
    org file.

    In case no :paramref:`~ZettelName.category` is stated (and therfor also no
    :paramref:`~ZettelName.subcategory`), the zettel folder is created inside
    the :ref:`lobby` which is a folder directly beneath the zettelkasten folder
    of which it's name is specified again inside the :ref:`cfile`. The default
    lobby folder name is ``lobby``.

    note
    ----
    Called by :meth:add_zettel during zettel creation.

    Parameters
    ----------
    parsed_zettel_name: ZettelName
        :class:`NamedTuple` representing the zettel location and uid as
        returned by :meth:`parse_zettel_name`

    dummy_location: str, pathlib.Path, None, default=None
        Dummy location used for testing.

    Return
    ------
    zettel_location: pathlib.Path
        Path specifying the zettel location.

    Examples
    --------
    Building on the examples stated in :meth:`parse_zettel_name`

    >>> import pprint #imported for better doctest output

        1. Using a complete name to automatically sort the zettel:

        >>> zn = parse_zettel_name("woodturning/tools/chisel")
        >>> path = create_zettel_location(
        ...     parsed_zettel_name=zn,
        ...     dummy_location="tests/testkasten/")
        >>> print(str(path))
        tests/testkasten/woodturning/tools/chisel

    """
    logger.debug(79 * "-")
    logger.debug("Preparing to create zettel location")
    folder = parsed_zettel_name.category
    subfolder = parsed_zettel_name.subcategory
    zettel_folder = parsed_zettel_name.uid

    if dummy_location is not None:
        zk_location = dummy_location
    else:
        zk_location = defaults.location
    # create zettel directory
    if folder is None and subfolder is None:
        logger.debug("Only zettel uid was stated.")
        logger.debug("Creating a lobby location for it")

        zettel_path = os.path.join(zk_location, "lobby", zettel_folder)

    else:
        logger.debug("Complete zettel name was stated")

        zettel_path = os.path.join(
            zk_location, folder, subfolder, zettel_folder
        )

    # create zettel path
    pathlib.Path(zettel_path).mkdir(parents=True, exist_ok=True)

    return pathlib.Path(zettel_path)


def write_org_zettel_attributes(org_file_path, zettel_attributes):
    r"""
    Utility wrapping the attribute writing in a singular call.

    Parameters
    ----------
    org_file_path: str, pathlib.Path
        Text or byte string stating the org zettel's file location.
        For more info on zettel location see :func:`create_zettel_location`.
    zettel_attributes: dict
        Dictionairy stating mapping attribute names to attribute values
        as stated in the :ref:`cfile`. For more on zettel attributes
        see :func:`parse_zettel_attributes`.

    Examples
    --------

    1. Create zettel folder dummy location:

       >>> import pathlib
       >>> pathlib.Path("tests/testkasten/lobby/attributes").mkdir(
       ...     parents=True, exist_ok=True)

    2. Create a dummy org file:

        >>> dummy_loc = "tests/testkasten/lobby/attributes/attributes.org"
        >>> write_org_zettel_attributes(
        ...     org_file_path=dummy_loc,
        ...     zettel_attributes={
        ...         'test1': 'test_attribute',
        ...         'test2': 'test_attribute',
        ...     }
        ... )

    3. Read out it's attributes:

        >>> with open(dummy_loc, 'r') as f:
        ...     pass
        ...     lines = f.readlines()
        ...     for line in lines:
        ...         print(line.strip(' \n'))
        test1 test_attribute
        test2 test_attribute
    """
    with open(org_file_path, "w") as f:
        for attribute, value in zettel_attributes.items():
            f.write(" ".join((attribute, str(value), "\n")))

    logger.debug(f"Wrote zettel_attributes: {zettel_attributes}")
    logger.debug(f"Into Zettel at: {org_file_path}")


def write_org_zettel_bibliography(
    org_file_path, bibliography_file, force_overwrite=False
):
    r"""
    Utility wrapping bibliography addition to the org file.

    Parameters
    ----------
    org_file_path: str, pathlib.Path
        Text or byte string stating the org zettel's file location.
        For more info on zettel location see :func:`create_zettel_location`.
    bibliography_file: str
        String specifying the bibliography file filename. File will be on the
        same level as :paramref:`~write_org_zettel_bibliography.org_file_path`
    force_overwrite: bool, default=False
        If ``True`` an already existing Zettel-Org-File will be overridden.
        Use with care.

    Examples
    --------

    1. Create zettel folder dummy location:

       >>> import pathlib
       >>> pathlib.Path("tests/testkasten/lobby/bibliography").mkdir(
       ...     parents=True, exist_ok=True)

    2. Create a dummy org file:

        >>> dummy_loc = (
        ...     "tests/testkasten/lobby/bibliography/bibliography.org"
        ... )
        >>> write_org_zettel_bibliography(
        ...     org_file_path=dummy_loc,
        ...     bibliography_file="bibliography.bib",
        ...     force_overwrite=True,
        ... )

    3. Read out it's bibliography content

        >>> with open(dummy_loc, 'r') as f:
        ...     lines = f.readlines()
        ...     for line in lines:
        ...         print(line.strip(' \n'))
        * Bibliography
        <BLANKLINE>
        bibliography:bibliography.bib

    """
    logger.debug("Writing bibliography section into zettel.")
    logger.debug("Assumed bibliography file name is")
    logger.debug(f"{bibliography_file}")

    if force_overwrite:
        mode = "w"
    else:
        mode = "a"

    with open(org_file_path, mode) as f:
        f.writelines(
            ["\n", "* Bibliography\n\n", f"bibliography:{bibliography_file}"]
        )


def create_bibliography_file(bibliography_file_path, force_overwrite=False):
    """
    Wrap bibliography file creation.

    Parameters
    ----------
    bibliography_file_path: str, pathlib.Path
        Text or byte string stating the bibliography's file location.
        For more info on the location see :func:`create_zettel_location`.
        By convention this has the same name as the corresponding
        zettel-org-file but with a different file ending.
    force_overwrite: bool, default=False
        If ``True`` an already existing Zettel-Bibliograph-File will be
        overridden. Use with care.

    Raises
    ------
    FileExistsError
        Raised if bibliography file already present and
        :paramref:`~create_bibliography_file.force_overwrite` is ``False``.
        Prevents unwanted data loss.

    Examples
    --------

    >>> import os

    1. Create zettel folder dummy location:

       >>> import pathlib
       >>> pathlib.Path("tests/testkasten/lobby/bibliography").mkdir(
       ...     parents=True, exist_ok=True)

    2. Create a dummy bib file:

        >>> dummy_loc = (
        ...     "tests/testkasten/lobby/bibliography/bibliography.bib"
        ... )
        >>> create_bibliography_file(
        ...     bibliography_file_path=dummy_loc,
        ...     force_overwrite=True)
        >>> os.path.isfile(dummy_loc)
        True
    """
    logger.debug(f"Writing bibliography file in {bibliography_file_path}.")

    # check for overwrite
    if os.path.isfile(bibliography_file_path):
        already_exists_msg = (
            f"Bibliography file in '{bibliography_file_path}' already exists"
        )

        if force_overwrite:
            logger.debug(already_exists_msg)
            logger.debug("Forced overwrite requested")
        else:  # dont force overwrite unless explicitly requested
            logger.error(already_exists_msg)
            logger.error("To purposely overwrite bibliography file use:")
            logger.error("zk add [-f/--force] zettel")
            raise FileExistsError

    with open(bibliography_file_path, "w"):
        pass


def create_bibliography_file_test_entries(
    zettel_name, force_overwrite=False, dummy_location=None
):
    """
    Wrap creating bibliography test entries.

    Parameters
    ----------
    zettel_name: str
        String specifying the name and/or the location of the zettel.
        See :class:`ZettelName` and :paramref:`parse_zettel_name.name` for more
        details.

    force_overwrite: bool, default=False
        If ``True`` already existing bibliography entries will be
        overridden. Use with care.

    dummy_location: str, pathlib.Path, None, default=None
        Dummy location used for testing. Design usage is to fallback on
        :attr:`zettelkasten.defaults.location`.
    """
    example_entries = [
        (
            "tests/bib_sources/test_audio.mp3",
            "audio_2021_sec2",
            "sec 2",
            "zk_api",
            "Test Audio",
        ),
        (
            "tests/bib_sources/test_image.jpg",
            "image_2021",
            None,
            "zk_api",
            "Test Image",
        ),
        (
            "tests/bib_sources/test_pdf.pdf",
            "pdf_2021_p2",
            "page 2",
            "zk_api",
            "Test PDF",
        ),
        (
            "tests/bib_sources/test_video.mp4",
            "video_2021_min42",
            "min 42",
            "zk_api",
            "Test Video",
        ),
    ]

    for (
        f,
        uid,
        locspec,
        author,
        title,
    ) in example_entries:
        new_source(
            zettel_name,
            f,
            uid,
            locspec=locspec,
            author=author,
            title=title,
            force_overwrite=force_overwrite,
            dummy_location=dummy_location,
        )


def new_zettel(name, force_overwrite=False, dummy_location=None, **kwargs):
    r"""Add a new Zettel to the Zettelkasten.

    Wraps all the utilities of:

        1. :func:`parse_zettel_name`
        2. :func:`parse_zettel_attributes`
        3. :func:`create_zettel_location`
        4. :func:`write_org_zettel_attributes`
        5. :func:`write_org_zettel_bibliography`

    in one callable designed to be used by the command line interface (cli).

    Parameters
    ----------
    name: str
        String specifying the name and/or the location of the zettel.
        See :class:`ZettelName` and :paramref:`parse_zettel_name.name` for more
        details.

    force_overwrite: bool, optional
        If ``True`` an already existing Zettel-Org-File will be overridden.
        Use with care. Default=False

    dummy_location: str, pathlib.Path, None,
        Dummy location used for testing. Used instead of
        :attr:`zettelkasten.defaults.location` when used.

    **kwargs
        Zettel attributes to be parsed. See :func:`parse_zettel_attributes`
        for more details.

    Raises
    ------
    FileExistsError
        Raised if zettel already present and
        :paramref:`~new_zettel.force_overwrite` is ``False``.

    Examples
    --------
    Building on the examples stated in :meth:`parse_zettel_name`

    >>> import os

        1. Using a complete name to automatically sort the zettel:

            >>> zn = parse_zettel_name("woodturning/tools/chisel")
            >>> path = create_zettel_location(
            ...     parsed_zettel_name=zn,
            ...     dummy_location="tests/testkasten/")
            >>> print(str(path))
            tests/testkasten/woodturning/tools/chisel

            (forced overwrite is used here for doctesting. Usually you don't
            want to do that)

            >>> new_zettel("woodturning/tools/chisel", force_overwrite=True)
            >>> os.path.isfile(
            ...     "tests/testkasten/woodturning/tools/chisel/chisel.org")
            True

        2. Use only a Zettel uid puts it into the lobby (stated in the
           :ref:`cfile`):

            (Again, forced overwrite is used here for doctesting. Usually you
            don't want to do that)

            >>> new_zettel("my_zettel", force_overwrite=True)
            >>> os.path.isfile(
            ...     "tests/testkasten/lobby/my_zettel/my_zettel.org")
            True

    Buildiing on the examples stated in :meth:`parse_zettel_attributes` tools
    add attributes to the Zettel during creation:

        >>> new_zettel(
        ...     name="woodturning/tools/gouge",
        ...     force_overwrite=True,
        ...     tags=["#Rework", "#NiceTry"],
        ...     topics=["#Test"],
        ...     not_showing="NotShowing",
        ...     )
        >>> zettel_org_file = pathlib.Path(
        ...     "tests/testkasten/woodturning/tools/gouge/gouge.org")
        >>> with open(zettel_org_file, 'r') as f:
        ...     lines = f.readlines()
        ...     for line in lines:
        ...         print(line.strip(' \n'))
        #+Title: gouge
        #+Category: woodturning
        #+Subcategory: tools
        #+Author: Mathias Ammon
        #+DOC: None
        #+DOLE: None
        #+Topics: ['#Test']
        #+Tags: ['#Rework', '#NiceTry']
        <BLANKLINE>
        * Bibliography
        <BLANKLINE>
        bibliography:gouge.bib
    """
    logger.debug("-------------------------------")
    logger.debug(f"Preparing to add Zettel '{name}'")

    # dissassemble the name/location syntax:
    zettel_name = parse_zettel_name(name)

    # parse the zettel attributes
    zettel_attributes = parse_zettel_attributes(zettel_name, **kwargs)

    zettel_path = create_zettel_location(
        parsed_zettel_name=zettel_name, dummy_location=dummy_location
    )

    # create zettel org file
    org_file_path = pathlib.Path(
        os.path.join(zettel_path, ".".join([zettel_name.uid, "org"]))
    )

    # check for overwrite
    if os.path.isfile(org_file_path):
        already_exists_msg = f"Zettel in '{zettel_path}' already exists"
        if force_overwrite:
            logger.debug(already_exists_msg)
            logger.debug("Forced overwrite requested")
        else:  # dont force overwrite unless explicitly requested
            logger.error(already_exists_msg)
            logger.error("To purposely overwrite a Zettel use:")
            logger.error("zk add [-f/--force] zettel")
            raise FileExistsError

    # wirte the zettel's inital attribute structure
    write_org_zettel_attributes(org_file_path, zettel_attributes)

    # create the zettel's bibliography file
    bib_file_path = pathlib.Path(
        os.path.join(zettel_path, ".".join([zettel_name.uid, "bib"]))
    )
    create_bibliography_file(bib_file_path, force_overwrite=force_overwrite)

    create_bibliography_file_test_entries(
        zettel_name=name,
        force_overwrite=True,
        dummy_location=dummy_location,
    )

    # write the zettel's bibiliography
    write_org_zettel_bibliography(org_file_path, f"{zettel_name.uid}.bib")

    logger.info(f"Succesfully created org-Zettel in '{org_file_path}'")


def write_source_entry(
    bibliography_file_path,
    source_file,
    uid,
    locspec,
    author,
    title,
    year,
    date,
    force_overwrite=False,
):
    """
    Utility wrapping source entry writing.

    Tests if the entry is already present,  whether to overwrite it or not and
    performs the actual writing.

    Parameters
    ----------
    bibliography_file_path: str, pathlib.Path
        Text or byte string stating the bibliography's file location.
        For more info on the location see :func:`create_zettel_location`.
        By convention this has the same name as the corresponding
        zettel-org-file but with a different file ending.

    source_file: file
        File representing the source that serves as reference.
        Supported file types are:

            - audio
            - image
            - pdf
            - video

        The source file is copied into :attr:`Zettelkasten's source folder
        <zettelkasten.defaults.sources_directory>`

    uid: str
        String uniquely specifying the source. Usually something like
        `author_year_locspec`

    locspec: str
        String specifying where (inside the source) exactly the reference
        points to. Something like:

            - 'page 42'
            - 'min 69',

    author: str
        String specifying the author. Either ``Surname, Name`` or
        ``Name Surname``

    title: str
        String specifying the source files title

    year: str, ~numbers.Number
        String or number specifying the year, the source was published

    date: str
        String specifying the date as in ``"%Y-%m-%d"``.

    force_overwrite: bool, default=False
        If ``True`` and the source is already present inside the bibliography
        file, then the entry will be overriden. Use with care.

    Raises
    ------
    FileExistsError
        Raised if source key already present and
        :paramref:`~write_source_entry.force_overwrite` is ``False``.
        Prevents unwanted data loss.
    """
    # open the zettel's bib file to write:
    logger.debug("Preparing to write the source entry")

    overwrite = False
    with open(bibliography_file_path) as f:
        content = f.read()
        if uid in content:
            already_exists_msg = (
                f"Entry of key {uid} already present in "
                + f"{bibliography_file_path}"
            )

            if force_overwrite:

                overwrite = True

                logger.debug(already_exists_msg)
                logger.debug("Overwrite requested.")

                part_1 = f"@misc{{{uid},\n"
                part_2 = content.split(part_1)[-1].split("\n}%\n")[0] + "\n}%\n"

                content_to_overwrite = part_1 + part_2

                replacement = "".join(
                    defaults.bibliography_entry(
                        source_file=source_file,
                        key=uid,
                        location_specifier=locspec,
                        author=author,
                        title=title,
                        year=year,
                        date=date,
                    )
                )

                content = content.replace(content_to_overwrite, replacement)
                # TODO overwrite
            else:
                logger.error(already_exists_msg)
                logger.error("To purposely overwrite an entry use:")
                # TODO Distinguish between api and command line call
                logger.error("zk source [-f/--force] file, key, [locspec]")
                raise FileExistsError

    if overwrite:
        with open(bibliography_file_path, "w") as f:
            logger.debug("Overwriting:\n")
            logger.debug(f"{content_to_overwrite}\n")
            logger.debug(f"in {bibliography_file_path}\n")
            logger.debug(f"with:\n {replacement}\n")
            f.write(content)

    else:
        with open(bibliography_file_path, "a") as f:
            logger.debug("No overwrite necessary, creating the entry")
            # print(f'writing into {bibliography_file_path}')
            f.writelines(
                defaults.bibliography_entry(
                    source_file=source_file,
                    key=uid,
                    location_specifier=locspec,
                    author=author,
                    title=title,
                    year=year,
                    date=date,
                )
            )


def new_source(
    zettel_name,
    source_file,
    uid,
    locspec=defaults.def_location_specifier,
    author=defaults.def_author,
    title=defaults.def_title,
    year=defaults.def_year,
    date=defaults.def_date,
    force_overwrite=False,
    dummy_location=None,
):
    r"""
    Source adding utility.

    Adds a source to a zettel's bibliography file as well as the
    :attr:`Zettelkasten's overall bibliography file
    <zettelkasten.defaults.zettelkasten_bib_file>`.
    Also copies the source file
    into the :attr:`Zettelkasten's source folder
    <zettelkasten.defaults.sources_directory>`.

    The bibliography entry is wirtten using the
    :attr:`bibliography entry <zettelkasten.defaults.bibliography_entry>`
    template.


    Parameters
    ----------
    zettel_name: str
        Zettel name. Either a singular uid as in "my_zettel" or a
        folder/subfolder/uid syntax as in "woodturning/tools/chisel". See
        :class:`ZettelName` and :func:`parse_zettel_name` for more details

    source_file: file
        File representing the source that serves as reference.
        Supported file types are:

            - audio
            - image
            - pdf
            - video

        The source file is copied into :attr:`Zettelkasten's source folder
        <zettelkasten.defaults.sources_directory>`

    uid: str
        String uniquely specifying the source. Usually something like
        `author_year_locspec`

    locspec: str
        String specifying where (inside the source) exactly the reference
        points to. Something like:

            - 'page 42'
            - 'min 69',

    author: str
        String specifying the author. Either ``Surname, Name`` or
        ``Name Surname``

    title: str
        String specifying the source files title

    year: str, ~numbers.Number
        String or number specifying the year, the source was published

    date: str
        String specifying the date as in ``"%Y-%m-%d"``.

    force_overwrite: bool, optional
        If ``True`` and the source is already present inside the bibliography
        file, then the entry will be overriden. Use with care.

    dummy_location: str, pathlib.Path, None, optional
        Dummy location used for testing. Design usage is to fallback on
        :attr:`zettelkasten.defaults.location`.

    Raises
    ------
    FileNotFoundError
        Raised when requested :paramref:`zettel <new_source.zettel_name>` is
        not found.

    Examples
    --------
    1. Default usecase, adding a new source (again, the force_overwrite=True
       is only used for doctesting, usually you don't want to use it this way):

        >>> new_zettel("woodturning/tools/skew", force_overwrite=True)
        >>> new_source(
        ...     zettel_name="woodturning/tools/skew",
        ...     source_file="tests/bib_sources/test_video.mp4",
        ...     uid="video2_2021_min42",
        ...     locspec="min 42",
        ...     force_overwrite=True)

        Check if the new source uid is in the zettels bibliography file:

        >>> with open(
        ...     "tests/testkasten/woodturning/tools/skew/skew.bib",
        ...     "r") as f:
        ...     "video2_2021_min42" in f.read()
        True

        Check if the file is now present inside the
        :attr:`Zettelkasten's source folder
        <zettelkasten.defaults.sources_directory>`:

        >>> os.path.isfile(
        ...     "tests/testkasten/_sources/videos/test_video.mp4")
        True

        See if the source uid is also present inside the zettelkasten's
        main bib file:

        >>> with open(
        ...     "tests/testkasten/_sources/zettelkasten.bib",
        ...     "r") as f:
        ...     "video2_2021_min42" in f.read()
        True
    """
    # generating the bib file string
    logger.debug("Preparing to add a new source entry")

    # dissassemble the name/location syntax:
    parsed_zettel_name = parse_zettel_name(zettel_name)

    # parse the zettel location
    zettel_path = create_zettel_location(
        parsed_zettel_name=parsed_zettel_name, dummy_location=dummy_location
    )

    org_file_path = pathlib.Path(
        os.path.join(zettel_path, ".".join([parsed_zettel_name.uid, "org"]))
    )

    # is zettel existing
    if not org_file_path.is_file():
        logger.error(f"Requested zettel was not found in {org_file_path}")
        raise FileNotFoundError

    # yes zettel is existing, so infer the zettel bibliography file path
    bib_file_path = pathlib.Path(
        os.path.join(zettel_path, ".".join([parsed_zettel_name.uid, "bib"]))
    )

    if dummy_location:
        location = dummy_location
    else:
        location = defaults.location

    logger.debug("Copying the new source entry into to main bib file")
    # also write an entry into the zettelkasten's bib file:
    zk_bib_file = os.path.join(
        location,
        defaults.sources_directory,
        defaults.zettelkasten_bib_file,
    )

    # copying the source file
    # find out directory by inspecting fileendings
    ftype = defaults.infer_file_type(source_file)

    destination = os.path.join(
        location,
        # defaults.location,
        defaults.sources_directory,
        ftype,
        source_file.split("/")[-1],
    )

    logger.debug(f"Copying the source file into {destination}")

    # and copy the file including permissions and meta data
    shutil.copy2(
        source_file,
        destination,
    )

    logger.debug("Writing the entry into the main bib file:")
    # also write the entry into the zk bib file
    write_source_entry(
        zk_bib_file,
        source_file=destination,
        uid=uid,
        force_overwrite=force_overwrite,
        locspec=locspec,
        author=author,
        title=title,
        year=year,
        date=date,
    )

    # write the actual source entry
    logger.debug("Writing the actual entry:")
    write_source_entry(
        bibliography_file_path=bib_file_path,
        source_file=destination,
        uid=uid,
        force_overwrite=force_overwrite,
        locspec=locspec,
        author=author,
        title=title,
        year=year,
        date=date,
    )

    logger.debug("Successfully added a new source entry")
