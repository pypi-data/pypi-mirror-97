# -*- coding:utf-8 -*-
__author__ = """David Scheliga"""
__email__ = "david.scheliga@gmx.de"
__version__ = "1.2.1"
__all__ = [
    "doctest_iter_print",
    "doctest_print",
    "doctest_print_list",
    "EditingItem",
    "PandasFormatSpecification",
    "prepare_print",
    "prepare_pandas",
    "print_pandas",
    "round_collections",
    "remove_trailing_tabs",
    "remove_trailing_whitespaces",
    "strip_trailing_whitespaces_and_tabs",
    "repr_posix_path",
    "set_in_quotes",
    "strip_base_path",
]

import copy
import re
import sys
import warnings
from collections import namedtuple
from enum import IntFlag, Enum
from pathlib import Path
from typing import (
    Iterable,
    List,
    Generator,
    Union,
    Match,
    Any,
    Optional,
    Mapping,
    Callable,
    Sequence,
    Tuple,
    Iterator,
    Dict,
)
import numpy as np
import pandas
from pandas import Series, DataFrame


FIND_WHITESPACES = re.compile(r"[\s]+")
WhiteSpaceBlockPosition = namedtuple("WhiteSpaceBlockPosition", "start end")
WhiteSpaceBlockPositions = Sequence[WhiteSpaceBlockPosition]
BlockSectionPosition = namedtuple("BlockSectionPosition", "start end")
BlockSectionPositions = Iterable[BlockSectionPosition]
LINE_BREAK = "\n"


class Platforms(IntFlag):
    WINDOWS = 0
    LINUX = 1

    @classmethod
    def get_current_platform(cls):
        if sys.platform in ["win32"]:
            return Platforms.WINDOWS
        if sys.platform in ["linux"]:
            return Platforms.LINUX


_current_platform = Platforms.get_current_platform()
_REPLACE_TRAILING_WHITESPACE = re.compile(r"[\s]+$", re.MULTILINE)
_REPLACE_TRAILING_TABS = re.compile(r"[\t]+$", re.MULTILINE)
_REPLACE_TRAILING_WHITESPACE_AND_TABS = re.compile(r"[\s\t]+$", re.MULTILINE)


APath = Union[str, Path]


def set_in_quotes(item: Any) -> str:
    """
    Set the string represenation of anything in quotes.

    Args:
        item(Any):
            The item which will be set in quotes.

    Returns:
        str

    Examples:
        >>> from doctestprinter import set_in_quotes
        >>> print(set_in_quotes("   a  "))
        '   a  '
        >>> print(set_in_quotes(""))
        ''
        >>> print(set_in_quotes("None"))
        'None'

        >>> from doctestprinter import doctest_iter_print
        >>> sample = ["o   ", " o  ", "  o ", "   o"]
        >>> doctest_iter_print(sample, edits_item=set_in_quotes)
        'o   '
        ' o  '
        '  o '
        '   o'
    """
    return "'{}'".format(item)


def strip_trailing_tabs(text: str) -> str:
    """
    Strips trailing tabs from the text. Introduced in 1.1.0.

    Args:
        text(str):
            Text from which trailing tabs should be stripd.

    Returns:
        str

    Examples:
        >>> sample_text = "A sample text with\\t\\n trailing tabs.\\t\\n\\t"
        >>> strip_trailing_tabs(sample_text)
        'A sample text with\\n trailing tabs.\\n'
        >>> sample_text = "A sample text with\\t\\n\\ttrailing tabs.\\t\\nEnd.\\t"
        >>> strip_trailing_tabs(sample_text)
        'A sample text with\\n\\ttrailing tabs.\\nEnd.'

    """
    return _REPLACE_TRAILING_TABS.sub("", text)


def strip_trailing_whitespaces(text: str) -> str:
    """
    Strips trailing whitespaces from the text. Introduced in 1.1.0.

    Args:
        text(str):
            Text from which trailing whitespaces should be stripd.

    Returns:
        str

    Examples:
        >>> sample_text = "A sample text with    \\n trailing whitespaces.   \\n   "
        >>> strip_trailing_whitespaces(sample_text)
        'A sample text with\\n trailing whitespaces.'
        >>> sample_text = "A sample text with    \\n trailing whitespaces.   \\nEnd. "
        >>> strip_trailing_whitespaces(sample_text)
        'A sample text with\\n trailing whitespaces.\\nEnd.'

    """
    return _REPLACE_TRAILING_WHITESPACE.sub("", text)


def strip_trailing_whitespaces_and_tabs(text: str) -> str:
    """
    Strips both trailing whitespaces and tabs from the text. Introduced in 1.1.0.

    Args:
        text(str):
            Text from which trailing tabs should be removed.

    Returns:
        str

    Examples:
        >>> sample_text = "A sample text with    \\n trailing whitespaces.   \\n\\t"
        >>> strip_trailing_whitespaces_and_tabs(sample_text)
        'A sample text with\\n trailing whitespaces.'
        >>> sample_text = "A sample text with    \\n trailing whitespaces.   \\nEnd.\\t"
        >>> strip_trailing_whitespaces_and_tabs(sample_text)
        'A sample text with\\n trailing whitespaces.\\nEnd.'
        >>> sample_text = "A sample text with    \\n trailing whitespaces.   \\n   "
        >>> strip_trailing_whitespaces(sample_text)
        'A sample text with\\n trailing whitespaces.'
        >>> sample_text = "A sample text with    \\n trailing whitespaces.   \\nEnd. "
        >>> strip_trailing_whitespaces_and_tabs(sample_text)
        'A sample text with\\n trailing whitespaces.\\nEnd.'

    """
    return _REPLACE_TRAILING_WHITESPACE_AND_TABS.sub("", text)


_ADDS_AN_IDENT_AT_SECOND_LINE = re.compile(LINE_BREAK, re.MULTILINE)


def _indent_block(paragraph: str, indent: Optional[str] = None) -> str:
    """
    Indents a multiline paragraph.

    Args:
        paragraph(str):
            The paragraph which should be indented.

        indent(Optional[str]):
            Custom indentation.

    Returns:
        str

    Test:
        >>> print(_indent_block("a\\nparagraph", indent="--> "))
        --> a
        --> paragraph
        >>> print(_indent_block("a\\nparagraph", indent=None))
            a
            paragraph

    """
    if indent is None:
        indent = "    "
    return _ADDS_AN_IDENT_AT_SECOND_LINE.sub(LINE_BREAK + indent, indent + paragraph)


_windows_drive_letter_matcher = re.compile("^([a-z]):")


def _replace_windows_drive_letter(drive_letter_match: Match) -> str:
    """
    Replaces the windows drive letter with a forward slash encapsulation.

    Notes:
        Is used by :func:`repr_posix_path` using :func:`re.sub`.

    Args:
        drive_letter_match(Match):
            The regular expression matched drive letter.

    Returns:
        str
    """
    drive_letter = drive_letter_match.group(1)
    return "/{}".format(drive_letter)


def repr_posix_path(any_path: Union[str, Path]) -> str:
    """
    Represents the path on a Windows machine as a Posix-Path representation
    turning back slashes to forward slashes.

    Examples:
        >>> repr_posix_path("c:\\\\a\\\\path")
        '/c/a/path'
        >>> repr_posix_path(".\\\\a\\\\path")
        './a/path'
        >>> repr_posix_path(".\\\\a\\\\path")
        './a/path'

    Args:
        any_path(str, Path):
            Any type of path representation.

    Returns:
        str
    """
    busted_windows_drive_letter = _windows_drive_letter_matcher.sub(
        _replace_windows_drive_letter, str(any_path)
    )
    return str(busted_windows_drive_letter).replace("\\", "/")


def strip_base_path(base_path_to_strip: APath, path_to_show: APath) -> str:
    """
    Strips the given *base path* from the *path to show* and performing
    :func:`repr_posix_path` on the result.

    Examples:
        >>> strip_base_path("/a/root/path", "/a/root/path/some/place")
        '... /some/place'
        >>> strip_base_path("\\\\a\\\\root\\\\path", "/a/root/path/some/place")
        '... /some/place'
        >>> strip_base_path("/a/root/path", "\\\\a\\\\root\\\\path\\\\some\\\\place")
        '... /some/place'

    Args:
        base_path_to_strip:
            The base path, which should be removed from the view.

        path_to_show:
            The path which is going to be viewed.

    Returns:
        str
    """
    if _current_platform == Platforms.WINDOWS:
        path_to_show = str(path_to_show).replace("/", "\\")
        base_path_to_strip = str(base_path_to_strip).replace("/", "\\")
    elif _current_platform == Platforms.LINUX:
        path_to_show = str(path_to_show).replace("\\", "/")
        base_path_to_strip = str(base_path_to_strip).replace("\\", "/")
    stripped_path = str(path_to_show).replace(str(base_path_to_strip), "... ")
    return repr_posix_path(stripped_path)


def get_positions_of_whitespace_blocks(text: str) -> WhiteSpaceBlockPositions:
    """

    Args:
        text(str):

    Examples:
        >>> sample_text = "This is a    test string.    "
        >>> white_space_positions = get_positions_of_whitespace_blocks(sample_text)
        >>> for position in white_space_positions:
        ...     print(position)
        WhiteSpaceBlockPosition(start=4, end=5)
        WhiteSpaceBlockPosition(start=7, end=8)
        WhiteSpaceBlockPosition(start=9, end=13)
        WhiteSpaceBlockPosition(start=17, end=18)
        WhiteSpaceBlockPosition(start=25, end=29)
        >>> get_positions_of_whitespace_blocks("")
        []
        >>> sample_text = str(list(iter("abcde")))
        >>> white_space_positions = get_positions_of_whitespace_blocks(sample_text)
        >>> for position in white_space_positions:
        ...     print(position)
        WhiteSpaceBlockPosition(start=5, end=6)
        WhiteSpaceBlockPosition(start=10, end=11)
        WhiteSpaceBlockPosition(start=15, end=16)
        WhiteSpaceBlockPosition(start=20, end=21)

    Returns:
        WhiteSpaceBlockPositions
    """
    assert text is not None, "`text` cannot be None."
    return [
        WhiteSpaceBlockPosition(match.start(), match.end())
        for match in FIND_WHITESPACES.finditer(text)
    ]


def find_section_positions_at_whitespaces(
    text: str, maximum_line_width: int
) -> List[BlockSectionPosition]:
    """
    Finds the positions of sections. Whitespaces marks the used section positions.

    Args:
        text(str):
            The text in which

        maximum_line_width(int):
            The maximum linewidth.

    Returns:
        List[BlockSectionPosition]

    Examples:
        >>> sample_text = str(list(range(60)))
        >>> section_positions = find_section_positions_at_whitespaces(sample_text, 40)
        >>> for section in section_positions:
        ...     print(section)
        BlockSectionPosition(start=0, end=42)
        BlockSectionPosition(start=43, end=86)
        BlockSectionPosition(start=87, end=130)
        BlockSectionPosition(start=131, end=174)
        BlockSectionPosition(start=175, end=218)
        BlockSectionPosition(start=219, end=230)
        >>> sample_text = str(list(iter("abcde")))
        >>> section_positions = find_section_positions_at_whitespaces(sample_text, 40)
        >>> for section in section_positions:
        ...     print(section)
        BlockSectionPosition(start=0, end=25)

    .. doctest:

        >>> sample = str(['strangely_eq', 'ual_wide_ite', 'ms_are_not_s'])
        >>> section_positions = find_section_positions_at_whitespaces(sample, 36)
        >>> for section in section_positions:
        ...     print(section)
        BlockSectionPosition(start=0, end=32)
        BlockSectionPosition(start=33, end=48)
        >>> section_positions = find_section_positions_at_whitespaces(sample, 48)
        >>> for section in section_positions:
        ...     print(section)
        BlockSectionPosition(start=0, end=48)

    """
    assert isinstance(
        text, (str, bytes, bytearray)
    ), "text must be a string or byte-like."
    text_length = len(text)
    full_text_fits_in_one_line = text_length <= maximum_line_width
    if full_text_fits_in_one_line:
        return [BlockSectionPosition(0, text_length)]

    block_positions = get_positions_of_whitespace_blocks(text)
    block_sections = []
    current_line_start_position_within_text = 0
    last_line_start_within_text = 0

    last_block_position = block_positions[-1]
    breaks_into_2_lines = last_block_position.start < maximum_line_width
    if breaks_into_2_lines:
        block_sections = [BlockSectionPosition(0, last_block_position.start)]
        last_line_start_within_text = last_block_position.end
    else:
        for block_position in block_positions:
            try:
                block_start_position_within_text, end_position = block_position
            except ValueError:
                raise ValueError(
                    "A block position must be a 2 item tuple of start & end."
                )

            current_line_end_within_text = (
                block_start_position_within_text
                - current_line_start_position_within_text
            )
            found_section_with_adequate_width = (
                current_line_end_within_text >= maximum_line_width
            )
            if found_section_with_adequate_width:
                block_sections.append(
                    BlockSectionPosition(
                        start=current_line_start_position_within_text,
                        end=block_start_position_within_text,
                    )
                )
                current_line_start_position_within_text = end_position
            last_line_start_within_text = current_line_start_position_within_text

    did_found_block_sections = len(block_sections) > 0
    if did_found_block_sections:
        last_block_position = block_sections[-1][1]
        text_length = text_length
        if last_block_position < text_length:
            block_sections.append(
                BlockSectionPosition(start=last_line_start_within_text, end=text_length)
            )

    return block_sections


def iter_split_text(
    text: str, block_sections: BlockSectionPositions
) -> Generator[str, None, None]:
    """
    Splits a texts by :attribute:`BlockSectionPositions`.

    Args:
        text(str):
            Text which should be split.

        block_sections(BlockSectionPositions):
            Positions by which to split.

    Yields:
        str

    Examples:
        >>> sample_text = str(list(range(60)))
        >>> block_positions = find_section_positions_at_whitespaces(sample_text, 40)
        >>> for line in iter_split_text(sample_text, block_positions):
        ...     print(line)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
        13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
        24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
        35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
        46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
        57, 58, 59]
    """
    for start_position, end_position in block_sections:
        yield text[start_position:end_position]


def break_lines_at_whitespaces(text: str, maximum_line_width: int) -> str:
    """
    Breaks lines at whitespaces.

    Notes:
        Within this implementation the linewidth is not broken by block
        text elements, which exceeds the maximum line width.

    Args:
        text(str):
            Text which should be broken into lines with an maximum line width.

        maximum_line_width(int):
            The maximum line width.

    Returns:
        str

    Examples:
        >>> sample_text = str(list(range(80)))
        >>> result_as_block = break_lines_at_whitespaces(sample_text, 72)
        >>> print(result_as_block)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
        40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
        59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
        78, 79]
        >>> small_list = str(list(iter("abcdefghij")))
        >>> result_as_block = break_lines_at_whitespaces(small_list, 72)
        >>> print(result_as_block)
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    .. doctest:

        >>> sample = str(['strangely_eq', 'ual_wide_ite', 'ms_are_not_s'])
        >>> result_as_block = break_lines_at_whitespaces(sample, maximum_line_width=36)
        >>> print(result_as_block)
        ['strangely_eq', 'ual_wide_ite',
        'ms_are_not_s']
        >>> result_as_block = break_lines_at_whitespaces(sample, maximum_line_width=48)
        >>> print(result_as_block)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s']

    """
    section_positions = find_section_positions_at_whitespaces(
        text=text, maximum_line_width=maximum_line_width
    )
    return LINE_BREAK.join(iter_split_text(text, block_sections=section_positions))


def _try_to_round(potentially_able_to_round: Any, digits: int) -> Any:
    """

    Args:
        potentially_able_to_round:

    Returns:

    .. doctest::

        >>> _try_to_round(1.234567, 4)
        1.2346
        >>> _try_to_round("not a number", 4)
        'not a number'
        >>> import numpy
        >>> _try_to_round(numpy.array([1.234567]), 4)
        array([1.2346])
        >>> from pandas import Series
        >>> _try_to_round(Series([1.234567]), 4)
        0    1.2346
        dtype: float64
        >>> from pandas import DataFrame
        >>> _try_to_round(DataFrame([[1.234567, "not a number"]]), 4)
                0             1
        0  1.2346  not a number
    """
    try:
        round_result = potentially_able_to_round.round(digits)
        return round_result
    except AttributeError:
        pass

    try:
        round_result = round(potentially_able_to_round, digits)
        return round_result
    except TypeError:
        return potentially_able_to_round


def round_collections(item_to_round: Any, digits: int = 3) -> Any:
    """
    Rounds items within collections (dict, list, tuple). This method also
    supports object, which implements a *round(digits)* method.

    Args:
        item_to_round(Any):
            An item with the potential to be rounded. If the item cannot be
            rounded it will be returned instead.

        digits(int):
            Remaining digits of the rounded number. Default is 3.

    Returns:
        Any

    Examples:

        >>> sample_dict = {"a_number": 1.234567, "not": "a number"}
        >>> round_collections(item_to_round=sample_dict, digits=4)
        {'a_number': 1.2346, 'not': 'a number'}
        >>> sample_list = [1.234567, "not a number"]
        >>> round_collections(item_to_round=sample_list, digits=4)
        [1.2346, 'not a number']
        >>> sample_tuple = (1.234567, "not a number")
        >>> round_collections(item_to_round=sample_tuple, digits=4)
        (1.2346, 'not a number')

        Invoking the *round(digit)* method of objects.

        >>> import numpy
        >>> sample_array = numpy.array([1.234567])
        >>> round_collections(item_to_round=sample_array, digits=4)
        array([1.2346])
        >>> from pandas import Series
        >>> sample_series = Series([1.234567])
        >>> round_collections(item_to_round=sample_series, digits=4)
        0    1.2346
        dtype: float64
        >>> from pandas import DataFrame
        >>> sample_frame = DataFrame([[1.234567, "not a number"]])
        >>> round_collections(item_to_round=sample_frame, digits=4)
                0             1
        0  1.2346  not a number

        Or just do nothing.

        >>> round_collections(item_to_round="nothing at all", digits=4)
        'nothing at all'

    """
    if isinstance(item_to_round, dict):
        round_result = {
            key: _try_to_round(item, digits) for key, item in item_to_round.items()
        }
        return round_result
    if isinstance(item_to_round, list):
        round_result = [_try_to_round(item, digits) for item in item_to_round]
        return round_result
    if isinstance(item_to_round, tuple):
        round_result = [_try_to_round(item, digits) for item in item_to_round]
        return tuple(round_result)
    return _try_to_round(potentially_able_to_round=item_to_round, digits=digits)


def doctest_print_list(object_to_print: Iterable, line_width: int = 72):
    """
    Print the content of an Iterable breaking the resulting string at whitespaces.

    Args:
        object_to_print(Any):
            The object of which a block should be printed.

        line_width(int):
            The line width on which the resulting text is broken at whitespaces.

    Examples:
        >>> sample_object = list(range(80))
        >>> doctest_print_list(sample_object)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
        40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
        59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
        78, 79]
        >>> small_list = list(iter("abcdefghij"))

    """
    string_representation = str(object_to_print)
    prepared_print_representation = break_lines_at_whitespaces(
        string_representation, maximum_line_width=line_width
    )
    print(prepared_print_representation)


def prepare_print(
    anything_to_print: Any,
    max_line_width: Optional[int] = 0,
    indent: Optional[str] = None,
) -> str:
    """
    Prepares anything for printing.

    Notes:
        The argument *max_line_width* will break lines a whitespaces. If the
        single text exceeds the maximum linewidth it will not be broken within
        this implementation.

    Args:
        anything_to_print(Any):
            Anything which will be converted into a string and postprocessed,
            with default methods.

        max_line_width(Optional[int]):
            Sets the maximum linewidth of the print.

        indent(str):
            Additional indentation added to the docstring.

    Returns:
       str

    Examples:
        >>> test_text = (
        ...     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed"
        ...     " do eiusmod tempor      incididunt ut labore et dolore magna"
        ...     " aliqua. Ut enim ad  minim veniam, quis nostrud exercitation"
        ...     " ullamco laboris  nisi ut  aliquip  ex ea commodo consequat."
        ... )
        >>> print(prepare_print(test_text[:84]))
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
        >>> print(prepare_print(test_text, max_line_width=60))
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
        do eiusmod tempor      incididunt ut labore et dolore magna aliqua.
        Ut enim ad  minim veniam, quis nostrud exercitation ullamco laboris
        nisi ut  aliquip  ex ea commodo consequat.
        >>> print(prepare_print(test_text, max_line_width=60, indent="    "))
            Lorem ipsum dolor sit amet, consectetur adipiscing elit,
            sed do eiusmod tempor      incididunt ut labore et dolore
            magna aliqua. Ut enim ad  minim veniam, quis nostrud exercitation
            ullamco laboris  nisi ut  aliquip  ex ea commodo consequat.
        >>> small_list = list(iter("abcdefghij"))
        >>> print(prepare_print(small_list))
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        >>> print(prepare_print(small_list, max_line_width=60))
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    .. doctest:

        >>> sample = ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s', 'shown_here__']
        >>> doctest_print(sample, max_line_width=49)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s',
        'shown_here__']
        >>> doctest_print(sample, max_line_width=60)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s',
        'shown_here__']
        >>> doctest_print(sample, max_line_width=64)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s', 'shown_here__']

        >>> sample = ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s']
        >>> doctest_print(sample, max_line_width=36)
        ['strangely_eq', 'ual_wide_ite',
        'ms_are_not_s']
        >>> sample = ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s']
        >>> doctest_print(sample, max_line_width=48)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s']

    """
    string_representation = str(anything_to_print)
    prepared_print_representation = strip_trailing_whitespaces_and_tabs(
        text=string_representation
    )
    if indent is not None:
        indent = str(indent)
        indent_count = len(indent)
    else:
        indent_count = 0
    if max_line_width > 0:
        prepared_print_representation = break_lines_at_whitespaces(
            prepared_print_representation,
            maximum_line_width=max_line_width - indent_count,
        )
    if indent is not None:
        prepared_print_representation = _indent_block(
            paragraph=prepared_print_representation, indent=indent
        )
    return prepared_print_representation


def doctest_print(
    anything_to_print: Any,
    max_line_width: Optional[int] = 0,
    indent: Optional[str] = None,
):
    """
    The general printing method for doctests.

    Notes:
        The argument *max_line_width* will break lines a whitespaces. If the
        single text exceeds the maximum linewidth it will not be broken within
        this implementation.

    Args:
        anything_to_print(Any):
            Anything which will be converted into a string and postprocessed,
            with default methods.

        max_line_width(Optional[int]):
            Sets the maximum linewidth of the print.

        indent(str):
            Additional indentation added to the docstring.

    Examples:
        >>> test_text = (
        ...     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed"
        ...     " do eiusmod tempor      incididunt ut labore et dolore magna"
        ...     " aliqua. Ut enim ad  minim veniam, quis nostrud exercitation"
        ...     " ullamco laboris  nisi ut  aliquip  ex ea commodo consequat."
        ... )
        >>> doctest_print(test_text[:84])
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
        >>> doctest_print(test_text, max_line_width=60)
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
        do eiusmod tempor      incididunt ut labore et dolore magna aliqua.
        Ut enim ad  minim veniam, quis nostrud exercitation ullamco laboris
        nisi ut  aliquip  ex ea commodo consequat.
        >>> doctest_print(test_text, max_line_width=60, indent="    ")
            Lorem ipsum dolor sit amet, consectetur adipiscing elit,
            sed do eiusmod tempor      incididunt ut labore et dolore
            magna aliqua. Ut enim ad  minim veniam, quis nostrud exercitation
            ullamco laboris  nisi ut  aliquip  ex ea commodo consequat.
        >>> small_list = list(iter("abcdefghij"))
        >>> doctest_print(small_list)
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        >>> doctest_print(small_list, max_line_width=60)
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    .. doctest:

        >>> sample = ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s', 'shown_here__']
        >>> doctest_print(sample, max_line_width=49)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s',
        'shown_here__']
        >>> doctest_print(sample, max_line_width=60)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s',
        'shown_here__']
        >>> doctest_print(sample, max_line_width=64)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s', 'shown_here__']

        >>> sample = ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s']
        >>> doctest_print(sample, max_line_width=36)
        ['strangely_eq', 'ual_wide_ite',
        'ms_are_not_s']
        >>> sample = ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s']
        >>> doctest_print(sample, max_line_width=48)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s']

    """
    print(
        prepare_print(
            anything_to_print=anything_to_print,
            max_line_width=max_line_width,
            indent=indent,
        )
    )


def doctest_iter_print(
    iterable_to_print: Union[Mapping, Iterable],
    max_line_width: Optional[int] = 0,
    indent: Optional[str] = None,
    edits_item: Optional[Callable[[Any], Any]] = None,
):
    """
    Prints the first level of the iterable or mapping.

    Args:
        iterable_to_print(Union[Mapping, Iterable]):
            A Mapping or Iterable which first level will be iterated and printed.

        max_line_width(Optional[int]):
            Sets the maximum linewidth of the print.

        indent(Optional[str]):
            Additional indentation. The items of mappings will be indented
            additionally.

        edits_item(Callable[[Any], Any]):
            A callable which takes the 1st level item and returing the
            state, which should be printed.

    Examples:
        >>> sample_mapping = {"a": "mapping  ", "with": 3, "i": "tems  "}
        >>> doctest_iter_print(sample_mapping)
        a:
          mapping
        with:
          3
        i:
          tems
        >>> doctest_iter_print(sample_mapping, indent="..")
        ..a:
        ....mapping
        ..with:
        ....3
        ..i:
        ....tems
        >>> doctest_iter_print([1, 2, {"a": "mapping  ", "with": 3, "i": "tems  "}])
        1
        2
        {'a': 'mapping  ', 'with': 3, 'i': 'tems  '}
        >>> doctest_iter_print(["abc", "abcd", "abcde"], edits_item=lambda x: x[:3])
        abc
        abc
        abc
        >>> doctest_iter_print({"edit": 1, "item": 2}, edits_item=lambda x: x**2)
        edit:
          1
        item:
          4
        >>> sample_dict = {"first_level": {"second": "level", "a number": 1.234567}}
        >>> doctest_iter_print(sample_dict, edits_item=round_collections)
        first_level:
          {'second': 'level', 'a number': 1.235}
    """
    edit_item_before_print = edits_item is not None
    if isinstance(iterable_to_print, Mapping):
        if indent is None:
            mapping_indent = "  "
        else:
            mapping_indent = str(indent) * 2
        for key in iterable_to_print:
            item_to_print = iterable_to_print[key]
            if edit_item_before_print:
                prepared_item = edits_item(item_to_print)
            else:
                prepared_item = item_to_print
            doctest_print(
                "{}:".format(str(key)), max_line_width=max_line_width, indent=indent
            )
            doctest_print(
                prepared_item, max_line_width=max_line_width, indent=mapping_indent
            )
    elif isinstance(iterable_to_print, Iterable):
        for item_to_print in iterable_to_print:
            if edit_item_before_print:
                prepared_item = edits_item(item_to_print)
            else:
                prepared_item = item_to_print
            doctest_print(prepared_item, max_line_width=max_line_width, indent=indent)


########################################################################################
# Pandas section
########################################################################################

COLUMN_VALUE_SPLITTER = "..."
"""
Default splitter in between leading and trailing rows of column representations.
"""

SMALL_COLUMN_VALUE_SPLITTER = ".."
"""
Splitter in between leading and trailing rows, if the column width is small.
"""

_INDEX_VALUE_FORMAT_DELIMITER = "#"
"""
Delimiter splitting the format specifications for index and value columns. 
"""

_DEFAULT_COLUMN_SPACER = 2
"""
Default spacer between columns of DataFrame and Series representations.
"""

_DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH = 16
"""
Default maximum column title width at which the title will be cut.
"""

_DEFAULT_SHORTEN_ROWS_AT = 60
"""
Default count of rows beyond which representations are shown within the shortened
representation.
"""

_SHORTENED_CAP_ROW_COUNT = 5
"""
Default count of leading and trailing rows within the shortened representation.
"""

_DEFAULT_PANDAS_FORMATS = "{:>g}#{:>g}"
"""
Default format specifications for index and value columns.
"""

_DETECTS_SOLE_NAN_REPRESENTATION = re.compile(r"^\s*NaN\s*$")
"""
For detecting literal 'NaN' value within Series.
"""


_DECODES_FORMAT_SPECIFICATION = re.compile(
    r"{:?(?P<align>[<>=^]?)?"
    r"(?P<width>\d+)?"
    r"(?P<precision>\.\d+)?"
    r"(?P<repr_type>[bcdeEfFgGnosxX%]?)?}"
)
"""
Decodes format specification like {:>1.2f}. Fill chars are not supported.
"""

_SPLITS_INDEX_AND_VALUE_FORMATS = re.compile(
    r"(?P<index_formats>({.*?})+)#(?P<values_formats>({.*?})+)"
)
"""
For splitting groups format specifications for index and value columns.
Like '{:1}{:2}#{:3}{:4}' into '{:1}{:2}' '{:3}{:4}'
"""

_SPLITS_FORMATS = re.compile(r"({.*?})")
"""
For splitting of groups into single format specifications.
"""

_TEST_NUMBER = 1.0


class PandasFormatSpecification(Mapping):
    """
    .. doctest::

        >>> from doctestprinter import PandasFormatSpecification
        >>> default_specification = PandasFormatSpecification()
        >>> default_specification
        {:>}
        >>> len(default_specification)
        4
        >>> list(default_specification)
        ['align', 'width', 'precision', 'repr_type']
        >>> sample_spec = PandasFormatSpecification("=", 2, ".4", "f")
        >>> sample_spec.align
        '='
        >>> sample_spec.width
        2
        >>> sample_spec.precision
        '.4'
        >>> sample_spec.repr_type
        'f'

        Comparing format specifications

        >>> sample_spec == "{:=2.4f}"
        True
        >>> sample_spec == PandasFormatSpecification.from_string("{:=2.4f}")
        True
        >>> sample_spec == 2
        Traceback (most recent call last):
        ...
        TypeError: PandasFormatSpecification does not support equal comparison with type '<class 'int'>'.
    """

    DEFAULT_SPECIFIERS = {
        "align": ">",
        "width": "",
        "precision": "",
        "repr_type": "",
    }

    def __init__(
        self,
        align: Optional[str] = None,
        width: Optional[Union[str, int]] = None,
        precision: Optional[str] = None,
        repr_type: Optional[str] = None,
        enforce_defaults: bool = True,
    ):
        """
        A helper class to carry the format specification.

        Args:
            align(str):
                Cell alignment.

            width(Union[str, int]):
                Predefined width of the cell. Is overruled by larger cell content
                and title.

            precision(str):
                Precision with leading dot.

            repr_type(str):
                Format type for numbers.

        Examples:

            >>> from doctestprinter import PandasFormatSpecification
            >>> default_specification = PandasFormatSpecification()
            >>> default_specification
            {:>}
            >>> len(default_specification)
            4
            >>> list(default_specification)
            ['align', 'width', 'precision', 'repr_type']
            >>> sample_spec = PandasFormatSpecification("=", 2, ".4", "f")
            >>> sample_spec.align
            '='
            >>> sample_spec.width
            2
            >>> sample_spec.precision
            '.4'
            >>> sample_spec.repr_type
            'f'

            Comparing format specifications

            >>> sample_spec == "{:=2.4f}"
            True
            >>> sample_spec == PandasFormatSpecification.from_string("{:=2.4f}")
            True
            >>> sample_spec == 2
            Traceback (most recent call last):
            ...
            TypeError: PandasFormatSpecification does not support equal comparison with type '<class 'int'>'.
        """
        if enforce_defaults:
            self._specifiers = PandasFormatSpecification.set_defaults(
                align=align, width=width, precision=precision, repr_type=repr_type
            )
        else:
            self._specifiers = copy.deepcopy(
                PandasFormatSpecification.DEFAULT_SPECIFIERS
            )
            if align is not None:
                self._specifiers["align"] = align
            if width is not None:
                self._specifiers["width"] = width
            if precision is not None:
                self._specifiers["precision"] = precision
            if repr_type is not None:
                self._specifiers["repr_type"] = repr_type
        self._specification = self.encode_format(**self._specifiers)

    def __repr__(self):
        return self._specification

    def __eq__(self, other):
        if isinstance(other, PandasFormatSpecification):
            return other.specification == self.specification
        if isinstance(other, str):
            return other == self.specification
        raise TypeError(
            "{} does not support equal comparison with type '{}'."
            "".format(self.__class__.__name__, type(other))
        )

    @staticmethod
    def set_defaults(
        align: Optional[str] = None,
        width: Optional[Union[str, int]] = None,
        precision: Optional[str] = None,
        repr_type: Optional[str] = None,
    ) -> Dict[str, Union[int, str]]:
        """
        Empty strings or None are replaced by defaults.

        Args:
            align(str):
                Cell alignment.

            width(Union[str, int]):
                Predefined width of the cell. Is overruled by larger cell content
                and title.

            precision(str):
                Precision with leading dot.

            repr_type(str):
                Format type for numbers.


        Returns:
            FormatSpecification

        Examples:
            >>> from doctestprinter import PandasFormatSpecification
            >>> PandasFormatSpecification.set_defaults()
            {'align': '>', 'width': '', 'precision': '', 'repr_type': ''}
            >>> PandasFormatSpecification.set_defaults("=", "8", ".4", "f")
            {'align': '=', 'width': '8', 'precision': '.4', 'repr_type': 'f'}

        """
        default_specifiers = copy.deepcopy(PandasFormatSpecification.DEFAULT_SPECIFIERS)
        if align is not None and align:
            default_specifiers["align"] = align
        width_as_str = str(width)
        if width is not None and width_as_str:
            default_specifiers["width"] = width_as_str
        if precision is not None and precision:
            default_specifiers["precision"] = precision
        if repr_type is not None and repr_type:
            default_specifiers["repr_type"] = repr_type
        return default_specifiers

    def for_object(self):
        """

        Returns:

        Examples:

            >>> from doctestprinter import PandasFormatSpecification
            >>> sample_spec = PandasFormatSpecification.from_string("{:>8.4f}")
            >>> sample_spec.for_object()
            {:>8}

        """
        return PandasFormatSpecification(align=self.align, width=self.width)

    @property
    def specification(self):
        return self._specification

    def with_new_entries(self, **new_entries):
        """

        Args:
            **new_entries:

        Returns:

        Examples:
            >>> from doctestprinter import PandasFormatSpecification
            >>> sample_spec = PandasFormatSpecification(width=8, repr_type="f")
            >>> sample_spec
            {:>8f}
            >>> sample_spec.with_new_entries(align="", repr_type="g")
            {:8g}
        """
        new_specifiers = self._specifiers.copy()
        new_specifiers.update(new_entries)
        return PandasFormatSpecification(**new_specifiers, enforce_defaults=False)

    @staticmethod
    def encode_format(
        align: str,
        width: str,
        precision: str,
        repr_type: str,
    ) -> str:
        """

        Args:
            align(str):
                Alignment of the content within the cell.

            width(Union[str, int]):
                Predefined width of the cell. Is overruled by larger cell content
                and title.

            precision(str):
                Precision with leading dot.

            repr_type(str):
                Format type for numbers.

        Returns:
            str

        Examples:
            >>> from doctestprinter import PandasFormatSpecification
            >>> PandasFormatSpecification.encode_format("", "", "", "")
            '{}'
            >>> PandasFormatSpecification.encode_format("", "8", "", "")
            '{:8}'
        """
        no_align = align is not None and not align
        no_width = width is not None and not width
        no_precision = precision is not None and not precision
        no_repr_type = repr_type is not None and not repr_type

        no_specific_specification = (
            no_align and no_width and no_precision and no_repr_type
        )
        if no_specific_specification:
            colon = ""
        else:
            colon = ":"
        return "{{{colon}{align}{width}{precision}{repr_type}}}".format(
            colon=colon,
            align=align,
            width=width,
            precision=precision,
            repr_type=repr_type,
        )

    @staticmethod
    def decode_specification(format_definition: str) -> dict:
        """
        Decodes a format definition into its parts.

        Args:
            format_definition:
                A string format definiton.

        Returns:
            dict:
                Format parts *align*, *width*, *precision* and *reprtype*.

        Examples:
            >>> from doctestprinter import PandasFormatSpecification
            >>> test_function = PandasFormatSpecification.decode_specification
            >>> PandasFormatSpecification.decode_specification("")
            Traceback (most recent call last):
            ...
            ValueError: Minimum of '{}' as format_definition is mandatory.
            >>> PandasFormatSpecification.decode_specification("{}")
            {'align': '', 'width': '', 'precision': '', 'repr_type': ''}
            >>> PandasFormatSpecification.decode_specification("{:8}")
            {'align': '', 'width': '8', 'precision': '', 'repr_type': ''}
            >>> PandasFormatSpecification.decode_specification("{:.4}")
            {'align': '', 'width': '', 'precision': '.4', 'repr_type': ''}
            >>> PandasFormatSpecification.decode_specification("{:8f}")
            {'align': '', 'width': '8', 'precision': '', 'repr_type': 'f'}
            >>> PandasFormatSpecification.decode_specification("{:12.4}")
            {'align': '', 'width': '12', 'precision': '.4', 'repr_type': ''}
            >>> PandasFormatSpecification.decode_specification("{:<.8}")
            {'align': '<', 'width': '', 'precision': '.8', 'repr_type': ''}
            >>> PandasFormatSpecification.decode_specification("{:=12.12f}")
            {'align': '=', 'width': '12', 'precision': '.12', 'repr_type': 'f'}
            >>> PandasFormatSpecification.decode_specification("{:6.f}")
            Traceback (most recent call last):
            ...
            ValueError: '{:6.f}' is not correct. Format specifier missing precision
            >>> PandasFormatSpecification.decode_specification("{6.f}")
            Traceback (most recent call last):
            ...
            ValueError: The format specifier '{6.f}' has probably the colon missing.
        """
        if not format_definition:
            raise ValueError("Minimum of '{}' as format_definition is mandatory.")
        try:
            format_definition.format(1.0)
        except ValueError as e:
            raise ValueError(
                "'{}' is not correct. {}".format(format_definition, e.args[0])
            )
        except (AttributeError, IndexError):
            raise ValueError(
                "The format specifier '{}' has probably the colon missing."
                "".format(format_definition)
            )
        match = _DECODES_FORMAT_SPECIFICATION.match(format_definition)
        return match.groupdict(default="")

    @staticmethod
    def split_formats(formats: str) -> List[str]:
        """

        Args:
            formats:

        Returns:

        Examples:
            >>> from doctestprinter import PandasFormatSpecification
            >>> PandasFormatSpecification.split_formats("{:1}{:2}")
            ['{:1}', '{:2}']
        """
        return _SPLITS_FORMATS.findall(formats)

    @staticmethod
    def from_string(specification: str) -> "PandasFormatSpecification":
        """

        Args:
            specification:

        Returns:

        Examples:
            >>> from doctestprinter import PandasFormatSpecification
            >>> PandasFormatSpecification.from_string("{}")
            {:>}
            >>> PandasFormatSpecification.from_string("{:>}")
            {:>}
            >>> PandasFormatSpecification.from_string("{:8}")
            {:>8}
            >>> PandasFormatSpecification.from_string("{:.4g}")
            {:>.4g}
        """
        specifiers = PandasFormatSpecification.decode_specification(specification)
        return PandasFormatSpecification(**specifiers)

    @staticmethod
    def parse_format_specifiers(
        column_formats: str, column_count: Optional[int] = None
    ) -> List[dict]:
        """
        Parses a string containing a group of format specification fields.
        Returning dictionaries with their specifiers in the process. Optionally
        for a targetted amount of columns.

        Args:
            column_formats(str):
                A group of format specifification fields e.g. '{:>1}{:<2}'.

            column_count(int, optionsl):
                The count of column for which the format specifications
                are destined to.

        Returns:
            List[dict]

        Examples:
            >>> from doctestprinter import PandasFormatSpecification, doctest_iter_print
            >>> test_function = PandasFormatSpecification.parse_format_specifiers
            >>> doctest_iter_print(test_function("{:.2}{:.8}", 4))
            {'align': '', 'width': '', 'precision': '.2', 'repr_type': ''}
            {'align': '', 'width': '', 'precision': '.8', 'repr_type': ''}
            {'align': '', 'width': '', 'precision': '.8', 'repr_type': ''}
            {'align': '', 'width': '', 'precision': '.8', 'repr_type': ''}
            >>> doctest_iter_print(test_function("{:.2}{:.8}{:>}{:>}", 2))
            {'align': '', 'width': '', 'precision': '.2', 'repr_type': ''}
            {'align': '', 'width': '', 'precision': '.8', 'repr_type': ''}
            >>> doctest_iter_print(test_function("{:2}{:.8}{:>12.0f}"))
            {'align': '', 'width': '2', 'precision': '', 'repr_type': ''}
            {'align': '', 'width': '', 'precision': '.8', 'repr_type': ''}
            {'align': '>', 'width': '12', 'precision': '.0', 'repr_type': 'f'}
        """
        format_definitions = PandasFormatSpecification.split_formats(
            formats=column_formats
        )
        parsed_definitions = []
        decodes_format_string = PandasFormatSpecification.decode_specification
        for raw_definition in format_definitions:
            decoded_definition = decodes_format_string(raw_definition)
            parsed_definitions.append(decoded_definition)
        if column_count is None:
            return parsed_definitions
        if column_count <= len(parsed_definitions):
            return parsed_definitions[:column_count]
        missing_count = column_count - len(parsed_definitions)
        missing_definitions = [parsed_definitions[-1]] * missing_count
        parsed_definitions = parsed_definitions + missing_definitions
        return parsed_definitions

    @staticmethod
    def parse_format_specifications(
        column_formats: str, column_count: Optional[int] = None
    ) -> List["PandasFormatSpecification"]:
        format_specs = []
        for specifiers in PandasFormatSpecification.parse_format_specifiers(
            column_formats=column_formats, column_count=column_count
        ):
            format_specs.append(PandasFormatSpecification(**specifiers))
        return format_specs

    def format(self, *args, **kwargs):
        try:
            return self._specification.format(*args, **kwargs)
        except ValueError as e:
            raise ValueError(
                "Specifier '{}' doesn't work for the values. You need to adjust\nthe"
                " format specification. Most probably string values are used with a\n"
                "format specification for numbers. {}"
                "".format(self._specification, e.args[0])
            )
        except TypeError as e:
            raise TypeError(
                "Specifier '{}' doesn't work with an object within the series. {}"
                "".format(self._specification, e.args[0])
            )

    def __getitem__(self, key):
        return self._specifiers[key]

    def __len__(self) -> int:
        return 4

    def __iter__(self) -> Iterator[str]:
        return iter(self._specifiers)

    @property
    def align(self):
        return self._specifiers["align"]

    @property
    def width(self):
        internal_width = self._specifiers["width"]
        if internal_width:
            return int(internal_width)
        return internal_width

    @property
    def precision(self):
        return self._specifiers["precision"]

    @property
    def repr_type(self):
        return self._specifiers["repr_type"]


class KeepsFirstOfLocalDuplicates(object):
    """
    Examples:
        >>> from pandas import Series
        >>> from doctestprinter import doctest_print, set_in_quotes
        >>> sample_series = Series(list(iter("aaabbcacccbbb")))
        >>> only_first_local_items = sample_series.map(
        ...     KeepsFirstOfLocalDuplicates(replacement="")
        ... )
        >>> only_first_local_items.to_list()
        ['a', '', '', 'b', '', 'c', 'a', 'c', '', '', 'b', '', '']

    """

    def __init__(self, replacement: Optional[Any] = None):
        self._previous_value = None
        self._replacement = replacement

    def __call__(self, current_value):
        if current_value != self._previous_value:
            self._previous_value = current_value
            return current_value
        return self._replacement


class EBlankTitleSpacer(Enum):
    NO_SPACER = "none"
    ABOVE = "above"
    BELOW = "below"


class _PandasColumn(object):
    def __init__(
        self,
        column: Series,
        format_spec: PandasFormatSpecification,
        title_align: str,
        modifier: Optional[Callable[[str], str]] = None,
    ):
        assert isinstance(
            format_spec, (str, PandasFormatSpecification)
        ), "format_spec should be string or PandasFormatSpecification."
        self._column = column
        self._format_spec = format_spec
        self._title_align = title_align
        self._modifier = modifier

    def __repr__(self):
        return "{}({} values, format: {}, title_align: {})" "".format(
            self.__class__.__name__,
            len(self._column),
            self._format_spec.specification,
            self._title_align,
        )

    def prepare_repr(
        self, max_line_count, max_title_width, title_spacer: EBlankTitleSpacer
    ) -> Series:
        preformatted_column = _format_series(
            series_to_print=self._column,
            target_format=self._format_spec,
            max_line_count=max_line_count,
            max_title_width=max_title_width,
        )
        if self._modifier is not None:
            preformatted_column = preformatted_column.map(self._modifier)

        column_title, adjusted_column = _adjust_title_and_formatted_series_width(
            preformatted_series=preformatted_column,
            cell_align=self._format_spec.align,
            title_align=self._title_align,
            max_title_width=max_title_width,
        )

        if title_spacer == EBlankTitleSpacer.NO_SPACER:
            return pandas.concat([Series(column_title), adjusted_column])

        blank_spacer = " " * len(column_title)
        if title_spacer == EBlankTitleSpacer.BELOW:
            return pandas.concat(
                [Series([column_title, blank_spacer]), adjusted_column]
            )

        if title_spacer == EBlankTitleSpacer.ABOVE:
            return pandas.concat(
                [Series([blank_spacer, column_title]), adjusted_column]
            )


def _lower_nan_representation(cell_text: str) -> str:
    """

    Args:
        cell_text:

    Returns:

    .. doctest::

        >>> # access to private member for testing only
        >>> # noinspection PyProtectedMember
        >>> from doctestprinter import _lower_nan_representation
        >>> _lower_nan_representation("NaN")
        'nan'
        >>> _lower_nan_representation("NaN   ")
        'nan   '
        >>> _lower_nan_representation(" NaN ")
        ' nan '
        >>> _lower_nan_representation("  NaN ")
        '  nan '
        >>> _lower_nan_representation(" NaN ")
        ' nan '
        >>> _lower_nan_representation(" NaN")
        ' nan'
        >>> _lower_nan_representation("NaN ")
        'nan '
        >>> _lower_nan_representation("NaNaNaNaNa Batman")
        'NaNaNaNaNa Batman'

    """
    # In this occasion its all about case sensitivity.
    # noinspection PyPep8Naming
    fast_path_because_pure_NaN = cell_text == "NaN"
    if fast_path_because_pure_NaN:
        return "nan"

    match = _DETECTS_SOLE_NAN_REPRESENTATION.match(cell_text)
    # In this occasion its all about case sensitivity.
    # noinspection PyPep8Naming
    is_sole_NaN_representation = match is not None
    if is_sole_NaN_representation:
        return cell_text.replace("NaN", "nan")
    return cell_text


def _get_multi_index_columns(
    multi_index: pandas.MultiIndex, index_formats: str
) -> List[_PandasColumn]:
    """

    Args:
        multi_index:
        index_formats:

    Returns:
        List[_PandasColumn]

    .. doctest::

        >>> from pandas import MultiIndex
        >>> # access to private member for testing only
        >>> # noinspection PyProtectedMember
        >>> from doctestprinter import (
        ...     doctest_iter_print, _get_multi_index_columns, PandasFormatSpecification
        ... )
        >>> sample_tuples = zip("aabb", "cdcd")
        >>> sample_formats = "{:>}{:>10}"
        >>> sample_index = MultiIndex.from_tuples(sample_tuples)
        >>> sample_columns = _get_multi_index_columns(sample_index, sample_formats)
        >>> doctest_iter_print(sample_columns)
        _PandasColumn(4 values, format: {:>}, title_align: <)
        _PandasColumn(4 values, format: {:>10}, title_align: <)
    """
    frame_of_index = multi_index.to_frame()
    count_of_columns = len(frame_of_index.columns)
    format_specs = PandasFormatSpecification.parse_format_specifiers(
        column_formats=index_formats, column_count=count_of_columns
    )
    last_column_index = count_of_columns - 1
    multi_index_columns = []
    for position, (index_label, index_series) in enumerate(frame_of_index.iteritems()):
        if position < last_column_index:
            multi_index_modifier = KeepsFirstOfLocalDuplicates(" ")
        else:
            multi_index_modifier = None
        index_series.name = multi_index.names[position]
        index_column = _PandasColumn(
            column=index_series,
            format_spec=PandasFormatSpecification(**format_specs[position]),
            title_align="<",
            modifier=multi_index_modifier,
        )
        multi_index_columns.append(index_column)
    return multi_index_columns


def _get_index_columns(
    pandas_index: pandas.Index, index_formats: str
) -> List[_PandasColumn]:
    """

    Args:
        pandas_index:
        index_formats (str):

    Returns:
        List[_PandasColumn]

    .. doctest::

        >>> from pandas import MultiIndex, Index
        >>> # access to private member for testing only
        >>> # noinspection PyProtectedMember
        >>> from doctestprinter import (
        ...     doctest_iter_print, _get_multi_index_columns, PandasFormatSpecification
        ... )
        >>> sample_tuples = zip("aabb", "cdcd")
        >>> sample_formats = "{:>}{:>10}"
        >>> sample_index = MultiIndex.from_tuples(sample_tuples)
        >>> sample_columns = _get_index_columns(sample_index, sample_formats)
        >>> doctest_iter_print(sample_columns)
        _PandasColumn(4 values, format: {:>}, title_align: <)
        _PandasColumn(4 values, format: {:>10}, title_align: <)

        >>> sole_sample_index = Index(list(iter("abc")))
        >>> sample_columns = _get_index_columns(sole_sample_index, sample_formats)
        >>> sample_columns
        [_PandasColumn(3 values, format: {:>}, title_align: <)]
    """
    if isinstance(pandas_index, pandas.MultiIndex):
        return _get_multi_index_columns(
            multi_index=pandas_index, index_formats=index_formats
        )
    index_formats = PandasFormatSpecification.parse_format_specifiers(
        column_formats=index_formats, column_count=1
    )
    index_format_spec = PandasFormatSpecification(**index_formats[0])
    return [
        _PandasColumn(
            pandas_index.to_series(), format_spec=index_format_spec, title_align="<"
        )
    ]


_RETURNS_PRECISION_NUMBERS = re.compile(r"^\s*\d*\.(\d*)\s*$")


def _extract_precision_numbers(number_text: str) -> str:
    """

    Args:
        number_text:

    Returns:

    .. doctest::

        >>> # access to private member for testing only
        >>> # noinspection PyProtectedMember
        >>> from doctestprinter import _extract_precision_numbers
        >>> _extract_precision_numbers("")
        ''
        >>> _extract_precision_numbers("   ")
        ''
        >>> _extract_precision_numbers("   1")
        ''
        >>> _extract_precision_numbers("   1.0   ")
        '0'
        >>> _extract_precision_numbers("1.0")
        '0'
        >>> _extract_precision_numbers("1.234")
        '234'
        >>> _extract_precision_numbers("123.456")
        '456'
    """
    matched_precision = _RETURNS_PRECISION_NUMBERS.match(number_text)
    if matched_precision is None:
        return ""
    return matched_precision.group(1)


def _estimate_precision_width(number_text: str) -> int:
    """

    Args:
        number_text:

    Returns:
        int

    .. doctest::

        >>> # access to private member for testing only
        >>> # noinspection PyProtectedMember
        >>> from doctestprinter import _extract_precision_numbers
        >>> _estimate_precision_width("")
        0
        >>> _estimate_precision_width("   ")
        0
        >>> _estimate_precision_width("   1")
        0
        >>> _estimate_precision_width("   1.0   ")
        1
        >>> _estimate_precision_width("1.0")
        1
        >>> _estimate_precision_width("1.234")
        3
        >>> _estimate_precision_width("123.456")
        3
    """
    return len(_extract_precision_numbers(number_text))


def _estimate_maximum_precision_width(formatted_values: Series) -> int:
    """

    Args:
        formatted_values:

    Returns:

    >>> from pandas import Series
    >>> sample_series = Series([0.0, 0.12, 0.1234, 0.123456])
    >>> formatted_sample = sample_series.map("{:g}".format)
    >>> formatted_sample.to_list()
    ['0', '0.12', '0.1234', '0.123456']
    >>> _estimate_maximum_precision_width(formatted_sample)
    6
    """
    precision_widths = formatted_values.map(_estimate_precision_width)
    maximum_precision_width = precision_widths.max()
    return maximum_precision_width


def _reformat_to_fixed_precision_if_necessary(
    series_to_print: Series,
    preformatted_series: Series,
    format_spec: PandasFormatSpecification,
) -> Series:
    """

    Args:
        series_to_print:
        preformatted_series:
        format_spec:

    Returns:

    .. doctest::

        >>> from pandas import Series
        >>> # access to private member for testing only
        >>> # noinspection PyProtectedMember
        >>> from doctestprinter import (
        ...     _reformat_to_fixed_precision_if_necessary, PandasFormatSpecification
        ... )
        >>> sample_series = Series([0.0, 0.12, 0.1234, 0.21000000001])
        >>> variable_spec = PandasFormatSpecification(repr_type="g")
        >>> formatted_sample = sample_series.map(variable_spec.format)
        >>> _reformat_to_fixed_precision_if_necessary(
        ...     series_to_print=sample_series,
        ...     preformatted_series=formatted_sample,
        ...     format_spec=variable_spec
        ... )
        0    0.0000
        1    0.1200
        2    0.1234
        3    0.2100
        dtype: object
    """
    is_not_a_native_numeric_type = series_to_print.dtype == object
    if is_not_a_native_numeric_type:
        return preformatted_series

    if format_spec.repr_type not in "gG":
        return preformatted_series

    target_precision_width = _estimate_maximum_precision_width(
        formatted_values=preformatted_series
    )
    fixed_precision = ".{}".format(target_precision_width)
    fixed_format_spec = format_spec.with_new_entries(
        precision=fixed_precision, repr_type="f"
    )
    reformatted_series = series_to_print.map(fixed_format_spec.format)
    return reformatted_series


def _series_is_not_a_native_numeric_type(series_to_print: Series) -> bool:
    """

    Args:
        series_to_print:

    Returns:

    .. doctest:

        >>> from doctestprinter import _series_is_not_a_native_numeric_type
        >>> from pandas import Series
        >>> from pathlib import Path
        >>> series_with_path = Series([Path("a/path")])
        >>> _series_is_not_a_native_numeric_type(series_to_print=series_with_path)
        True
    """
    is_not_a_native_numeric_type = series_to_print.dtype == object
    return is_not_a_native_numeric_type


def _format_values_of_series_to_representation(
    series_to_print: Series,
    format_spec: PandasFormatSpecification,
    max_title_width: int,
) -> Series:
    assert isinstance(
        format_spec, (str, PandasFormatSpecification)
    ), "format_spec should be string or PandasFormatSpecification."
    assert isinstance(max_title_width, int), "max_title_width must be an integer."

    if _series_is_not_a_native_numeric_type(series_to_print):
        series_ready_to_format = series_to_print.map(str)
        adjusted_format_spec = format_spec.for_object()
    else:
        series_ready_to_format = series_to_print
        adjusted_format_spec = format_spec

    formatted_values = series_ready_to_format.map(adjusted_format_spec.format)
    formatted_values = _reformat_to_fixed_precision_if_necessary(
        series_to_print=series_to_print,
        preformatted_series=formatted_values,
        format_spec=adjusted_format_spec,
    )
    formatted_values.name = series_to_print.name
    max_item_length = formatted_values.map(len).max()

    column_title = series_to_print.name
    if column_title is not None:
        column_title_width = len(str(column_title))
    else:
        column_title_width = 0

    actual_column_title_width_exceeds_allowed = max_title_width < column_title_width
    if actual_column_title_width_exceeds_allowed:
        column_title_width = max_title_width

    title_width_defines_the_cell_width = max_item_length < column_title_width
    if title_width_defines_the_cell_width:
        max_item_length = column_title_width

    final_formatting = "{{:{}{}}}".format(format_spec.align, max_item_length)

    final_formatted_values = formatted_values.map(final_formatting.format)
    return final_formatted_values


def _adjust_column_name_len(column_name, target_max_length, side=">") -> str:
    """

    Args:
        column_name:
        target_max_length:

    Returns:

    .. doctest::
        >>> _adjust_column_name_len(None, 8)
        '        '
        >>> _adjust_column_name_len("testname", 8)
        'testname'
        >>> _adjust_column_name_len("testname", 4)
        'test'
        >>> _adjust_column_name_len("testname", 10, ">")
        '  testname'
        >>> _adjust_column_name_len("testname", 10, "<")
        'testname  '
    """
    if column_name is None:
        return " " * target_max_length
    if len(column_name) >= target_max_length:
        return column_name[:target_max_length]
    add_whitespace_count = target_max_length - len(column_name)
    additional_whitespaces = " " * add_whitespace_count
    if side == ">":
        return additional_whitespaces + column_name
    return column_name + additional_whitespaces


def _split_formats_to_index_value_groups(all_formats: str) -> Dict[str, str]:
    """

    Args:
        all_formats:

    Returns:

    .. doctest::

        >>> # access to private member for testing only
        >>> # noinspection PyProtectedMember
        >>> from doctestprinter import _split_formats_to_index_value_groups
        >>> _split_formats_to_index_value_groups("{}{}")
        Traceback (most recent call last):
        ...
        ValueError: The format specifications '{}{}' are invalid. {}#{} 'all_formats' for index and values are mandatory.
        >>> _split_formats_to_index_value_groups("{1}")
        {'index_formats': '{1}', 'values_formats': '{1}'}
        >>> _split_formats_to_index_value_groups("{1}#{2}")
        {'index_formats': '{1}', 'values_formats': '{2}'}
        >>> _split_formats_to_index_value_groups("{1}{2}#{3}{4}{5}")
        {'index_formats': '{1}{2}', 'values_formats': '{3}{4}{5}'}
    """
    matched_formats = _SPLITS_INDEX_AND_VALUE_FORMATS.match(all_formats)
    if matched_formats is None:
        formats = _SPLITS_FORMATS.findall(all_formats)
        a_single_formats_count_for_all = len(formats) == 1
        if a_single_formats_count_for_all:
            return {
                "index_formats": formats[0],
                "values_formats": copy.deepcopy(formats[0]),
            }

        raise ValueError(
            "The format specifications '{}' are invalid."
            " {{}}#{{}} 'all_formats' for index and values are mandatory."
            "".format(all_formats)
        )
    return matched_formats.groupdict()


def _format_column_name(
    series_name: Any, align: str, cell_width: int, max_title_width: Optional[int] = None
) -> str:
    """

    Args:
        series_name:
        align:
        cell_width:
        max_title_width:

    Returns:

    .. doctest::

        >>> # access to private member for testing only
        >>> # noinspection PyProtectedMember
        >>> from doctestprinter import _format_column_name
        >>> _format_column_name("y", align=">", cell_width=6)
        '     y'
        >>> _format_column_name("x", align="<", cell_width=6 )
        'x     '
        >>> _format_column_name(
        ...     "A_longer_column_name",
        ...     align=">",
        ...     cell_width=10,
        ... )
        'A_longer_colum..'
        >>> _format_column_name(
        ...     "A_longer_column_name",
        ...     align="<",
        ...     cell_width=10,
        ... )
        'A_longer_colum..'
        >>> _format_column_name(
        ...     "A_longer_column_name",
        ...     align=">",
        ...     cell_width=10,
        ...     max_title_width=25
        ... )
        'A_longer_column_name'
        >>> _format_column_name(
        ...     "A_longer_column_name",
        ...     align=">",
        ...     cell_width=25,
        ... )
        '     A_longer_column_name'
        >>> _format_column_name(
        ...     "A_longer_column_name",
        ...     align="<",
        ...     cell_width=25,
        ... )
        'A_longer_column_name     '
    """
    column_format = "{{:{}{}}}".format(align, cell_width)
    origin_name_length = len(str(series_name))
    formatted_name = column_format.format(series_name)
    if max_title_width is None:
        max_title_width = _DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH
    assert isinstance(max_title_width, int), "max_title_width must be an integer."
    assert 0 < max_title_width, "max_title_width must be greater than 0"

    cell_width_overrides_maximum_title_width = max_title_width < cell_width
    if cell_width_overrides_maximum_title_width:
        max_title_width = cell_width

    if max_title_width < origin_name_length:
        return formatted_name[: max_title_width - 2] + ".."

    if align == "<":
        return formatted_name[:max_title_width]
    return formatted_name[-max_title_width:]


def _format_series(
    series_to_print: Series,
    target_format: Union[str, PandasFormatSpecification],
    max_line_count: int,
    max_title_width: int,
) -> Series:
    """
    Formats a Series according to the given *target format*. This function renders
    all items into string returning a *dtype=object*.

    Args:
        series_to_print:
        target_format:
        max_line_count:
        max_title_width:

    Returns:
        Series

    .. doctest::

        >>> # Shadowing from outer scope for testing
        >>> # noinspection PyShadowingNames
        >>> import numpy as np
        >>> from pandas import Series, Index
        >>> # access to private member for testing only
        >>> # noinspection PyProtectedMember
        >>> from doctestprinter import _format_series, doctest_iter_print, set_in_quotes
        >>> sample_series = Series(
        ...     np.arange(7),
        ...     name="y"
        ... )
        >>> sample_format = PandasFormatSpecification(
        ...     align='>', width='', precision='.1', repr_type='f'
        ... )
        >>> sample_result = _format_series(
        ...     sample_series, sample_format, max_line_count=5, max_title_width=16
        ... )
        >>> doctest_iter_print(
        ...     sample_result.to_list(), edits_item=set_in_quotes
        ... )
        '0.0'
        '1.0'
        ' ..'
        '5.0'
        '6.0'
        >>> sample_series = Series(
        ...     np.linspace(1,5000/3,num=7),
        ...     name="y"
        ... )
        >>> sample_result = _format_series(sample_series, sample_format, 60, 16)
        >>> doctest_iter_print(
        ...     sample_result.to_list(), edits_item=set_in_quotes
        ... )
        '   1.0'
        ' 278.6'
        ' 556.2'
        ' 833.8'
        '1111.4'
        '1389.1'
        '1666.7'
        >>> sample_series = Series(
        ...     list(iter("abc")),
        ...     name="y"
        ... )
        >>> sample_format = PandasFormatSpecification.from_string("{:>4.8f}")
        >>> sample_result = _format_series(sample_series, sample_format, 60, 16)
        >>> doctest_iter_print(
        ...     sample_result.to_list(), edits_item=set_in_quotes
        ... )
        '   a'
        '   b'
        '   c'



    """
    assert isinstance(
        target_format, PandasFormatSpecification
    ), "target_format must by of type PandasFormatSpecification."
    assert isinstance(max_title_width, int), "max_title_width must be an integer."
    if max_line_count < 2:
        max_line_count = 2
    do_cutting_to_max_line_count = max_line_count < len(series_to_print)

    if do_cutting_to_max_line_count:
        half_height = max_line_count // 2
        if half_height < _SHORTENED_CAP_ROW_COUNT:
            cutting_index = half_height
        else:
            cutting_index = _SHORTENED_CAP_ROW_COUNT

        head_part = series_to_print.iloc[:cutting_index]
        tail_part = series_to_print.iloc[-cutting_index:]
        values_to_print = pandas.concat([head_part, tail_part])
    else:
        values_to_print = series_to_print

    formatted_values = _format_values_of_series_to_representation(
        series_to_print=values_to_print,
        format_spec=target_format,
        max_title_width=max_title_width,
    )
    if not do_cutting_to_max_line_count:
        return formatted_values

    first_values = formatted_values.iloc[0]
    current_cell_width = len(first_values)
    used_splitter = COLUMN_VALUE_SPLITTER
    if current_cell_width <= 3:
        used_splitter = SMALL_COLUMN_VALUE_SPLITTER
    splitter_format = "{{:{align}{width}}}".format(
        align=target_format["align"], width=current_cell_width
    )
    formatted_splitter = splitter_format.format(used_splitter)
    split_values = pandas.concat(
        [
            formatted_values.iloc[:cutting_index],
            Series(formatted_splitter),
            formatted_values.iloc[-cutting_index:],
        ]
    )
    split_values.name = series_to_print.name
    return split_values


def _adjust_title_and_formatted_series_width(
    preformatted_series: Series,
    cell_align: str,
    title_align: str,
    max_title_width: Optional[int] = None,
) -> Tuple[str, Series]:
    """

    Args:
        preformatted_series(Series):
            Series which was formatted using the target format specifier.
            Cell width within this *preformatted series* must not be equal.

        cell_align(str):
            The targetted alignment of the column.

        title_align(str):
            The alignment of the column's title.

        max_title_width(int, Optional):
            Maximum allowed width of the title.

    Returns:
        Tuple[str, Series]

    .. doctest::

        >>> from pandas import Series, Index
        >>> # access to private member for testing only
        >>> # noinspection PyProtectedMember
        >>> from doctestprinter import _adjust_title_and_formatted_series_width
        >>> sample_series = Series(
        ...     [1.0, 2.0],
        ...     index=Index([0.1, 0.2], name="x"),
        ...     name="y",
        ...     dtype=float
        ... )
        >>> sample_format = {"align": ">", "width":8, "precision":".0", "repr_type":"f"}
        >>> preformat_sample = _format_values_of_series_to_representation(
        ...     series_to_print=sample_series,
        ...     format_spec=PandasFormatSpecification(**sample_format),
        ...     max_title_width=16
        ... )
        >>> sample_title, final_sample = _adjust_title_and_formatted_series_width(
        ...     preformatted_series=preformat_sample,
        ...     cell_align=sample_format["align"],
        ...     title_align=">"
        ... )
        >>> sample_title
        '       y'
        >>> final_sample
        x
        0.1           1
        0.2           2
        Name: y, dtype: object
        >>> sample_series = Series(
        ...     [1.0, 2.0],
        ...     index=Index([0.1, 0.2], name="x"),
        ...     name="A-pretty-long_title",
        ...     dtype=float
        ... )
        >>> sample_format = {"align": ">", "width":8, "precision":".0", "repr_type":"f"}
        >>> preformat_sample = _format_values_of_series_to_representation(
        ...     series_to_print=sample_series,
        ...     format_spec=PandasFormatSpecification(**sample_format),
        ...     max_title_width=16
        ... )
        >>> sample_title, final_sample = _adjust_title_and_formatted_series_width(
        ...     preformatted_series=preformat_sample,
        ...     cell_align=sample_format["align"],
        ...     title_align=">"
        ... )
        >>> sample_title
        'A-pretty-long_..'
        >>> final_sample
        x
        0.1                   1
        0.2                   2
        Name: A-pretty-long_title, dtype: object


    """
    name_of_series = preformatted_series.name
    cell_length = preformatted_series.str.len()
    min_pre_width_of_cells = cell_length.min()
    max_pre_width_of_cells = cell_length.max()

    if name_of_series is None:
        blank_title = " " * max_pre_width_of_cells
        return blank_title, preformatted_series

    formatted_title = _format_column_name(
        preformatted_series.name,
        align=title_align,
        cell_width=max_pre_width_of_cells,
        max_title_width=max_title_width,
    )
    width_of_title = len(formatted_title)

    all_cells_are_equally_wide = min_pre_width_of_cells == max_pre_width_of_cells
    title_and_all_cells_has_equal_width = width_of_title == all_cells_are_equally_wide
    if title_and_all_cells_has_equal_width:
        return formatted_title, preformatted_series

    assert (
        max_pre_width_of_cells <= width_of_title
    ), "The title's width should not be smaller than the cells width."

    if cell_align == "<":
        final_series = preformatted_series.str.ljust(width_of_title, " ")
    elif cell_align == ">":
        final_series = preformatted_series.str.rjust(width_of_title, " ")
    elif cell_align == "^":
        final_series = preformatted_series.str.center(width_of_title, " ")
    else:
        raise ValueError("Unsupported align specifier '{}'.".format(cell_align))
    return formatted_title, final_series


def _prepare_title_definition(
    index_to_print: pandas.Index, values_column_count: int
) -> List[EBlankTitleSpacer]:
    """
    Prepares the placements of the titles.

    Args:
        index_to_print:
        values_column_count:

    Returns:
        List[EBlankTitleSpacer]

    .. doctest::

        >>> # access to private member for testing only
        >>> # noinspection PyProtectedMember
        >>> from doctestprinter import _prepare_title_definition, doctest_iter_print
        >>> from pandas import Index, MultiIndex
        >>> sample_index = Index(list(iter("abc")))
        >>> sample_multi_index = MultiIndex.from_tuples(zip("ab", "cd"))
        >>> doctest_iter_print(_prepare_title_definition(sample_index, 2))
        EBlankTitleSpacer.NO_SPACER
        EBlankTitleSpacer.NO_SPACER
        EBlankTitleSpacer.NO_SPACER
        >>> doctest_iter_print(_prepare_title_definition(sample_multi_index, 2))
        EBlankTitleSpacer.NO_SPACER
        EBlankTitleSpacer.NO_SPACER
        EBlankTitleSpacer.NO_SPACER
        EBlankTitleSpacer.NO_SPACER
        >>> sample_index.name = "x"
        >>> sample_multi_index.names = ["x1", "x2"]
        >>> doctest_iter_print(_prepare_title_definition(sample_index, 2))
        EBlankTitleSpacer.ABOVE
        EBlankTitleSpacer.BELOW
        EBlankTitleSpacer.BELOW
        >>> doctest_iter_print(_prepare_title_definition(sample_multi_index, 2))
        EBlankTitleSpacer.ABOVE
        EBlankTitleSpacer.ABOVE
        EBlankTitleSpacer.BELOW
        EBlankTitleSpacer.BELOW
    """
    if isinstance(index_to_print, pandas.MultiIndex):
        index_column_count = len(index_to_print.names)
        unique_names_of_index = list(set(index_to_print.names))
        has_no_index_titles = (
            len(unique_names_of_index) == 1 and unique_names_of_index[0] is None
        )
    else:
        index_column_count = 1
        has_no_index_titles = index_to_print.name is None

    if has_no_index_titles:
        total_column_count = index_column_count + values_column_count
        return [EBlankTitleSpacer.NO_SPACER] * total_column_count
    else:
        index_title_spacers = [EBlankTitleSpacer.ABOVE] * index_column_count
        value_title_spacers = [EBlankTitleSpacer.BELOW] * values_column_count
        return index_title_spacers + value_title_spacers


def _generate_dataframe_representation(
    pandas_dataframe: DataFrame,
    all_formats: Optional[str] = None,
    max_line_count: Optional[int] = None,
    max_title_width: Optional[int] = None,
) -> str:
    """
    Prepares the representation of a pandas.Series.

    Args:
        pandas_dataframe(Series):
            Series for which a string representation should be generated.

        all_formats(str; optional):
            Concatenated format specifiers for the index column(s) and
            value column(s). Default `{:>f}#{:>f}`

        max_line_count(int; optional):
            Defines the max lines which should be print. Its half wide is
            used to show either head and tail. Default is 60.

        max_title_width(int; optional):
            Maximum printed width of the column title. Default is 16.


    Returns:
        str

    .. doctest::

        >>> import pandas
        >>> # access to private member for testing only
        >>> # noinspection PyProtectedMember
        >>> from doctestprinter import _generate_series_representation
        >>> from pandas import DataFrame, Index
        >>> # Shadowing from outer scope for testing
        >>> # noinspection PyShadowingNames
        >>> import numpy as np
        >>> sample_frame = DataFrame(
        ...     np.arange(4).reshape(2, 2),
        ...     index=Index([0.1, 0.2], name="x"),
        ...     columns=["y1", "y2"],
        ...     dtype=float
        ... )
        >>> doctest_print(sample_frame)
              y1   y2
        x
        0.1  0.0  1.0
        0.2  2.0  3.0
        >>> doctest_print(_generate_dataframe_representation(sample_frame, "{:.1f}#{:.0f}"))
             y1  y2
        x
        0.1   0   1
        0.2   2   3
        >>> sample_frame = DataFrame(
        ...     np.arange(20).reshape(10, 2),
        ...     index=Index(np.arange(10)*0.1, name="x"),
        ...     columns=["y1", "y2"],
        ...     dtype=float
        ... )
        >>> doctest_print(_generate_dataframe_representation(sample_frame, "{:>.1f}#{:>6.0f}{:>.0f}", max_line_count=7))
                 y1  y2
        x
        0.0       0   1
        0.1       2   3
        0.2       4   5
         ..     ...  ..
        0.7      14  15
        0.8      16  17
        0.9      18  19
        >>> doctest_print(_generate_dataframe_representation(sample_frame, "{:>.1f}", max_line_count=7))
               y1    y2
        x
        0.0   0.0   1.0
        0.1   2.0   3.0
        0.2   4.0   5.0
         ..   ...   ...
        0.7  14.0  15.0
        0.8  16.0  17.0
        0.9  18.0  19.0
    """
    all_formats, max_line_count, max_title_width = _set_defaults_setup(
        all_formats, max_line_count, max_title_width
    )

    split_formats = _split_formats_to_index_value_groups(all_formats=all_formats)
    index_formats = split_formats["index_formats"]
    values_formats = split_formats["values_formats"]

    index_columns = _get_index_columns(
        pandas_dataframe.index, index_formats=index_formats
    )

    value_column_count = len(pandas_dataframe.columns)
    value_format_specifiers = PandasFormatSpecification.parse_format_specifications(
        values_formats, column_count=value_column_count
    )
    all_columns = index_columns
    for spec_index, (label, value_column) in enumerate(pandas_dataframe.iteritems()):
        value_column = _PandasColumn(
            column=value_column,
            format_spec=value_format_specifiers[spec_index],
            title_align=">",
        )
        all_columns.append(value_column)

    title_spacers = _prepare_title_definition(
        index_to_print=pandas_dataframe.index, values_column_count=value_column_count
    )

    return _generate_pandas_representation(
        all_columns, title_spacers, max_line_count, max_title_width
    )


def _set_defaults_setup(
    all_formats, max_line_count, max_title_width
) -> Tuple[str, int, int]:
    """

    Args:
        all_formats:
        max_line_count:
        max_title_width:

    Returns:
        Tuple[str, int, int]:
            all_formats, max_line_count, max_title_width with default values
            if None.

    .. doctest::

        >>> # access to private member for testing only
        >>> # noinspection PyProtectedMember
        >>> from doctestprinter import _set_defaults_setup
        >>> _set_defaults_setup(None, None, None)
        ('{:>g}#{:>g}', 60, 16)
    """
    if all_formats is None:
        all_formats = _DEFAULT_PANDAS_FORMATS
    if max_line_count is None:
        max_line_count = _DEFAULT_SHORTEN_ROWS_AT
    if max_title_width is None:
        max_title_width = _DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH
    return all_formats, max_line_count, max_title_width


def _generate_pandas_representation(
    all_columns: List[_PandasColumn],
    title_spacers: List[EBlankTitleSpacer],
    max_line_count: int,
    max_title_width: int,
):
    assert isinstance(max_line_count, int), "max_line_count must be an integer"
    assert isinstance(max_title_width, int), "max_title_width must be an integer"

    most_left_column = all_columns.pop(0)
    most_left_spacer = title_spacers.pop(0)
    combined_rows = most_left_column.prepare_repr(
        max_line_count=max_line_count,
        max_title_width=max_title_width,
        title_spacer=most_left_spacer,
    )
    for column_index, column in enumerate(all_columns):
        adjusted_column = column.prepare_repr(
            max_line_count=max_line_count,
            max_title_width=max_title_width,
            title_spacer=title_spacers[column_index],
        )
        first_line = adjusted_column.iloc[0]
        column_width = len(first_line)
        final_column_width = column_width + _DEFAULT_COLUMN_SPACER
        final_values = adjusted_column.str.rjust(final_column_width, " ")
        combined_rows += final_values

    first_line = combined_rows.iloc[0]
    first_line_is_blank_then_remove = len(set(first_line)) == 1
    start_index = 0
    if first_line_is_blank_then_remove:
        start_index = 1

    return "\n".join(combined_rows.iloc[start_index:].to_list())


class EditingItem(object):
    def __init__(
        self,
        editor: Callable,
        *editor_args,
        **editor_kwargs,
    ):
        """
        *EditingItem* is a wrapper class for the *edit_item* argument of
        :func:`doctest_iter_print`.

        Args:
            editor(Callable[[Any], Any]):
                A callable which first argument is the item to be edited,
                before printing.

            editor_args:
                Arguments for the *editor*.

            editor_kwargs:
                Keyword arguments for the *editor*.

        Examples:
            *prepare_pandas* accepts 4 arguments. *edits_item* of
            :func:`doctest_iter_print` takes a Callable and passes each item
            within the iteration as the first argument to the *editor*. Therefor
            *edits_pandas* allows to predefine the arguments for any Callable,
            which provides additional functionality.

            >>> from doctestprinter import (
            ...     EditingItem, doctest_iter_print, prepare_pandas
            ... )
            >>> from pandas import DataFrame
            >>> frame_1 = DataFrame.from_records({"Alpha": 1, "Beta": 2}, index=[1.234])
            >>> frame_2 = DataFrame({"Gamma":3, "Delta": 4}, index=[2.345])
            >>> edits_pandas = EditingItem(prepare_pandas, formats="{:>.1f}#{:>8}")
            >>> doctest_iter_print([frame_1, frame_2], edits_item=edits_pandas)
                    Alpha      Beta
            1.2         1         2
                    Gamma     Delta
            2.3         3         4
        """
        self._editor = editor
        self._editor_args = editor_args
        self._editor_kwargs = editor_kwargs

    def __call__(self, item_to_edit: Any) -> str:
        return self._editor(item_to_edit, *self._editor_args, **self._editor_kwargs)


def _generate_series_representation(
    pandas_series: Series,
    all_formats: Optional[str] = None,
    max_line_count: Optional[int] = None,
    max_title_width: Optional[int] = None,
) -> str:
    """
    Prepares the representation of a pandas.Series.

    Args:
        pandas_series:
            The Series to be represented.

        all_formats(str; optional):
            Concatenated format specifiers for the index column(s) and
            value column(s). Default `{:>f}#{:>f}`

        max_line_count(int; optional):
            Defines the max lines which should be print. Its half wide is
            used to show either head and tail. Default is 60.

        max_title_width(int; optional):
            Maximum printed width of the column title. Default is 16.


    Returns:
        str

    .. doctest::

        >>> import pandas
        >>> # access to private member for testing only
        >>> # noinspection PyProtectedMember
        >>> from doctestprinter import _generate_series_representation
        >>> from pandas import Series, Index
        >>> sample_series = Series(
        ...     [1.0, 2.0],
        ...     index=Index([0.1, 0.2], name="x"),
        ...     name="y",
        ...     dtype=float
        ... )
        >>> sample_series
        x
        0.1    1.0
        0.2    2.0
        Name: y, dtype: float64
        >>> print(_generate_series_representation(sample_series, "{:.1f}#{:.0f}"))
        x    y
        0.1  1
        0.2  2
        >>> # Shadowing from outer scope for testing
        >>> # noinspection PyShadowingNames
        >>> import numpy as np
        >>> sample_series = Series(
        ...     np.arange(10),
        ...     index=Index(np.arange(10)*0.1, name="x"),
        ...     name="y",
        ...     dtype=float
        ... )
        >>> print(_generate_series_representation(sample_series, "{:>.1f}#{:>6.0f}", max_line_count=7))
        x         y
        0.0       0
        0.1       1
        0.2       2
         ..     ...
        0.7       7
        0.8       8
        0.9       9
        >>> print(_generate_series_representation(sample_series, "{:>.1f}#{:>.0f}", max_line_count=7))
        x     y
        0.0   0
        0.1   1
        0.2   2
         ..  ..
        0.7   7
        0.8   8
        0.9   9

    """

    all_formats, max_line_count, max_title_width = _set_defaults_setup(
        all_formats, max_line_count, max_title_width
    )
    assert isinstance(max_line_count, int), "max_line_count must be an integer"
    assert isinstance(max_title_width, int), "max_title_width must be an integer"

    split_formats = _split_formats_to_index_value_groups(all_formats=all_formats)
    index_formats = split_formats["index_formats"]
    values_formats = split_formats["values_formats"]

    index_columns = _get_index_columns(pandas_series.index, index_formats=index_formats)

    series_has_only_1_column = 1
    value_format_specifiers = PandasFormatSpecification.parse_format_specifications(
        values_formats, column_count=series_has_only_1_column
    )
    all_columns = index_columns
    value_column = _PandasColumn(
        column=pandas_series,
        format_spec=value_format_specifiers[0],
        title_align=">",
    )
    all_columns.append(value_column)
    title_spacers = [EBlankTitleSpacer.NO_SPACER] * len(all_columns)
    return _generate_pandas_representation(
        all_columns=all_columns,
        title_spacers=title_spacers,
        max_line_count=max_line_count,
        max_title_width=max_title_width,
    )


def prepare_pandas(
    frame_or_series: Optional = None,
    formats: Optional[str] = None,
    max_line_count: Optional[int] = None,
    max_title_width: Optional[int] = None,
) -> str:
    """
    Builds explicitly string representations for *pandas.DataFrame* and
    *pandas.Series* objects.

    Args:
        frame_or_series:
            The DataFrame or Series to be represented.

        formats(str; optional):
            Concatenated format specifiers for the index column(s) and
            value column(s). Default `{:>f}#{:>f}`

        max_line_count(int; optional):
            Defines the max lines which should be print. Its half wide is
            used to show either head and tail. Default is 60.

        max_title_width(int; optional):
            Maximum printed width of the column title. Default is 16.

    Returns:
        str

    Notes:
        For further details see :func:`print_pandas`.
    """
    if frame_or_series is None:
        return "pandas"

    if frame_or_series.empty:
        return str(frame_or_series)

    if isinstance(frame_or_series, Series):
        series_representation = _generate_series_representation(
            pandas_series=frame_or_series,
            all_formats=formats,
            max_line_count=max_line_count,
            max_title_width=max_title_width,
        )
        return series_representation

    if isinstance(frame_or_series, DataFrame):
        dataframe_representation = _generate_dataframe_representation(
            pandas_dataframe=frame_or_series,
            all_formats=formats,
            max_line_count=max_line_count,
            max_title_width=max_title_width,
        )
        return dataframe_representation


def print_pandas(
    frame_or_series: Optional = None,
    formats: Optional[str] = None,
    max_line_count: Optional[int] = None,
    max_title_width: Optional[int] = None,
):
    """
    Prints explicitly *pandas.DataFrame* and *pandas.Series* objects.

    Args:
        frame_or_series:
            The DataFrame or Series to be print.

        formats(str; optional):
            Concatenated format specifiers for the index column(s) and
            value column(s). Default `{:>f}#{:>f}`

        max_line_count(int; optional):
            Defines the max lines which should be print. Its half wide is
            used to show either head and tail. Default is 60.

        max_title_width(int; optional):
            Maximum printed width of the column title. Default is 16.

    .. warning::
        This method doesn't reproduce the exact representation as pandas does.
        This is intentional as this function was written to takle issues regarding
        usage of doctests in combination with pytest.

    Notes:
        This function was written in response to failed doctests in pytest
        due to changed formatting behaviour in between running the doctest
        outside and inside pytest.

        Other reasons are the different *NaN* value representation,
        representation of floats on different operating systems and lack of
        defining a string formatting behavior for each column.

        In between different python versions, which changes between `nan` and `NaN`.
        In cases of running the tests on Linux and Windows on different machines
        the float representation in the footer of a Series print changes leading
        to failed doctests. First problem is solved by lowercase `NaN` to `nan`
        and second case is solved by a changed Series representation.

    Examples:

        .. testsetup::
            >>> from doctestprinter import print_pandas
            >>> from pandas import DataFrame, Index, MultiIndex
            >>> # Shadowing from outer scope for testing
            >>> # noinspection PyShadowingNames
            >>> import numpy as np

        The default format specification is {:>g}. But the intention of this
        function is to define a specific format specification for each test
        to fix the doctest result for any python version within a tox test.

        .. doctest::

            >>> single_index_test_frame = DataFrame(
            ...     np.linspace(1/3, 1000/3, num=4).reshape(2, 2),
            ...     columns=["x", "y"],
            ...     index=Index([0.1, 0.211], name="t")
            ... )
            >>> print_pandas(single_index_test_frame)
                            x        y
            t
            0.100    0.333333  111.333
            0.211  222.333333  333.333
            >>> print_pandas(single_index_test_frame, "{:>.1f}#{:>4.1f}{:>e}")
                     x             y
            t
            0.1    0.3  1.113333e+02
            0.2  222.3  3.333333e+02

        The main task of :func:`print_pandas` is the possibility to fix the
        format of each column within a DataFrame.

        .. doctest::

            >>> index_items = zip("aabb", np.linspace(0.0, 1/3, num=4))
            >>> sample_index = MultiIndex.from_tuples(index_items, names=["x1", "x2"])
            >>> sample_frame = DataFrame(
            ...     np.linspace(1/3, 1000/3, num=12).reshape(4, 3),
            ...     index=sample_index,
            ...     columns=["Alpha", "Beta", "G"]
            ... )
            >>> print_pandas(sample_frame, "{:>4}{:>.2f}#{:.0f}{:.1e}{:.5g}")
                        Alpha     Beta        G
            x1    x2
               a  0.00      0  3.1e+01   60.879
                  0.11     91  1.2e+02  151.697
               b  0.22    182  2.1e+02  242.515
                  0.33    273  3.0e+02  333.333

    """
    doctest_print(
        prepare_pandas(
            frame_or_series=frame_or_series,
            formats=formats,
            max_line_count=max_line_count,
            max_title_width=max_title_width,
        )
    )