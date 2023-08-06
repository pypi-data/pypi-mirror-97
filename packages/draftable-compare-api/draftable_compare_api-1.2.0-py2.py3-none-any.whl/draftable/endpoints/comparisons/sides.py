from __future__ import absolute_import

from os.path import basename, isfile, join, splitext

from six import string_types

# Note: `urllib3` is a required dependency of `requests`
from urllib3.util import parse_url

from ..exceptions import InvalidPath
from .. import validation

try:
    # noinspection PyUnresolvedReferences
    from typing import List, Union, Optional, Any
except ImportError:
    pass


class Side(object):
    def __init__(self, file_type, display_name=None):
        # type: (str, Optional[str]) -> None
        self.__file_type = validation.validate_file_type(file_type)
        self.__display_name = None if display_name is None else str(display_name)

    @property
    def file_type(self):
        # type: () -> str
        return self.__file_type

    @property
    def display_name(self):
        # type: () -> Optional[str]
        return self.__display_name


class FileSide(Side):
    # noinspection PyShadowingBuiltins
    def __init__(self, file, file_type, display_name=None):
        # type: (Any, str, Optional[str]) -> None
        self.__file = validation.validate_file(file)
        super(FileSide, self).__init__(file_type=file_type, display_name=display_name)

    @property
    def file(self):
        # type: () -> Any
        return self.__file

    def __str__(self):
        return "File side: {} ({}, '{}')".format(
            self.__file, self.file_type, self.display_name
        )


class URLSide(Side):
    def __init__(self, url, file_type, display_name=None):
        # type: (str, str, Optional[str]) -> None
        self.__url = validation.validate_url(url)
        super(URLSide, self).__init__(file_type=file_type, display_name=display_name)

    @property
    def url(self):
        # type: () -> str
        return self.__url

    def __str__(self):
        return "URL side: {} ({}, '{}')".format(
            self.__url, self.file_type, self.display_name
        )


def data_from_side(side_name, side):
    """Given a side (which may be a string or Side object, return the data needed
    for a comparison POST request as a dictionary.
    """
    # type: (str, Union[str, FileSide, URLSide]) -> dict

    if isinstance(side, string_types):
        # User has provided a file path or URL.
        side = make_side(side)

    data = {
        "file_type": side.file_type,
    }

    if side.display_name:
        data["display_name"] = side.display_name
    if isinstance(side, URLSide):
        data["source_url"] = side.url
    else:
        assert isinstance(side, FileSide)
        data["file"] = (
            "{}.{}".format(side_name, side.file_type),
            side.file,
            join("application", "octet-stream"),
        )
    return data


def side_from_url(url, file_type, display_name=None):
    # type: (str, str, Optional[str]) -> URLSide
    return URLSide(url, file_type, display_name)


def side_from_file(file_obj, file_type, display_name=None):
    # type: (Any, str, Optional[str]) -> FileSide
    return FileSide(file_obj, file_type, display_name)


def side_from_file_path(file_path, file_type=None, display_name=None):
    should_guess = file_type is None or file_type == "guess"
    if should_guess:
        file_type = guess_file_type_from_path(file_path)
    display_name = display_name or basename(file_path)

    # TODO: make sure this closes the file handle
    return FileSide(open(file_path, "rb"), file_type, display_name)


def make_side(url_or_file_path, file_type=None, display_name=None):
    """
    Parsing the URL or file path and looking for the file extension is "ok"
    but works only based on human conventions. The more industrial strength
    approach is to read the beginning of the file or URL and determine the
    type unambiguously from the content.

    :param url_or_file_path: a URL or file path to compare.
    :param file_type: a string like "pdf", "docx", etc, or "guess" (or None) to detect.
    :return: a Side object
    """
    # type: (str, Optional[str])
    guess_type = file_type is None or file_type == "guess"

    if url_or_file_path.startswith("http"):
        url = parse_url(
            url_or_file_path
        )  # parse to get the path component on its own, without query string
        if guess_type:
            file_type = guess_file_type_from_path(url.path)
            if not file_type:
                raise InvalidArgument("file_type", "Unable to infer file type from URL. `file_type` must be specified. This may require "
                                                   "passing a URLSide to comparisons.create rather than a string.")
        display_name = display_name or basename(url.path)
        return URLSide(url.url, file_type, display_name)

    elif url_or_file_path.startswith("file:"):
        url = parse_url(url_or_file_path)
        if url.host:
            raise InvalidPath(
                "File url '{}' must be local only, and not contain host name ('{}')".format(
                    url_or_file_path, url.host
                )
            )

        if not isfile(url.path):
            raise InvalidPath(
                "File url '{}' refers to file '{}' but no such file exists".format(
                    url_or_file_path, url.path
                )
            )

        return side_from_file_path(url.path, file_type, display_name)

    elif isfile(url_or_file_path):
        return side_from_file_path(url_or_file_path, file_type, display_name)

    else:
        raise ValueError(
            "Path is not a URL and not a file that exists: {}".format(url_or_file_path)
        )


def guess_file_type_from_path(path):
    _, file_type = splitext(path)
    return file_type.strip(".").lower()


def guess_file_type_from_url(url):
    url = parse_url(
        url
    )  # parse to get the path component on its own, without query string
    file_type = guess_file_type_from_path(url.path)
    return file_type
