from pathlib import Path

import pandas
from pandas import DataFrame, Series
import numpy as np

from doctestprinter import (
    _PandasColumn,
    PandasFormatSpecification,
    EBlankTitleSpacer,
    _format_values_of_series_to_representation,
    _adjust_title_and_formatted_series_width,
    _generate_dataframe_representation,
    _DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH
)


def test_series_example1():
    """

    .. doctest::

        >>> from doctestprinter import doctest_print
        >>> sample_frame = test_series_example1()
        >>> doctest_print(sample_frame)
        x
        1.103000    10.121000
        1.096185    10.237287
        1.076563    10.339548
        1.046500    10.415449
        1.009622    10.455835
        0.970378    10.455835
        0.933500    10.415449
        0.903437    10.339548
        0.883815    10.237287
        0.877000    10.121000
        Name: a longer name, dtype: float64

    """
    angles = np.linspace(0.0, np.pi, num=10)
    x_values = np.cos(angles) * 0.113
    x_values += 0.99
    y_values = np.sin(angles) * 0.34
    y_values += 10.121
    sample_frame = Series(
        y_values, index=pandas.Index(x_values, name="x"), name="a longer name"
    )
    return sample_frame


def test_convert_pandas_series():
    """
    >>> import numpy as np
    >>> from pandas import Series, Index
    >>> from doctestprinter import (
    ...     _format_values_of_series_to_representation,
    ...     doctest_print,
    ...     PandasFormatSpecification
    ... )
    >>> sample_series = Series(
    ...     np.linspace(1,5000/3,num=3),
    ...     index=Index(np.arange(1, 4)*0.1, name="x"),
    ...     name="y"
    ... )
    >>> sample_result = _format_values_of_series_to_representation(
    ...     sample_series,
    ...     format_spec=PandasFormatSpecification(align=">", precision=".2", repr_type="f"),
    ...     max_title_width=16
    ... )
    >>> print(sample_result)
    x
    0.1       1.00
    0.2     833.83
    0.3    1666.67
    Name: y, dtype: object
    >>> sample_result = _format_values_of_series_to_representation(
    ...     sample_series,
    ...     format_spec=PandasFormatSpecification(align="<", precision=".4", repr_type="f"),
    ...     max_title_width=16
    ... )
    >>> doctest_print(sample_result)
    x
    0.1    1.0000
    0.2    833.8333
    0.3    1666.6667
    Name: y, dtype: object
    """
    pass


def test_pandas_column_prepare_left_align():
    """

    >>> from doctestprinter import (
    ...     doctest_print,
    ...     _DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH,
    ...     _DEFAULT_SHORTEN_ROWS_AT,
    ...     EBlankTitleSpacer
    ... )
    >>> left_aligned_column = test_pandas_column_prepare_left_align()
    >>> prepared_sample = left_aligned_column.prepare_repr(
    ...     max_line_count=_DEFAULT_SHORTEN_ROWS_AT,
    ...     max_title_width=_DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH,
    ...     title_spacer=EBlankTitleSpacer.NO_SPACER
    ... )
    >>> doctest_print(prepared_sample)
    0    y
    0    a
    1    b
    2    c
    dtype: object
    >>> prepared_sample = left_aligned_column.prepare_repr(
    ...     max_line_count=_DEFAULT_SHORTEN_ROWS_AT,
    ...     max_title_width=_DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH,
    ...     title_spacer=EBlankTitleSpacer.ABOVE
    ... )
    >>> doctest_print(prepared_sample)
    0
    1    y
    0    a
    1    b
    2    c
    dtype: object
    >>> prepared_sample = left_aligned_column.prepare_repr(
    ...     max_line_count=_DEFAULT_SHORTEN_ROWS_AT,
    ...     max_title_width=_DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH,
    ...     title_spacer=EBlankTitleSpacer.BELOW
    ... )
    >>> doctest_print(prepared_sample)
    0    y
    1
    0    a
    1    b
    2    c
    dtype: object
    """
    left_aligned = PandasFormatSpecification("<")
    assert left_aligned == "{:<}", "Formatting is not as expected."
    sole_sample_values = Series(list(iter("abc")), name="y")
    return _PandasColumn(
        column=sole_sample_values,
        format_spec=left_aligned,
        title_align="<",
    )


def test_pandas_column_prepare_left_align_longer_title():
    """

    >>> from doctestprinter import (
    ...     doctest_iter_print,
    ...     _DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH,
    ...     _DEFAULT_SHORTEN_ROWS_AT,
    ...     EBlankTitleSpacer,
    ...     set_in_quotes
    ... )
    >>> left_aligned_column = test_pandas_column_prepare_left_align_longer_title()
    >>> prepared_sample = left_aligned_column.prepare_repr(
    ...     max_line_count=_DEFAULT_SHORTEN_ROWS_AT,
    ...     max_title_width=_DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH,
    ...     title_spacer=EBlankTitleSpacer.NO_SPACER
    ... )
    >>> doctest_iter_print(
    ...     prepared_sample.to_list(), edits_item=set_in_quotes
    ... )
    'longer_title'
    'a           '
    'b           '
    'c           '
    >>> prepared_sample = left_aligned_column.prepare_repr(
    ...     max_line_count=_DEFAULT_SHORTEN_ROWS_AT,
    ...     max_title_width=_DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH,
    ...     title_spacer=EBlankTitleSpacer.ABOVE
    ... )
    >>> doctest_iter_print(
    ...     prepared_sample.to_list(), edits_item=set_in_quotes
    ... )
    '            '
    'longer_title'
    'a           '
    'b           '
    'c           '
    >>> prepared_sample = left_aligned_column.prepare_repr(
    ...     max_line_count=_DEFAULT_SHORTEN_ROWS_AT,
    ...     max_title_width=_DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH,
    ...     title_spacer=EBlankTitleSpacer.BELOW
    ... )
    >>> doctest_iter_print(
    ...     prepared_sample.to_list(), edits_item=set_in_quotes
    ... )
    'longer_title'
    '            '
    'a           '
    'b           '
    'c           '
    """
    left_aligned = PandasFormatSpecification("<")
    sole_sample_values = Series(list(iter("abc")), name="longer_title")
    return _PandasColumn(
        column=sole_sample_values,
        format_spec=left_aligned,
        title_align=">",
    )


def test_pandas_column_prepare_right_align_longer_title():
    """

    >>> from doctestprinter import (
    ...     doctest_iter_print,
    ...     _DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH,
    ...     _DEFAULT_SHORTEN_ROWS_AT,
    ...     EBlankTitleSpacer,
    ...     set_in_quotes
    ... )
    >>> right_aligned_column = test_pandas_column_prepare_right_align_longer_title()
    >>> prepared_sample = right_aligned_column.prepare_repr(
    ...     max_line_count=_DEFAULT_SHORTEN_ROWS_AT,
    ...     max_title_width=_DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH,
    ...     title_spacer=EBlankTitleSpacer.NO_SPACER
    ... )
    >>> doctest_iter_print(
    ...     prepared_sample.to_list(), edits_item=set_in_quotes
    ... )
    'longer_title'
    '           1'
    '           2'
    '           3'
    >>> prepared_sample = right_aligned_column.prepare_repr(
    ...     max_line_count=_DEFAULT_SHORTEN_ROWS_AT,
    ...     max_title_width=_DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH,
    ...     title_spacer=EBlankTitleSpacer.ABOVE
    ... )
    >>> doctest_iter_print(
    ...     prepared_sample.to_list(), edits_item=set_in_quotes
    ... )
    '            '
    'longer_title'
    '           1'
    '           2'
    '           3'
    >>> prepared_sample = right_aligned_column.prepare_repr(
    ...     max_line_count=_DEFAULT_SHORTEN_ROWS_AT,
    ...     max_title_width=_DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH,
    ...     title_spacer=EBlankTitleSpacer.BELOW
    ... )
    >>> doctest_iter_print(
    ...     prepared_sample.to_list(), edits_item=set_in_quotes
    ... )
    'longer_title'
    '            '
    '           1'
    '           2'
    '           3'

    """
    right_aligned = PandasFormatSpecification.from_string("{:>.0f}")
    sole_sample_values = Series([1, 2, 3], name="longer_title")
    return _PandasColumn(
        column=sole_sample_values,
        format_spec=right_aligned,
        title_align=">",
    )


def test_adjust_title_and_formatted_series_width():
    """
    >>> from doctestprinter import doctest_print
    >>> sample_title, final_sample = test_adjust_title_and_formatted_series_width()
    >>> sample_title
    'y'
    >>> doctest_print(final_sample.to_list())
    ['1', '2']
    """
    sample_series = Series(
        [1.0, 2.0], index=pandas.Index([0.1, 0.2], name="x"), name="y", dtype=float
    )
    preformat_sample = _format_values_of_series_to_representation(
        series_to_print=sample_series,
        format_spec=PandasFormatSpecification(align=">", precision=".0", repr_type="f"),
        max_title_width=_DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH
    )
    adjusted_title, final_series = _adjust_title_and_formatted_series_width(
        preformatted_series=preformat_sample, cell_align=">", title_align=">"
    )
    return adjusted_title, final_series


def test_adjust_title_formatted_width_longer_title():
    """
    >>> from doctestprinter import doctest_print
    >>> sample_title, final_sample = test_adjust_title_formatted_width_longer_title()
    >>> sample_title
    'longer'
    >>> doctest_print(final_sample.to_list())
    ['     1', '     2']
    """
    sample_series = Series(
        [1.0, 2.0], index=pandas.Index([0.1, 0.2], name="x"), name="longer", dtype=float
    )
    preformat_sample = _format_values_of_series_to_representation(
        series_to_print=sample_series,
        format_spec=PandasFormatSpecification(align=">", precision=".0", repr_type="f"),
        max_title_width=_DEFAULT_MAXIMUM_COLUMN_TITLE_WIDTH
    )
    adjusted_title, final_series = _adjust_title_and_formatted_series_width(
        preformatted_series=preformat_sample, cell_align=">", title_align=">"
    )
    return adjusted_title, final_series


def test_generate_dataframe_representation():
    """
    >>> from doctestprinter import doctest_print
    >>> doctest_print(test_generate_dataframe_representation())
         y1  y2
    x
    0.1   0   1
    0.2   2   3
    """
    sample_frame = DataFrame(
        np.arange(4).reshape(2, 2),
        index=pandas.Index([0.1, 0.2], name="x"),
        columns=["y1", "y2"],
        dtype=float,
    )
    return _generate_dataframe_representation(sample_frame, "{:.1f}#{:.0f}")


def test_format_series():
    """
    .. testsetup::

        >>> import numpy as np
        >>> from pandas import Series, Index
        >>> from doctestprinter import _format_series, doctest_print
        >>> sample_series = Series(
        ...     np.arange(60),
        ...     name="y"
        ... )
        >>> sample_format = PandasFormatSpecification(
        ...     align='>', width='', precision='.1', repr_type='f'
        ... )

    Testing max_line_count < 2
    --------------------------

    .. doctest::

        >>> sample_result = _format_series(
        ...     sample_series, sample_format, max_line_count=1, max_title_width=16
        ... )
        >>> doctest_print(sample_result)
        0      0.0
        0      ...
        59    59.0
        Name: y, dtype: object


    Testing default max_line_count
    ------------------------------

    .. doctest::

        >>> sample_result = _format_series(
        ...     series_to_print=sample_series,
        ...     target_format=sample_format,
        ...     max_line_count=20,
        ...     max_title_width=16
        ... )
        >>> doctest_print(sample_result)
        0      0.0
        1      1.0
        2      2.0
        3      3.0
        4      4.0
        0      ...
        55    55.0
        56    56.0
        57    57.0
        58    58.0
        59    59.0
        Name: y, dtype: object

    """
    pass


def test_print_pandas():
    """

    .. testsetup::

        >>> from pandas import DataFrame, Series
        >>> from doctestprinter import print_pandas
        >>> import numpy as np

    .. doctest::

        >>> print_pandas()
        pandas
        >>> print_pandas(DataFrame([], dtype=str))
        Empty DataFrame
        Columns: []
        Index: []
        >>> print_pandas(Series([], dtype=str))
        Series([], dtype: object)
        >>> print_pandas(DataFrame(np.full(4, np.nan).reshape(2, 2)), formats="{:.0f}")
             0    1
        0  nan  nan
        1  nan  nan
    """


def test_print_pandas_with_multi_index_dataframe():
    """

    .. testsetup::

        >>> from pandas import DataFrame
        >>> from doctestprinter import print_pandas
        >>> import numpy as np

    .. doctest::

        >>> from pandas import MultiIndex
        >>> sample_tuples = list(zip("aaaaaaaa", "bbbbcccc", "ddeeffgg"))
        >>> sample_multi_index = MultiIndex.from_tuples(sample_tuples)
        >>> sample_frame = DataFrame(np.arange(10, 18), index=sample_multi_index)
        >>> print_pandas(sample_frame)
                  0
        a  b  d  10
              d  11
              e  12
              e  13
           c  f  14
              f  15
              g  16
              g  17

    .. doctest::

        >>> from pandas import MultiIndex
        >>> sample_tuples = list(zip("aaaaaaaa", "bbbbcccc", "ddeeffgg"))
        >>> sample_multi_index = MultiIndex.from_tuples(sample_tuples)
        >>> sample_frame = DataFrame(np.arange(10, 18), index=sample_multi_index)
        >>> print_pandas(sample_frame, formats="{:>}#{:.0f}")
                  0
        a  b  d  10
              d  11
              e  12
              e  13
           c  f  14
              f  15
              g  16
              g  17

    """
    pass


def test_print_pandas_with_multi_index_series():
    """

    .. testsetup::

        >>> from pandas import Series
        >>> from doctestprinter import print_pandas
        >>> import numpy as np

    .. doctest::

        >>> from pandas import MultiIndex
        >>> sample_tuples = list(zip("aaaaaaaa", "bbbbcccc", "ddeeffgg"))
        >>> sample_multi_index = MultiIndex.from_tuples(sample_tuples)
        >>> sample_series = Series(np.arange(10,18), index=sample_multi_index)
        >>> print_pandas(sample_series)
        a  b  d  10
              d  11
              e  12
              e  13
           c  f  14
              f  15
              g  16
              g  17

    .. doctest::

        >>> from pandas import MultiIndex
        >>> sample_tuples = list(zip("aaaaaaaa", "bbbbcccc", "ddeeffgg"))
        >>> sample_multi_index = MultiIndex.from_tuples(sample_tuples)
        >>> sample_series = Series(np.arange(10, 18), index=sample_multi_index)
        >>> print_pandas(sample_series, formats="{:>}#{:.0f}")
        a  b  d  10
              d  11
              e  12
              e  13
           c  f  14
              f  15
              g  16
              g  17
    """

def test_pandas_print_with_very_long_title():
    """

    .. testsetup::

        >>> from pandas import Series, DataFrame
        >>> from doctestprinter import print_pandas
        >>> import numpy as np

    .. doctest::

        >>> sample_series = Series(
        ...     [10], name="A_very_long_title,_longer_than_the_default_maximum_length."
        ... )
        >>> print_pandas(sample_series)
           A_very_long_ti..
        0                10

    """
    pass


def test_pathlib_path():
    """
    >>> from doctestprinter import print_pandas
    >>> sample_with_path = test_pathlib_path()
    >>> print_pandas(sample_with_path)
    0  a/path
    """
    return Series(Path("a/path"))