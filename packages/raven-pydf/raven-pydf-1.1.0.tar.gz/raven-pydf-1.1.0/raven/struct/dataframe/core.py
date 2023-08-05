# Copyright (C) 2021 Raven Computing
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Provides a DataFrame API and implementations."""

import re as regex_matcher
import inspect

from abc import ABC, ABCMeta

import numpy as np

import raven.struct.dataframe.column
import raven.struct.dataframe.bytecolumn as bytecolumn
import raven.struct.dataframe.shortcolumn as shortcolumn
import raven.struct.dataframe.intcolumn as intcolumn
import raven.struct.dataframe.longcolumn as longcolumn
import raven.struct.dataframe.floatcolumn as floatcolumn
import raven.struct.dataframe.doublecolumn as doublecolumn
import raven.struct.dataframe.stringcolumn as stringcolumn
import raven.struct.dataframe.charcolumn as charcolumn
import raven.struct.dataframe.booleancolumn as booleancolumn
import raven.struct.dataframe.binarycolumn as binarycolumn
import raven.struct.dataframe._dataframeutils as dataframeutils
import raven.io.dataframe.dataframes
import raven.io.dataframe.csvfiles

__author__ = "Phil Gaiser"

class DataFrame(ABC):
    """An object that binds strongly typed columns into one data structure.

    All Columns have equal length but each Column can be of a different type.
    A Column can have a name associated with it so it can be accessed through that
    name without knowledge of the index the Column is located at. Methods provided
    by this interface allow Columns to be referenced both by index and name. Access
    to any column-row value is guaranteed to be fulfilled in constant time.

    All DataFrame implementations work with raven.struct.dataframe.column.Column types,
    which represent any column of a particular DataFrame. In order to ensure
    type safety, all concrete column types work with elements of one, and only one,
    concrete type. It is not possible to mix elements of different types within
    one Column instance.

    Ten different element types are supported by any DataFrame implementation:

    byte (int8), short (int16), int (int32), long (int64), float (float32),
    double (float64), string (str), char (single ASCII-character), boolean (bool)
    and binary (bytearray).

    A DataFrame manages Column instances and the underlying data arrays. When adding
    or removing rows, a buffer in every Column of a DataFrame may be present, i.e.
    the low-level array inside a Column of a DataFrame may be longer than the number
    of rows in the underlying DataFrame at that time. It is the responsibility of
    each DataFrame implementation to correctly manage any unused space. A DataFrame
    provides methods to determine the used number of Columns and rows as well as the
    actual memory capacity used by all Columns. A DataFrame can be flushed at any time
    which releases any unused memory from the Columns it manages. Since Columns do not
    manage their capacity independently, care must be taken when working with Column
    instances directly. Users are generally advised to only manipulate Columns through
    methods provided by the DataFrame class. Moreover, because a DataFrame is a
    collection of references to Columns, it is possible for a user to generate an
    inconsistent state in DataFrames. For example, two DataFrames can have a reference
    to the same Column instance to safe memory. However, if one DataFrame then removes
    rows from the underlying Column, then the other DataFrame will not be aware of
    that change. It is the responsibility of the user to explicitly copy (clone) Columns
    whenever needed to avoid conflicts.

    Two concrete Column implementations are provided for all core types. On the one hand,
    a default implementation is provided which does not allow the use of null values.
    Therefore, when using default Columns, all entries are always guaranteed to be set
    to a valid value of the corresponding type. On the other hand, a second Column
    implementation is provided, allowing the use of null values.

    The term 'null' or 'null value' is equivalent to the term 'None' and 'NoneType'
    respectively and may be used interchangeably.

    Default Column implementations are generally speaking more efficient than nullable
    implementations both in terms of runtime and memory footprint.

    Just as there are two different Column implementations for all supported element
    types, there are also two separate implementations of a DataFrame:

    DefaultDataFrame and NullableDataFrame.

    Both DataFrame implementations can only work with the corresponding appropriate
    Column type. That is, a DefaultDataFrame must use default (non-nullable) Column
    instances whereas a NullableDataFrame must use nullable Column instances.

    The DataFrame API defines various methods for numerical computations. These
    computations should whenever possible be directly executed with the corresponding
    element type of the underlying Column. Methods may dynamically return a value of
    the corresponding element type representing the final return value computed.
    Individual methods should document how numeric values returned by them are handled.

    Any method provided by a DataFrame can throw
    a raven.struct.dataframe.DataFrameException at runtime if any argument passed to
    it is invalid, for example an out of bounds index, or if that operation would
    result in an incoherent/invalid state of that DataFrame. Docstrings of specific
    methods do not have to mention this explicitly. A DataFrameException extends
    the built-in Exception class.

    The DataFrame API also provides various static utility methods to work
    with DataFrames. This includes a standard API for serialization and file I/O support
    for DataFrames.

    In addition to the official specification, DataFrames implemented by this module
    also support various syntactical conveniences through the []-operator, which allows
    easy read and write access to columns, rows and individual values, as well as slicing.
    These additions are all optional and the API declared by the specification is not
    reduced in any way. Using the []-operator can simplify code as it usually looks less
    verbose than the equivalent standard method calls.

    DataFrame instances should not be constructed directly. Various static methods
    are provided for DataFrame and Column construction.

    For example:

      >>> from raven.struct.dataframe import DataFrame
      >>> df = DataFrame.Default(
      >>>         DataFrame.IntColumn("col1", [1, 2, 3]),
      >>>         DataFrame.StringColumn("col2", ["AAA", "BBB", "CCC"]),
      >>>         DataFrame.BooleanColumn("col3", [True, False, True]))

    The above code constructs a DefaultDataFrame with the specified Columns.

    A NullableDataFrame can be constructed in the same way, for example:

      >>> df = DataFrame.Nullable(
      >>>         DataFrame.NullableIntColumn("col1", [1, None, 3]),
      >>>         DataFrame.NullableStringColumn("col2", ["AAA", None, "CCC"]),
      >>>         DataFrame.NullableBooleanColumn("col3", [True, None, False]))

    All Columns can also be constructed directly by importing the
    corresponding classes.

    For example:
      >>> from raven.struct.dataframe import (DefaultDataFrame,
      >>>                                     IntColumn,
      >>>                                     StringColumn,
      >>>                                     BooleanColumn)
      >>> df = DefaultDataFrame(
      >>>         IntColumn("col1", [1, 2, 3]),
      >>>         StringColumn("col2", ["AAA", "BBB", "CCC"]),
      >>>         BooleanColumn("col3", [True, False, True]))
    """

    __metaclass__ = ABCMeta

    # pylint: disable=C0103, C0121, C0302, W0212, R0911
    # pylint: disable=R0912, R0914, R0915, R1705, R1720
    def __init__(self, is_nullable=None, columns=None):
        """Constructs a new DataFrame.

        WARNING:

        This constructor should not be used by API users.
        Please construct a DataFrame by calling the appropriate static function or
        directly construct either a DefaultDataFrame or NullableDataFrame object.

        For example:

          >>> from raven.struct.dataframe import DataFrame
          >>> df = DataFrame.Default(
          >>>         DataFrame.IntColumn("col1", [1, 2, 3]),
          >>>         DataFrame.StringColumn("col2", ["AAA", "BBB", "CCC"]),
          >>>         DataFrame.BooleanColumn("col3", [True, False, True]))

        The above code constructs a DefaultDataFrame with the specified Columns.

        A NullableDataFrame can be constructed in the same way, for example:

          >>> df = DataFrame.Nullable(
          >>>         DataFrame.NullableIntColumn("col1", [1, None, 3]),
          >>>         DataFrame.NullableStringColumn("col2", ["AAA", None, "CCC"]),
          >>>         DataFrame.NullableBooleanColumn("col3", [True, None, False]))
        """
        if is_nullable is None:
            raise DataFrameException(
                ("Invalid argument. Must specify DataFrame type. "
                 "WARNING: This constructor is not public API"))

        if not isinstance(is_nullable, bool):
            raise DataFrameException(
                ("Invalid argument 'is_nullable'. Must be "
                 "a bool. WARNING: This constructor is not public API"))

        self.__is_nullable = is_nullable
        if columns is None or len(columns) == 0:
            self.__next = -1
            self.__names = None
            self.__columns = None
            return

        col_size = columns[0].capacity()
        for i in range(1, len(columns)):
            if columns[i].capacity() != col_size:
                raise DataFrameException("Columns have deviating sizes")

        self.__names = None
        for i, col in enumerate(columns):
            if self.__is_nullable:
                if not col.is_nullable():
                    columns[i] = col.as_nullable()

            else:
                if col.is_nullable():
                    raise DataFrameException(
                        "DefaultDataFrame cannot use NullableColumn instance")

            if col._name:
                if self.__names is None:
                    self.__names = dict()

                self.__names[col._name] = i

        self.__next = col_size
        self.__columns = columns

    def get_byte(self, col, row):
        """Gets the byte from the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values, then the
        returned byte is guaranteed to be not None.

        Args:
            col: The name or index of the column to get the value from.
                Must be an int or str
            row: The row index of the value to get

        Returns:
            The byte value at the specified position as an int object
        """
        if self.__is_nullable:
            return self._get_typed_value(col, row, bytecolumn.NullableByteColumn.TYPE_CODE)
        else:
            return self._get_typed_value(col, row, bytecolumn.ByteColumn.TYPE_CODE)

    def get_short(self, col, row):
        """Gets the short from the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values, then the
        returned short is guaranteed to be not None.

        Args:
            col: The name or index of the column to get the value from.
                Must be an int or str
            row: The row index of the value to get

        Returns:
            The short value at the specified position as an int object
        """
        if self.__is_nullable:
            return self._get_typed_value(col, row, shortcolumn.NullableShortColumn.TYPE_CODE)
        else:
            return self._get_typed_value(col, row, shortcolumn.ShortColumn.TYPE_CODE)

    def get_int(self, col, row):
        """Gets the int from the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values, then the
        returned int is guaranteed to be not None.

        Args:
            col: The name or index of the column to get the value from.
                Must be an int or str
            row: The row index of the value to get

        Returns:
            The int value at the specified position as an int object
        """
        if self.__is_nullable:
            return self._get_typed_value(col, row, intcolumn.NullableIntColumn.TYPE_CODE)
        else:
            return self._get_typed_value(col, row, intcolumn.IntColumn.TYPE_CODE)

    def get_long(self, col, row):
        """Gets the long from the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values, then the
        returned long is guaranteed to be not None.

        Args:
            col: The name or index of the column to get the value from.
                Must be an int or str
            row: The row index of the value to get

        Returns:
            The long value at the specified position as an int object
        """
        if self.__is_nullable:
            return self._get_typed_value(col, row, longcolumn.NullableLongColumn.TYPE_CODE)
        else:
            return self._get_typed_value(col, row, longcolumn.LongColumn.TYPE_CODE)

    def get_string(self, col, row):
        """Gets the string from the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values, then the
        returned string is guaranteed to be not None.

        Args:
            col: The name or index of the column to get the value from.
                Must be an int or str
            row: The row index of the value to get

        Returns:
            The string value at the specified position
        """
        if self.__is_nullable:
            return self._get_typed_value(col, row, stringcolumn.NullableStringColumn.TYPE_CODE)
        else:
            return self._get_typed_value(col, row, stringcolumn.StringColumn.TYPE_CODE)

    def get_float(self, col, row):
        """Gets the float from the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values, then the
        returned float is guaranteed to be not None.

        Args:
            col: The name or index of the column to get the value from.
                Must be an int or str
            row: The row index of the value to get

        Returns:
            The float value at the specified position as a float object
        """
        if self.__is_nullable:
            return self._get_typed_value(col, row, floatcolumn.NullableFloatColumn.TYPE_CODE)
        else:
            return self._get_typed_value(col, row, floatcolumn.FloatColumn.TYPE_CODE)

    def get_double(self, col, row):
        """Gets the double from the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values, then the
        returned double is guaranteed to be not None.

        Args:
            col: The name or index of the column to get the value from.
                Must be an int or str
            row: The row index of the value to get

        Returns:
            The double value at the specified position as a float object
        """
        if self.__is_nullable:
            return self._get_typed_value(col, row, doublecolumn.NullableDoubleColumn.TYPE_CODE)
        else:
            return self._get_typed_value(col, row, doublecolumn.DoubleColumn.TYPE_CODE)

    def get_char(self, col, row):
        """Gets the char from the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values, then the
        returned char is guaranteed to be not None.

        Args:
            col: The name or index of the column to get the value from.
                Must be an int or str
            row: The row index of the value to get

        Returns:
            The char value at the specified position as a str
            object of length 1
        """
        if self.__is_nullable:
            return self._get_typed_value(col, row, charcolumn.NullableCharColumn.TYPE_CODE)
        else:
            return self._get_typed_value(col, row, charcolumn.CharColumn.TYPE_CODE)

    def get_boolean(self, col, row):
        """Gets the boolean from the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values, then the
        returned boolean is guaranteed to be not None.

        Args:
            col: The name or index of the column to get the value from.
                Must be an int or str
            row: The row index of the value to get

        Returns:
            The boolean value at the specified position as a bool object
        """
        if self.__is_nullable:
            return self._get_typed_value(col, row, booleancolumn.NullableBooleanColumn.TYPE_CODE)
        else:
            return self._get_typed_value(col, row, booleancolumn.BooleanColumn.TYPE_CODE)

    def get_binary(self, col, row):
        """Gets the binary data from the specified column at
        the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values, then the
        returned bytearray is guaranteed to be not None.

        Args:
            col: The name or index of the column to get the value from.
                Must be an int or str
            row: The row index of the value to get

        Returns:
            The binary data at the specified position as a bytearray object
        """
        if self.__is_nullable:
            return self._get_typed_value(col, row, binarycolumn.NullableBinaryColumn.TYPE_CODE)
        else:
            return self._get_typed_value(col, row, binarycolumn.BinaryColumn.TYPE_CODE)

    def set_byte(self, col, row, value):
        """Sets the byte at the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values,
        then the provided byte must not be None

        Args:
            col: The name or index of the column to set the value at
                Must be an int or str
            row: The row index of the value to set
            value: The byte value to set. Must be a Python int
                or numpy dtype.int8
        """
        if self.__is_nullable:
            self._set_typed_value(col, row, value, bytecolumn.NullableByteColumn.TYPE_CODE)
        else:
            self._set_typed_value(col, row, value, bytecolumn.ByteColumn.TYPE_CODE)

    def set_short(self, col, row, value):
        """Sets the short at the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values,
        then the provided short must not be None

        Args:
            col: The name or index of the column to set the value at
                Must be an int or str
            row: The row index of the value to set
            value: The short value to set. Must be a Python int
                or numpy dtype.int16
        """
        if self.__is_nullable:
            self._set_typed_value(col, row, value, shortcolumn.NullableShortColumn.TYPE_CODE)
        else:
            self._set_typed_value(col, row, value, shortcolumn.ShortColumn.TYPE_CODE)

    def set_int(self, col, row, value):
        """Sets the int at the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values,
        then the provided int must not be None

        Args:
            col: The name or index of the column to set the value at
                Must be an int or str
            row: The row index of the value to set
            value: The int value to set. Must be a Python int
                or numpy dtype.int32
        """
        if self.__is_nullable:
            self._set_typed_value(col, row, value, intcolumn.NullableIntColumn.TYPE_CODE)
        else:
            self._set_typed_value(col, row, value, intcolumn.IntColumn.TYPE_CODE)

    def set_long(self, col, row, value):
        """Sets the long at the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values,
        then the provided long must not be None

        Args:
            col: The name or index of the column to set the value at
                Must be an int or str
            row: The row index of the value to set
            value: The long value to set. Must be a Python int
                or numpy dtype.int64
        """
        if self.__is_nullable:
            self._set_typed_value(col, row, value, longcolumn.NullableLongColumn.TYPE_CODE)
        else:
            self._set_typed_value(col, row, value, longcolumn.LongColumn.TYPE_CODE)

    def set_string(self, col, row, value):
        """Sets the string at the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values,
        then the provided string will be converted to 'n/a' if
        it is None or empty

        Args:
            col: The name or index of the column to set the value at
                Must be an int or str
            row: The row index of the value to set
            value: The string value to set. Must be a str
        """
        if self.__is_nullable:
            self._set_typed_value(col, row, value, stringcolumn.NullableStringColumn.TYPE_CODE)
        else:
            self._set_typed_value(col, row, value, stringcolumn.StringColumn.TYPE_CODE)

    def set_float(self, col, row, value):
        """Sets the float at the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values,
        then the provided float must not be None

        Args:
            col: The name or index of the column to set the value at
                Must be an int or str
            row: The row index of the value to set
            value: The float value to set. Must be a Python float
                or numpy dtype.float32
        """
        if self.__is_nullable:
            self._set_typed_value(col, row, value, floatcolumn.NullableFloatColumn.TYPE_CODE)
        else:
            self._set_typed_value(col, row, value, floatcolumn.FloatColumn.TYPE_CODE)

    def set_double(self, col, row, value):
        """Sets the double at the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values,
        then the provided double must not be None

        Args:
            col: The name or index of the column to set the value at
                Must be an int or str
            row: The row index of the value to set
            value: The double value to set. Must be a Python float
                or numpy dtype.float64
        """
        if self.__is_nullable:
            self._set_typed_value(col, row, value, doublecolumn.NullableDoubleColumn.TYPE_CODE)
        else:
            self._set_typed_value(col, row, value, doublecolumn.DoubleColumn.TYPE_CODE)

    def set_char(self, col, row, value):
        """Sets the char at the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values,
        then the provided char must not be None

        Args:
            col: The name or index of the column to set the value at
                Must be an int or str
            row: The row index of the value to set
            value: The char value to set. Must be a str.
                Only printable ASCII characters are permitted
        """
        if self.__is_nullable:
            self._set_typed_value(col, row, value, charcolumn.NullableCharColumn.TYPE_CODE)
        else:
            self._set_typed_value(col, row, value, charcolumn.CharColumn.TYPE_CODE)

    def set_boolean(self, col, row, value):
        """Sets the boolean at the specified column at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values,
        then the provided boolean must not be None

        Args:
            col: The name or index of the column to set the value at
                Must be an int or str
            row: The row index of the value to set
            value: The boolean value to set. Must be a Python bool
                or numpy dtype.bool
        """
        if self.__is_nullable:
            self._set_typed_value(col, row, value, booleancolumn.NullableBooleanColumn.TYPE_CODE)
        else:
            self._set_typed_value(col, row, value, booleancolumn.BooleanColumn.TYPE_CODE)

    def set_binary(self, col, row, value):
        """Sets the binary data at the specified column
        at the specified row index.

        The column can be specified either by index or by name. If the
        underlying DataFrame implementation doesn't support null values,
        then the provided bytearray must not be None

        Args:
            col: The name or index of the column to set the value at
                Must be an int or str
            row: The row index of the value to set
            value: The binary data to set. Must be a bytearray
        """
        if self.__is_nullable:
            self._set_typed_value(col, row, value, binarycolumn.NullableBinaryColumn.TYPE_CODE)
        else:
            self._set_typed_value(col, row, value, binarycolumn.BinaryColumn.TYPE_CODE)

    def get_column_names(self):
        """Gets the name of all columns of this DataFrame in proper order.

        Columns which have not been named will be represented as their index
        within the DataFrame.

        Returns:
            The names of all columns as a list of str, or None if no column
            names have been set
        """
        if self.__names is not None:
            names = [None] * len(self.__columns)
            for i in range(len(self.__columns)):
                s = self.__columns[i]._name
                if s:
                    names[i] = s
                else:
                    names[i] = str(i)

            return names

        return None

    def get_column_name(self, index):
        """Gets the name of the column at the specified index.

        Args:
            col: The index of the column, as an int

        Returns:
            The name of the column as a str, or None if no name has
            been set for this column
        """
        if not isinstance(index, int):
            raise DataFrameException(
                ("Invalid argument 'index': Expected "
                 "int but found {}").format(type(index)))

        if (self.__next == -1) or (index < 0) or (index >= len(self.__columns)):
            raise DataFrameException("Invalid column index: {}".format(index))

        if self.__names is not None:
            return self.__columns[index]._name

        return None

    def get_column_index(self, col):
        """Gets the index of the column with the specified name.

        This method may throw a DataFrameException if no column of this
        DataFrame has the specified name or if no names have been set

        Args:
            col: The name of the column to get the index for. Must be a str

        Returns:
            The index of the column with the specified name
        """
        return self._enforce_name(col)

    def set_column_names(self, *names):
        """Assigns all columns the specified names. Any already set name will
        get overridden. The length of the provided list must match the number
        of columns in this DataFrame.

        Please note that no checks will be performed regarding duplicates.
        Assigning more than one column the same name will result in undefined
        behaviour

        Args:
            names: The names of the columns, as a list of strings.
                Must not be None. Must not contain None or empty strings

        Returns:
            This DataFrame instance
        """
        if names is None or len(names) == 0:
            raise DataFrameException("Arg must not be None or empty")

        # unpack if names were not given as varags
        if isinstance(names[0], (list, tuple)):
            names = names[0]

        if self.__next == -1 or len(names) != len(self.__columns):
            raise DataFrameException(
                ("Length of column names list does not match number of "
                 "columns: {} (the DataFrame has {} columns)").format(len(names), self.columns()))

        self.__names = dict()
        for i, name in enumerate(names):
            if name is not None and not isinstance(name, str):
                raise DataFrameException(
                    ("Invalid type for column name. "
                     "Expected str but found {}").format(type(name)))

            if not name:
                raise DataFrameException("Column name must not be None or empty")

            self.__names[name] = i
            self.__columns[i]._name = name

        return self

    def set_column_name(self, col, name):
        """Assigns the specified Column the given new name.

        The Column to rename can be specified either by index or by name.
        The return value of this method depends on the type of
        the 'col' argument.

        No checks will be performed regarding duplicates. Assigning more
        than one Column the same name will result in undefined behaviour.

        Args:
            col: The index or name of the Column to rename. Must be an int or str.
            name: The new name to assign to the column, as a str.
                  Must not be None or empty

        Returns:
            This DataFrame instance if the 'col' argument was specified as a str.
            Returns a bool if the 'col' argument was specified as an int. The bool
            indicates whether any previous name of the specified Column was
            overridden as a result of this operation.
        """
        if not isinstance(col, (int, str)):
            raise DataFrameException(
                ("Invalid argument 'col'. "
                 "Expected int or str but found {}").format(type(col)))

        arg_is_string = False
        if isinstance(col, str):
            col = self._enforce_name(col)
            arg_is_string = True

        if not isinstance(name, str):
            raise DataFrameException(
                ("Invalid argument 'name'. "
                 "Expected str but found {}").format(type(name)))

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        if not name:
            raise DataFrameException("Column name must not be None or empty")

        if self.__names is None:
            self.__names = dict()

        overridden = False
        current = self.__columns[col]._name
        index = None
        if current:
            index = self.__names[current]

        if index is not None and index == col:
            del self.__names[current]
            overridden = True

        self.__names[name] = col
        self.__columns[col]._name = name
        return self if arg_is_string else overridden

    def remove_column_names(self):
        """Removes all column names from this DataFrame instance.

        Returns:
            This DataFrame instance
        """
        self.__names = None
        for i in range(len(self.__columns)):
            self.__columns[i]._name = None

        return self

    def has_column(self, col):
        """Indicates whether this DataFrame has a Column with
        the specified name.

        Args:
            col: The name of the Column. Must be a str

        Returns:
            True if this DataFrame has a Column with the specified name,
            False if no Column with the specified name exists in this DataFrame
        """
        if not isinstance(col, str):
            raise DataFrameException(
                ("Invalid argument 'col'. Expected str but found {}").format(type(col)))

        if not col:
            raise DataFrameException("Column name must not be None or empty")

        if self.__names is None:
            return False

        try:
            return self.__names[col] is not None
        except KeyError:
            return False

    def has_column_names(self):
        """Indicates whether this DataFrame has any column names set.

        Please note that this method returns True even when Column names are only
        partially set, i.e. not all Columns must have a name
        assigned to them. In other words, this method returns True if at
        least one Column has a name assigned to it.

        Returns:
            True if this DataFrame has any Column names set,
            False if no Column names have been set
        """
        return self.__names is not None

    def get_row(self, index):
        """Gets the row at the specified index.

        If the underlying DataFrame implementation doesn't support null values,
        then the returned list is guaranteed to consist of non-None values.
        The length of the returned list is equal to the number of Columns
        of this DataFrame

        Args:
            index: The index of the row to get, as an int

        Returns:
            The row at the specified index, as a list
        """
        if not isinstance(index, int):
            raise DataFrameException(
                ("Invalid argument 'index'. Expected int "
                 "but found {}").format(type(index)))

        if index >= self.__next or index < 0:
            raise DataFrameException("Invalid row index: {}".format(index))

        row = []
        for col in self.__columns:
            row.append(col.get_value(index))

        return row

    def get_rows(self, from_index=None, to_index=None):
        """Gets the rows located in the specified range.

        If the underlying DataFrame implementation doesn't support null values,
        then the returned DataFrame is guaranteed to consist of non-None values.
        The returned DataFrame is of the same type as the DateFrame this method
        is called upon.

        All rows in the returned DataFrame are copies of the original rows, so
        changing values within the returned DataFrame has no effect on the original
        DataFrame and vice versa. Please note that this does not apply to bytearray
        objects of BinaryColumns, in which case the references to the underlying
        bytearray objects are copied to the rows of the returned DataFrame.

        Args:
            from_index: The index from which to get all rows from (inclusive), as an int
            to_index: The index to which to get all rows from (exclusive), as an int

        Returns:
            A DataFrame with the same Column structure and all rows from
            the specified start index to the specified end index
        """
        if from_index is None:
            from_index = 0

        if to_index is None:
            to_index = self.__next

        if not isinstance(from_index, int):
            raise DataFrameException(
                ("Invalid argument 'from_index'. "
                 "Expected int but found {}").format(type(from_index)))

        if not isinstance(to_index, int):
            raise DataFrameException(
                ("Invalid argument 'to_index'. "
                 "Expected int but found {}").format(type(to_index)))

        if from_index >= to_index:
            raise DataFrameException(
                ("End index argument 'to_index' must be "
                 "greater than start index 'from_index'"))

        if (from_index < 0 or to_index < 0 or from_index >= self.__next
                or to_index > self.__next):

            raise DataFrameException(
                ("Invalid row index: {}")
                .format(from_index
                        if from_index < 0 or from_index >= self.__next
                        else to_index))

        df = NullableDataFrame() if self.__is_nullable else DefaultDataFrame()
        length = to_index - from_index
        for _, col in enumerate(self.__columns):
            c = raven.struct.dataframe.column.Column.of_type(col.type_code(), length)
            for i in range(from_index, to_index, 1):
                c.set_value(i - from_index, col.get_value(i))

            df.add_column(c)

        if self.__names is not None:
            df.set_column_names(self.get_column_names())

        return df

    def set_row(self, index, row):
        """Sets and replaces the provided row within this DataFrame
        at the specified index.

        The type of each element must be equal to the element type of the Column
        it is placed in. If the underlying DataFrame implementation doesn't
        support null values, then passing a list with None values will result
        in a DataFrameException. The number of provided row items must be equal to
        the number of Columns in this DataFrame

        Args:
            index: The index of the row, as an int
            row: The row items to set. Must be a list

        Returns:
            This DataFrame instance
        """
        if not isinstance(index, int):
            raise DataFrameException(
                ("Invalid argument 'index'. "
                 "Expected int but found {}").format(type(index)))

        if index >= self.__next or index < 0:
            raise DataFrameException("Invalid row index: {}".format(index))

        self._enforce_types(row)
        for i in range(len(self.__columns)):
            self.__columns[i].set_value(index, row[i])

        return self

    def add_row(self, row):
        """Adds the provided row to the end of this DataFrame.

        The type of each element must be equal to the element type of the
        Column it is placed in. If the underlying DataFrame implementation
        doesn't support null values, then passing a list with None values
        will result in a DataFrameException. The number of provided
        row items must be equal to the number of Columns in this DataFrame

        Args:
            row: The items of the row to add. Must be a list

        Returns:
            This DataFrame instance
        """
        self._enforce_types(row)
        if self.__next >= self.__columns[0].capacity():
            self._resize()

        for i in range(len(self.__columns)):
            self.__columns[i].set_value(self.__next, row[i])

        self.__next += 1
        return self

    def add_rows(self, rows):
        """Adds all rows from the specified DataFrame to this DataFrame.

        If the specified DataFrame has labeled Columns, then row items are matched
        according to the respective Column name. If the specified DataFrame has
        unlabeled Columns, then row items are matched according to the respective
        index of the Column they originate from. The type of all row items must be
        equal to the element type of the corresponding Column. If the underlying
        DataFrame implementation doesn't support null values, then all rows must
        consist of non-None values.

        Excessive Columns within the specified DataFrame instance are ignored
        when adding rows, i.e. the Column structure of this DataFrame is never
        changed by this operation. Missing items in rows to be added are substituted
        with either None values or default values of the corresponding Column
        element type if the underlying DataFrame implementation doesn't
        support null values.

        Args:
            rows: The DataFrame instance holding all rows to add.
                Must be a DataFrame
        Returns:
            This DataFrame instance
        """
        if rows is None:
            raise DataFrameException(
                "Invalid argument 'rows'. Argument must not be None")

        if rows.is_empty():
            return self

        # cache
        nrows = rows.rows()
        ncols = len(self.__columns)
        if rows.has_column_names(): # match columns by name
            for i in range(nrows):
                row = [None] * ncols
                for j in range(ncols):
                    name = self.__columns[j].get_name()
                    if name:
                        if rows.has_column(name):
                            row[j] = rows.get_column(name).get_value(i)
                        else:
                            row[j] = self.__columns[j].get_default_value()

                    else:
                        row[j] = (rows.get_column(j).get_value(i)
                                  if j < rows.columns()
                                  else self.__columns[j].get_default_value())

                self.add_row(row)

        else: # match columns by index
            for i in range(nrows):
                row = [None] * ncols
                added_items = 0
                for j in range(rows.columns()):
                    row[j] = rows.get_column(j).get_value(i)
                    added_items += 1

                if added_items < ncols:
                    # add missing row items as default values
                    for j in range(added_items, ncols, 1):
                        row[j] = self.__columns[j].get_default_value()

                self.add_row(row)

        return self

    def insert_row(self, index, row):
        """Inserts the provided row into this DataFrame at the specified index.

        Shifts the row currently at that position and any subsequent rows
        down (adds one to their indices).

        The type of each element must be equal to the element type of the Column
        it is placed in. If the underlying DataFrame implementation doesn't support
        null values, then passing a list with None values will result in a
        DataFrameException. The number of provided row items must be equal to
        the number of Columns in this DataFrame.

        Args:
            index: The index at which the specified row is to be inserted, as an int
            row: The row items to be inserted. Must be a list

        Returns:
            This DataFrame instance
        """
        if not isinstance(index, int):
            raise DataFrameException(
                ("Invalid argument 'index'. "
                 "Expected int but found {}").format(type(index)))

        if index > self.__next or index < 0:
            raise DataFrameException("Invalid row index: {}".format(index))

        if index == self.__next:
            return self.add_row(row)

        self._enforce_types(row)
        if self.__next >= self.__columns[0].capacity():
            self._resize()

        for i, col in enumerate(self.__columns):
            col._insert_value_at(index, self.__next, row[i])

        self.__next += 1
        return self

    def remove_row(self, index):
        """Removes the row at the specified index.

        Args:
            index: The index of the row to be removed, as an int

        Returns:
            This DataFrame instance
        """
        if not isinstance(index, int):
            raise DataFrameException(
                ("Invalid argument 'index'. "
                 "Expected int but found {}").format(type(index)))

        if index >= self.__next or index < 0:
            raise DataFrameException("Invalid row index: {}".format(index))

        for col in self.__columns:
            col._remove(index, index+1, self.__next)

        self.__next -= 1
        if self.__next*3 < self.__columns[0].capacity():
            self._flush_all(4)

        return self

    def remove_rows(self, col=None, regex=None, from_index=None, to_index=None):
        """Removes all rows that match the specified condition.

        This method can be used in two ways. The first way specifies a
        regular expression that all rows to be removed must match in
        a specified Column. In this case, both the 'col' and the 'regex'
        arguments must be specified but NOT the 'from_index' or 'to_index'
        arguments.

        The second way that rows can be removed is by specifying the row
        indices directly. The indices are specified by a range with a start
        and end index. In this case, both the 'from_index' and the 'to_index'
        arguments must be specified but NOT the 'col' or 'regex' arguments.

        The first way removes all rows that match the specified regular
        expression in specified Column. This method then returns an int
        which indicates the number of removed rows, i.e. the number of rows
        that matched the specified regular expression in the specified Column.
        The second way removes all rows which are located in the specified
        interval. This method then returns the reference to this
        DataFrame instance. Optionally, if the second way is used, only one
        of the interval boundaries must necessarily be specified and the
        missing boundary will then be assumed to be the lower or upper
        boundary respectively.

        Args:
            col: The index or name of the Column that the specified regex
                 is matched against. Must be an int or str
            regex: The regular expression that row entries in
                the specified Column must match, as a str
            from_index: The index from which all rows should be removed (inclusive).
                Must be an int
            to_index: The index to which all rows should be removed (exclusive).
                Must be an int

        Returns:
            The number of removed rows if the 'col' and 'regex' arguments
            were specified, as an int. Returns this DataFrame instance if the
            'from_index' and/or 'to_index' arguments were specified
        """
        use_match_op = False
        if col is not None:
            if regex is None:
                raise DataFrameException(
                    ("Invalid arguments. Argument 'col' was "
                     "specified but 'regex' is missing"))

            if from_index is not None:
                raise DataFrameException(
                    ("Invalid arguments. Arguments 'col' and 'regex' were "
                     "specified but 'from_index' is not None"))

            if to_index is not None:
                raise DataFrameException(
                    ("Invalid arguments. Arguments 'col' and 'regex' were "
                     "specified but 'to_index' is not None"))

            if isinstance(col, str):
                col = self._enforce_name(col)

            use_match_op = True

        if not use_match_op and regex is not None:
            raise DataFrameException(
                ("Invalid arguments. Argument 'regex' was "
                 "specified but 'col' is missing"))

        if from_index is not None and to_index is None:
            to_index = self.__next

        if to_index is not None and from_index is None:
            from_index = 0

        if not use_match_op and from_index is None and to_index is None:
            raise DataFrameException("Unable to remove rows. No arguments specified")

        if not use_match_op:
            if from_index >= to_index:
                raise DataFrameException("'to_index' must be greater than 'from_index'")

            if (from_index < 0 or to_index < 0 or from_index >= self.__next
                    or to_index > self.__next):

                if from_index < 0 or from_index >= self.__next:
                    raise DataFrameException(
                        ("Invalid row index 'from_index': {}").format(from_index))

                else:
                    raise DataFrameException(
                        ("Invalid row index 'to_index': {}").format(to_index))

        # call corresponding implementation method
        if use_match_op:
            return self._remove_rows_by_match(col, regex)
        else:
            return self._remove_rows_by_range(from_index, to_index)

    def add_column(self, col=None, name=None):
        """Adds the provided Column to this DataFrame.

        If the specified Column is empty then a new Column instance with the same
        name and type as the specified Column is created and its length is set to
        match the number of rows within this DataFrame. If this DataFrame
        implementation supports null values, then all missing Column entries are
        initialized with null values. If this DataFrame implementation does not support
        null values, then all missing Column entries are initialized with the default
        value of the corresponding Column.

        If the underlying DataFrame implementation supports null values and has a
        deviating size or the provided Column has a deviating size, then the DataFrame
        will refill all missing entries with None values to match the largest Column.
        If the underlying DataFrame implementation does not support null values,
        then the size of the provided Column must match the size of the already
        existing Columns.

        If the added Column was labeled during its construction, then it will
        be referenceable by its name. If the name argument is specified, then
        any already set label in the specified Column will get overridden by
        the specified name.

        Args:
            col: The Column to add to the DataFrame. Must not be None
            name: The name of the Column to add. Must be a str

        Returns:
            This DataFrame instance
        """
        if col is None:
            raise DataFrameException("Invalid argument. Argument 'col' must not be None")

        if self.__is_nullable:
            if not col.is_nullable():
                raise DataFrameException(
                    "NullableDataFrame must use NullableColumn instance")
        else:
            if col.is_nullable():
                raise DataFrameException(
                    "DefaultDataFrame cannot use NullableColumn instance")

        if name is not None and not isinstance(name, str):
            raise DataFrameException(
                ("Invalid argument 'name'. Expected "
                 "str but found {}").format(type(name)))

        if col.capacity() == 0 and self.__next > 0:
            col = raven.struct.dataframe.column.Column.like(col, self.__next)

        if self.__next == -1:
            self.__columns = [None]
            self.__columns[0] = col
            self.__next = col.capacity()
            if name:
                col._name = name

            if col._name:
                self.__names = dict()
                self.__names[col._name] = 0

        else:
            # check column length
            if self.__is_nullable:
                if col.capacity() > self.__next:
                    # match column length in this DataFrame
                    diff = col.capacity() - self.__next
                    csize = len(self.__columns)
                    for i in range(diff):
                        self.add_row([None] * csize)
            else:
                if col.capacity() != self.__next:
                    raise DataFrameException(
                        ("Invalid column length. Must be "
                         "of length {}").format(self.__next))

            col._match_length(self.capacity())
            tmp = [None] * (len(self.__columns) + 1)
            for i, c in enumerate(self.__columns):
                tmp[i] = c

            tmp[len(self.__columns)] = col
            if name: # override name
                col._name = name

            if col._name:
                if self.__names is None:
                    self.__names = dict()

                self.__names[col._name] = len(self.__columns)

            self.__columns = tmp

        return self

    def remove_column(self, col):
        """Removes the Column from this DataFrame.

        The specified Column argument can be specified as
        a Column index, Column name or Column reference.

        Args:
            col: The index or name of the Column to remove, or the
                Column instance. Must be an int, str or Column

        Returns:
            The removed Column instance if the col argument was
            specified as the index or name of the Column to remove.
            Returns a bool if the col argument was specified as the
            Column instance to remove, in which case this method returns
            True if the specified Column was successfully removed or
            False if the specified Column instance was not part of
            this DataFrame and therefore not removed
        """
        if isinstance(col, raven.struct.dataframe.column.Column):
            # search for Column instance
            if self.__next != -1 and self.__columns is not None:
                for i, c in enumerate(self.__columns):
                    if c is col:
                        self.remove_column(i)
                        return True

            # Column instance was not found in DataFrame
            return False

        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        tmp = [None] * (len(self.__columns) - 1)
        idx = 0
        removed = self.__columns[col]
        for i, c in enumerate(self.__columns):
            if i != col:
                tmp[idx] = c
                idx += 1

        if self.__names is not None:
            name = self.__columns[col]._name
            if name:
                del self.__names[name]

            for key, value in self.__names.items():
                if value >= col:
                    self.__names[key] = value-1

        self.__columns = tmp
        return removed

    def insert_column(self, index, col=None, name=None):
        """Inserts the provided Column at the specified index to this DataFrame.

        Shifts the Column currently at that position and any subsequent Columns
        to the right (adds one to their indices).

        If the specified Column is empty then a new Column instance with the same
        name and type as the specified Column is created and its length is set to
        match the number of rows within this DataFrame. If this DataFrame
        implementation supports null values, then all missing Column entries are
        initialized with null values. If this DataFrame implementation does not support
        null values, then all missing Column entries are initialized with the default
        value of the corresponding Column.

        If the underlying DataFrame implementation supports null values and has a
        deviating size or the provided Column has a deviating size, then the DataFrame
        will refill all missing entries with None values to match the largest Column.
        If the underlying DataFrame implementation does not support null values,
        then the size of the provided Column must match the size of the already
        existing Columns.

        If the inserted Column was labeled during its construction, then it will be
        referenceable by its name. If the name argument is specified, then
        the label of the Column will get overridden by the specified name
        before it is inserted.

        Args:
            index: The index at which the specified column is to be inserted, as an int
            col: The Column to be inserted
            name: The name of the Column to insert. Must be a str

        Returns:
            This DataFrame instance
        """
        if col is None:
            raise DataFrameException(
                "Invalid argument 'col'. Argument must not be None")

        if self.__is_nullable:
            if not col.is_nullable():
                raise DataFrameException(
                    "NullableDataFrame must use NullableColumn instance")

        else:
            if col.is_nullable():
                raise DataFrameException(
                    "DefaultDataFrame cannot use NullableColumn instance")

        if name is not None:
            if not isinstance(name, str):
                raise DataFrameException(
                    ("Invalid argument 'name'. Expected "
                     "str but found {}").format(type(name)))

            col._name = name

        if col.capacity() == 0 and self.__next > 0:
            col = raven.struct.dataframe.column.Column.like(col, self.__next)

        if self.__next == -1:
            if index != 0:
                raise DataFrameException("Invalid column index: {}".format(index))

            self.__columns = [None]
            self.__columns[0] = col
            self.__next = col.capacity()
            if col._name:
                self.__names = dict()
                self.__names[col._name] = 0

        else:
            if index < 0 or index > len(self.__columns):
                raise DataFrameException("Invalid column index: {}".format(index))

            # check column length
            if self.__is_nullable:
                if col.capacity() > self.__next:
                    # match column length in this DataFrame
                    diff = col.capacity() - self.__next
                    csize = len(self.__columns)
                    for i in range(diff):
                        self.add_row([None] * csize)
            else:
                if col.capacity() != self.__next:
                    raise DataFrameException(
                        ("Invalid column length. Must be "
                         "of length {}").format(self.__next))

            col._match_length(self.capacity())
            tmp = [None] * (len(self.__columns)+1)
            for i in range(len(tmp)-1, index, -1):
                tmp[i] = self.__columns[i-1]

            tmp[index] = col
            for i in range(index):
                tmp[i] = self.__columns[i]

            self.__columns = tmp
            if self.__names is not None:
                for key, value in self.__names.items():
                    if value >= index:
                        self.__names[key] = value+1

            if col._name:
                if self.__names is None:
                    self.__names = dict()

                self.__names[col._name] = index

        return self

    def contains(self, col, regex):
        """Indicates whether the specified Column contains an element
        that matches the specified regular expression.

        Args:
            col: The index or name of the Column to search.
                Must be an int or str
            regex: The regular expression that an element in the
                specified Column must match. May be None

        Returns:
            True if the specified Column contains at least one
            element that matches the given regular expression
        """
        return self.index_of(col, regex=regex) != -1

    def columns(self):
        """Indicates the number of Columns this DataFrame currently holds.

        Returns:
            The number of columns of this DataFrame, as an int
        """
        return len(self.__columns) if self.__columns is not None else 0

    def capacity(self):
        """Indicates the capacity of each Column within this DataFrame.

        The capacity is the number of entries any given Column can hold
        without the need of resizing. Therefore this method is different
        from rows() because capacity() also indicates the allocated space
        of the underlying array of each Column.

        Returns:
            The capacity of each Column of this DataFrame, as an int
        """
        return self.__columns[0].capacity() if self.__columns is not None else 0

    def rows(self):
        """Indicates the number of rows this DataFrame currently holds.

        Returns:
            The number of rows of this DataFrame, as an int
        """
        return self.__next if self.__columns is not None else 0

    def is_empty(self):
        """Indicates whether this DataFrame is empty, i.e. it has no rows.

        Returns:
            True if this DataFrame is empty, False otherwise
        """
        return self.__next <= 0

    def is_nullable(self):
        """Indicates whether this DataFrame supports null values.

        In Python, the term 'null' and 'null value' is equivalent to 'None'
        and 'None type' respectively, with regard to the DataFrame API.

        Returns:
            True if this DataFrame supports null values,
            False if it does not support null values
        """
        return self.__is_nullable

    def clear(self):
        """Removes all rows from this DataFrame and frees up allocated space.

        However, the column structure will not be changed by this operation.
        """
        for col in self.__columns:
            col._remove(0, self.__next, self.__next)

        self.__next = 0
        self._flush_all(2)

    def flush(self):
        """Changes the capacity of each Column to match the actually needed
        space by the entries currently in this DataFrame. Therefore, subsequently
        adding rows will require further resizing.

        This method can be called when unnecessary space allocation
        should get freed up.
        """
        if self.__next != -1 and self.__next != self.__columns[0].capacity():
            self._flush_all(0)

    def get_column(self, col):
        """Gets a reference of the Column instance with the specified
        name or index.

        Any changes to values in that Column are reflected in the
        DataFrame and vice versa.

        Args:
            col: The index or name of the Column to get.
                Must be an int or str

        Returns:
            The Column with the specified name or at the specified index
        """
        if not isinstance(col, (int, str)):
            raise DataFrameException(
                ("Invalid argument 'col'. Expected int or "
                 "str but found {}").format(type(col)))

        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        return self.__columns[col]

    def get_columns(self, cols=None, types=None):
        """Returns a DataFrame consisting of all Columns that
        match the specified condition.

        This method can be used in two ways. The first way specifies the
        indices and/or the names of all Columns to get. Use the 'cols'
        argument to specify all indices or names to select. Names and indices
        can be mixed within the 'cols' tuple argument but no validation regarding
        duplicate Columns is performed. Selecting the same Column multiple
        times will result in undefined behaviour with regard to
        the returned DataFrame.

        The second way that Columns can be selected is by the type
        of their elements. Use the 'types' argument to specify all element
        type names to select. All type names must be specified as a string
        denoting a standardized name of the element types to select.
        The following type names are supported:

        'byte', 'short', 'int', 'long', 'string', 'float', 'double',
        'char', 'boolean', 'binary'

        Additionally, the type name 'number' will match all numeric Columns.

        Both Column selection ways cannot be mixed within one method call,
        i.e. either the 'cols' or 'types' argument can be specified but not
        both at the same time.

        Please note that the selected Column instances are only passed to the
        returned DataFrame by reference. Therefore, changing values within
        the returned DataFrame has the same effect on this DataFrame and
        vice versa. However, adding or removing rows produces an inconsistency
        between this and the returned DataFrame. If the row structure of either
        DataFrame is to be manipulated, then ensure to copy the DataFrame returned
        by this method.

        The order of Columns in the returned DataFrame is equal to the order
        of the specified names or, when Columns are selected by types, the order
        they occur in this DataFrame.

        Args:
            cols: The indices and/or names of all Column instances to select.
                Must be a tuple of int, str. This argument cannot be used
                together with 'types'
            types: The element type names of all Column instances to select.
                Must be a tuple of str. This argument cannot be used together
                with 'cols'

        Returns:
            A DataFrame containing references to all Columns denoted by the
            specified Column indices, names or element type names
        """
        if cols is None and types is None:
            raise DataFrameException("Unable to get columns. No arguments specified")

        if self.__next == -1:
            raise DataFrameException("DataFrame has no columns to select")

        if not (cols is None) ^ (types is None):
            raise DataFrameException(
                ("Invalid arguments. Specify either 'cols' or 'types' "
                 "but not both"))

        self.flush()
        result = NullableDataFrame() if self.__is_nullable else DefaultDataFrame()

        if cols is not None:
            # match columns by their index or name
            if isinstance(cols, (int, str)):
                cols = (cols, )
            elif not isinstance(cols, (list, tuple)):
                raise DataFrameException(
                    ("Column selection by index or name must "
                     "be specified as tuple of int, str"))

            for col in cols:
                if isinstance(col, int):
                    result.add_column(self.get_column(col))
                elif isinstance(col, str):
                    result.add_column(self.__columns[self._enforce_name(col)])
                else:
                    raise DataFrameException(
                        ("Invalid column selection argument. "
                         "Expected int or str but found {}").format(type(col)))

        else:
            # match columns by their element type
            if isinstance(types, str):
                types = (types, )
            elif not isinstance(types, (list, tuple)):
                raise DataFrameException(
                    ("Column selection by type name must be "
                     "specified by tuple of str"))

            all_types = {"byte", "short", "int", "long", "string", "float",
                         "double", "char", "boolean", "binary", "number"}

            # check if specified args are in allowed keywords
            for coltype in types:
                if isinstance(coltype, str):
                    if not coltype in all_types:
                        raise DataFrameException(
                            ("Invalid column selection "
                             "argument: '{}'").format(coltype))
                else:
                    raise DataFrameException(
                        ("Invalid column selection argument. "
                         "Expected str but found {}").format(type(coltype)))

            allow_number = "number" in types
            # add matching columns to result DataFrame
            for col in self.__columns:
                if allow_number and col.is_numeric():
                    result.add_column(col)

                elif col.type_name() in types:
                    result.add_column(col)

        return result

    def set_column(self, position, col):
        """Sets the specified Column to be part of this DataFrame.

        The position argument can be either a column index or a column name.

        If the position is specified as an int and if the specified Column has
        a label associated with it, then that label will be incorporated into
        the DataFrame. If the provided Column is not labeled, then the label of
        the provided Column will be set to the label of the replaced Column
        at the specified index.

        If the position is specified as a string and if a Column with the
        specified name already exists in this DataFrame, it will be replaced by
        the specified Column. If no Column with the specified name exists in this
        DataFrame, then the specified Column will be added to it. If the specified
        name differs from the set label of the specified Column, the provided string
        will take precedence and the name of the Column will be set to
        the specified name.

        Args:
            position: The index or name of the Column to set. Must be an int or str
            col: The Column to set within this DataFrame. Must not be None

        Returns:
            This DataFrame instance
        """
        if position is None:
            raise DataFrameException("Invalid argument 'position'. Argument must not be None")

        if col is None:
            raise DataFrameException("Invalid argument 'col'. Argument must not be None")

        if self.__is_nullable:
            if not col.is_nullable():
                raise DataFrameException(
                    "NullableDataFrame must use NullableColumn instance")
        else:
            if col.is_nullable():
                raise DataFrameException(
                    "DefaultDataFrame cannot use NullableColumn instance")

        if isinstance(position, str):
            if self.has_column(position):
                col._name = position
                return self.set_column(self._enforce_name(position), col)
            else:
                return self.add_column(col, name=position)
        elif isinstance(position, int):
            index = position
        else:
            raise DataFrameException(
                ("Invalid argument 'position'. Expected int "
                 "or str but found {}".format(type(position))))

        if self.__next == -1 or index < 0 or index >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(index))

        if col.capacity() == 0 and self.__next > 0:
            col = raven.struct.dataframe.column.Column.like(col, length=self.__next)

        # check column length
        if self.__is_nullable:
            if col.capacity() > self.__next:
                # match column length in this DataFrame
                diff = col.capacity() - self.__next
                csize = len(self.__columns)
                for _ in range(diff):
                    self.add_row([None] * csize)
        else:
            if col.capacity() != self.__next:
                raise DataFrameException(
                    ("Invalid column length. Must be "
                     "of length {}").format(self.__next))

        col._match_length(self.capacity())
        old_name = self.__columns[index]._name
        self.__columns[index] = col
        if col._name:
            if self.__names is not None and old_name is not None:
                del self.__names[old_name]

            if self.__names is None:
                self.__names = dict()

            self.__names[col._name] = index
        else:
            col._name = old_name

        return self

    def convert(self, col, typecode):
        """Converts the specified Column to a Column instance of the specified
        type code.

        This method may raise a DataFrameException if the specified Column
        cannot be converted.

        Optionally, this method also allows the typecode argument to be specified
        as the string type name of the target Column.

        The following type names can be used:

            "byte", "short", "int", "long", "float", "double", "string", "char",
            "boolean", "binary"

        Args:
            col: The index or name of the Column to convert and replace.
                Must be an int or str
            typecode: The type code or type name of the Column to convert the
                specified Column to. Must be an int or str

        Returns:
            This DataFrame instance
        """
        if not isinstance(col, (int, str)):
            raise DataFrameException(
                ("Invalid argument 'col'. Expected int or "
                 "str but found {}").format(type(col)))

        if not isinstance(typecode, (int, str)):
            raise DataFrameException(
                ("Invalid argument 'typecode'. Expected int or "
                 "str but found {}").format(type(typecode)))

        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        c = self.__columns[col]

        if isinstance(typecode, str):
            coltype = dataframeutils.column_from_typename(typecode)
            if coltype is None:
                raise DataFrameException(
                    ("Invalid argument 'typecode'. "
                     "Invalid column element type: '{}'").format(typecode))

            if self.__is_nullable:
                coltype = coltype.as_nullable()

            typecode = coltype.type_code()

        if c.type_code() == typecode: #NO-OP
            return self

        self.flush()
        try:
            c = c.convert_to(typecode)
        except ValueError as ex:
            raise DataFrameException("Cannot convert column. Invalid value encountered") from ex

        if self.__is_nullable ^ c.is_nullable():
            raise DataFrameException(
                ("NullableDataFrame must use NullableColumn instance"
                 if self.__is_nullable
                 else "DefaultDataFrame cannot use NullableColumn instance"))

        self.__columns[col] = c
        return self

    def index_of(self, col, regex, start_from=0):
        """Computes and returns the row index of the first occurrence that matches
        the specified regular expression in the specified Column.

        The start_from argument specifies the row index to start searching from.
        A regex value of None will match null values.

        Args:
            col: The index or name of the Column to search. Must be an int or str
            regex: The regular expression to search for, as a str. May be None

        Returns:
            The index of the row which matches the given regular expression in
            the specified Column, as an int.
            Returns -1 if nothing in the Column matches the given
            regular expression
        """
        if regex is not None and not isinstance(regex, str):
            raise DataFrameException(
                ("Invalid argument 'regex'. "
                 "Expected str but found {}").format(type(regex)))

        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        if regex is None or regex == "null":
            regex = "None"

        if regex == "NaN":
            regex = "nan"

        if start_from < 0 or start_from >= self.__next:
            raise DataFrameException(
                "Invalid argument 'start_from': {}".format(start_from))

        column = self.__columns[col]
        pattern = regex_matcher.compile(regex)
        for i in range(start_from, self.__next, 1):
            if pattern.fullmatch(str(column[i])):
                return i

        return -1

    def index_of_all(self, col, regex):
        """Computes and returns the row indices of all occurrences that match
        the specified regular expression in the Column with the specified name.

        A regex value of None will match null values.

        Args:
            col: The index or name of the Column to search. Must be an int or str
            regex: The regular expression to search for, as a str. May be None

        Returns:
            A list containing all row indices in proper order of all occurrences
            that match the given regular expression.
            Returns an empty list if nothing in the Column matches
            the given regular expression
        """
        if regex is not None and not isinstance(regex, str):
            raise DataFrameException(
                ("Invalid argument 'regex'. "
                 "Expected str but found {}").format(type(regex)))

        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        if regex is None or regex == "null":
            regex = "None"

        if regex == "NaN":
            regex = "nan"

        column = self.__columns[col]
        indices = []
        pattern = regex_matcher.compile(regex)
        for i in range(self.__next):
            if pattern.fullmatch(str(column[i])):
                indices.append(i)

        return [] if len(indices) == 0 else indices

    def filter(self, col, regex):
        """Computes and returns a DataFrame containing all rows that match the
        specified regular expression in the specified Column.

        This DataFrame is not changed by this operation. A regex value of None
        will match null values.

        All rows in the returned DataFrame are copies of the original rows, so
        changing values within the returned DataFrame has no effect on the
        original DataFrame and vice versa. Please note that this does not apply
        to bytearray objects of BinaryColumns, in which case the references
        to the underlying bytearray objects are copied to the rows of
        the returned DataFrame.

        Args:
            col: The index or name of the Column to search. Must be an int or str
            regex: The regular expression to search for, as a str. May be None

        Returns:
            A sub-DataFrame containing all rows that match the given regular
            expression in the specified Column.
            Returns an empty DataFrame if nothing in the Column matches the
            given regular expression
        """
        if regex is not None and not isinstance(regex, str):
            raise DataFrameException(
                ("Invalid argument 'regex'. "
                 "Expected str but found {}").format(type(regex)))

        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        if regex is None or regex == "null":
            regex = "None"

        if regex == "NaN":
            regex = "nan"

        indices = self.index_of_all(col, regex)
        n_rows = len(indices)
        cols = [None] * len(self.__columns)
        for i, c in enumerate(self.__columns):
            cols[i] = raven.struct.dataframe.column.Column.of_type(c.type_code(), length=n_rows)

        df = NullableDataFrame(cols) if self.__is_nullable else DefaultDataFrame(cols)

        for i, index in enumerate(indices):
            df.set_row(i, self.get_row(index))

        if self.__names is not None:
            df.set_column_names(*self.get_column_names())

        return df

    def include(self, col, regex):
        """Retains all rows in this DataFrame that match the specified regular
        expression in the specified Column.

        A regex value of None will match null values.

        Args:
            col: The index or name of the Column to search. Must be an int or str
            regex: The regular expression to search for, as a str. May be None

        Returns:
            This DataFrame instance
        """
        if regex is not None and not isinstance(regex, str):
            raise DataFrameException(
                ("Invalid argument 'regex'. "
                 "Expected str but found {}").format(type(regex)))

        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        if regex is None or regex == "null":
            regex = "None"

        if regex == "NaN":
            regex = "nan"

        column = self.__columns[col]
        pattern = regex_matcher.compile(regex)
        i = 0
        k = -1
        while i < self.__next:
            if not pattern.fullmatch(str(column[i])):
                if k == -1:
                    k = i

                i += 1
            else:
                if k != -1:
                    self.remove_rows(from_index=k, to_index=i)
                    i -= (i - k)
                    k = -1
                else:
                    i += 1

        if k != -1:
            self.remove_rows(from_index=k, to_index=i)

        return self

    def drop(self, col, regex):
        """Computes and returns a DataFrame containing all rows that do not
        match the specified regular expression in the specified Column.

        This DataFrame is not changed by this operation. A regex value of None
        will match null values.

        All rows in the returned DataFrame are copies of the original rows,
        so changing values within the returned DataFrame has no effect on the
        original DataFrame and vice versa. Please note that this does not apply
        to bytearray object of BinaryColumns, in which case the references to the
        underlying bytearray object are copied to the rows
        of the returned DataFrame.

        Args:
            col: The index or name of the Column to search. Must be an int or str
            regex: The regular expression to search for, as a str. May be None

        Returns:
            A sub-DataFrame containing all rows that do not match the given
            regular expression in the specified Column.
            Returns an empty DataFrame if everything in the Column matches
            the given regular expression
        """
        if regex is not None and not isinstance(regex, str):
            raise DataFrameException(
                ("Invalid argument 'regex'. "
                 "Expected str but found {}").format(type(regex)))

        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        if regex is None or regex == "null":
            regex = "None"

        if regex == "NaN":
            regex = "nan"

        column = self.__columns[col]
        pattern = regex_matcher.compile(regex)

        result = NullableDataFrame() if self.__is_nullable else DefaultDataFrame()
        for c in self.__columns:
            result.add_column(raven.struct.dataframe.column.Column.of_type(c.type_code()))

        for i in range(self.__next):
            if not pattern.fullmatch(str(column[i])):
                result.add_row(self.get_row(i))

        if self.__names is not None:
            result.set_column_names(self.get_column_names())

        result.flush()
        return result

    def exclude(self, col, regex):
        """Removes all rows in this DataFrame that match the specified regular
        expression in the specified Column.

        A regex value of None will match null values.

        Args:
            col: The index or name of the Column to search. Must be an int or str
            regex: The regular expression to search for, as a str. May be None

        Returns:
            This DataFrame instance
        """
        if regex is None or regex == "null":
            regex = "None"

        if not isinstance(regex, str):
            raise DataFrameException(
                ("Invalid argument 'regex'. "
                 "Expected str but found {}").format(type(regex)))

        self.remove_rows(col, regex=regex)
        return self

    def replace(self, col=None, regex=None, replacement=None, df=None):
        """Replaces all values in the specified Column that match the specified
        regular expression.

        All matched values are replaced with the value returned by the specified
        replacement function. If the underlying DataFrame implementation doesn't
        support null values, then the value returned by the specified replacement
        function must not be None. The replacement function can also be specified
        as a constant value of the corresponding element type of the
        specified Column.

        Passing either None or an empty string as the regex argument to this method
        is equivalent to matching all values.

        The replacement function must take either a single argument
        (v: the current value) or two arguments
        (i: the row index, v: the current value) and return a single value of the
        corresponding element type of the underlying Column, or None if
        the Column permits null values.

        If the 'df' argument is specified, then this method replaces all Columns in
        this DataFrame with matched Columns from the specified DataFrame. If both
        DataFrame instances have labeled Columns, then matching is performed via
        Column names. If both DataFrame instances are not labeled, then all Columns
        are set from lower indices to higher indices, i.e. left to right, from the
        specified DataFrame. Please note that DataFrames must be both either labeled
        or unlabeled. Both DataFrames must have the same number of rows.

        Args:
            col: The index or name of the Column to replace values in.
                Must be an int or str
            regex: The regular expression that all Column values to be replaced
                must match, as a str. May be None or empty
            replacement: The replacement function to determine the new value
                for each matched position. Passing None as a replacement argument
                will result in no change being applied
            df: The DataFrame instance holding all Columns that should replace the
                corresponding Columns in this instance. It must have the same number
                of rows as this DataFrame. All other arguments must be None when this
                argument is used. This argument is optional and may be None

        Returns:
            The number of values that were replaced by this operation. If the 'df'
            argument was specified, this method returns the number of Column instances
            that were replaced by this operation
        """
        if df is not None:
            if col is not None or regex is not None or replacement is not None:
                raise DataFrameException(
                    ("Invalid arguments. Argument 'df' was "
                     "specified but other args are not None"))

            return self._replace_by_datafarame(df)
        else:
            if col is None:
                raise DataFrameException(
                    ("Invalid arguments. "
                     "Argument 'col' was not specified"))

            return self._replace_by_match(col, regex, replacement)

    def factor(self, col):
        """Changes the categorical data in the specified Column into factors.

        The produced factors are unordered. The specified Column is converted to
        an IntColumn or NullableIntColumn respectively. The conducted change to
        factors is reflected by the returned dictionary, which maps every
        category to the factor in the specified Column.

        If the specified Column is already numeric, then no change is applied
        to this DataFrame and an empty dictionary is returned. If the
        underlying DataFrame implementation supports null values, then None
        values are excluded from this operation.

        Args:
            col: The index or name of the Column to change categories into factors.
                Must be an int or str

        Returns:
            A dictionary holding the mapping from the encountered categories to
            the produced factors
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        c = self.__columns[col]
        if c.is_numeric():
            return dict()

        fmap = dict()
        factors = (intcolumn.NullableIntColumn(values=self.capacity())
                   if self.__is_nullable
                   else intcolumn.IntColumn(values=self.capacity()))

        factors._name = c._name
        total_factors = 0
        for i in range(self.__next):
            val = c.get_value(i)
            if val is None:
                continue

            factor = fmap.get(val)
            if factor is not None:
                factors[i] = factor
            else:
                total_factors += 1
                fmap[val] = total_factors
                factors[i] = total_factors

        self.__columns[col] = factors
        return fmap

    def count(self, col, regex=None):
        """Counts the occurrence of values in the specified Column.

        If the regex argument is None, then this method counts the number of
        occurrences of all unique values in the specified column. Every unique
        value is described by a row in the returned DataFrame. It has three
        Columns: The Column at index 0 is of the same type as the specified
        Column and it contains all unique values encountered in the
        specified Column, with the same name if set in this DataFrame.
        The Column at index 1 ("count") contains the quantity of the corresponding
        value as an int. The Column at index 2 ("%") contains the quantity of
        each value relative to the total number of rows in this
        DataFrame as a float.

        If the underlying DataFrame implementation supports null values,
        then the occurrence of None values is included as the last row in
        the returned DataFrame.

        If the regex argument is not None, then this method counts the number
        of occurrences in the specified Column that match the specified
        regular expression. In that case, this method returns an int denoting
        the number of matches.

        Args:
            col: The index or name of the Column to count values for.
                Must be an int or str
            regex: The regular expression to count matches for, as a str.
                May be None

        Returns:
            A DataFrame describing the count of every unique value in this DataFrame,
            if the regex argument is None. The returned DataFrame is of the same
            type as this DataFrame. If the regex argument is not None, then this
            method returns an int which denotes the number of regex matches
            in the specified Column
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        if regex is not None and not isinstance(regex, str):
            raise DataFrameException(
                ("Invalid argument 'regex'. Expected str "
                 "but found {}").format(type(regex)))

        if regex:
            # count the number of matches in the specified column
            column = self.__columns[col]
            pattern = regex_matcher.compile(regex)
            elem_count = 0
            for i in range(self.__next):
                if pattern.fullmatch(str(column.get_value(i))):
                    elem_count += 1

            return elem_count

        # create a DataFrame with the frequencies
        # of all unique element values
        column = self.__columns[col]
        if self.__is_nullable:
            result = NullableDataFrame(
                raven.struct.dataframe.column.Column.of_type(column.type_code()),
                intcolumn.NullableIntColumn("count"),
                floatcolumn.NullableFloatColumn("%"))
        else:
            result = DefaultDataFrame(
                raven.struct.dataframe.column.Column.of_type(column.type_code()),
                intcolumn.IntColumn("count"),
                floatcolumn.FloatColumn("%"))

        name = column._name
        if name:
            if name in ("count", "%"):
                name = name + "_"

            result.set_column_name(0, name)

        cmap = dict()
        for i in range(self.__next):
            value = column.get_value(i)
            count = cmap.get(value)
            if count is not None:
                cmap[value] = count + 1
            else:
                cmap[value] = 1

        for key, value in cmap.items():
            if key is not None: # skip null counts
                result.add_row([key, value, float(value) / self.__next])

        if self.__is_nullable:
            # add null count as the last row
            if None in cmap:
                result.add_row([None,
                                cmap.get(None),
                                float(cmap.get(None)) / self.__next])

        return result

    def count_unique(self, col):
        """Counts the number of unique elements in the specified Column.

        If the underlying DataFrame implementation supports null values,
        then the occurrence of None values is excluded in the computed number

        Args:
            col: The index or name of the Column to count the number
                of unique elements for. Must be an int or str

        Returns:
            The number of unique non-null elements in the specified Column,
            as an int
        """
        return len(self.unique(col))

    def unique(self, col):
        """Returns the set of unique elements in the specified column.

        If the underlying DataFrame implementation supports null values,
        then None values are not included in the computed set.

        The returned set contains elements whose types are equal to the
        element types in the underlying Column.

        Args:
            col: The index or name of the Column to return all unique
                elements for

        Returns:
            A set which contains all unique elements in the specified Column
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        if self.rows() == 0:
            return set()

        column = self.__columns[col]
        values = column.as_array()
        if self.__is_nullable:
            values = values[values != None]

        unique = np.unique(values)
        # in-place replacement for bytearray objects to bytes
        # objects since bytearrays are not hashable
        if column.type_name() == "binary":
            for i, _ in enumerate(unique):
                unique[i] = bytes(unique[i])

        # convert array to set
        unique = set(unique)
        # convert uint8 ASCII codes to strings for unique
        # values in CharColumns and NullableCharColumns
        if column.type_name() == "char":
            converted = set()
            for elem in unique:
                converted.add(chr(elem))

            unique = converted

        return unique

    def difference_columns(self, df):
        """Computes the set-theoretic difference of this DataFrame and the
        specified DataFrame instance.

        The difference is created with respect to all encountered Columns. This
        operation therefore returns a DataFrame with all Columns that are part
        of either this DataFrame or the specified DataFrame instance but not
        both. Columns are only matched by their name. Therefore, all Columns
        must be labeled at the time this method is called. The specified
        DataFrame must have the same type and number of rows as this DataFrame.

        All Column instances included in the returned DataFrame are only added by
        reference. Therefore, changing values within the returned DataFrame has the
        same effect on the respective DataFrame and vice versa. However, adding or
        removing rows produces an inconsistency between this and the returned
        DataFrame. If the row structure of any DataFrame involved in this operation
        is to be manipulated, then ensure to copy the DataFrame
        returned by this method

        Args:
            df: The DataFrame instance to be used in the difference operation

        Returns:
            A DataFrame holding references to all Columns that are either in
            this DataFrame or the specified DataFrame but not in both
        """
        self._ensure_valid_column_set_operation(df)
        result = NullableDataFrame() if self.__is_nullable else DefaultDataFrame()
        for i, col in enumerate(self.__columns):
            name = col._name
            if not name:
                raise DataFrameException(
                    ("Encountered an unlabeled "
                     "column at index {}".format(i)))

            if not df.has_column(name):
                result.add_column(col)

        for i, col in enumerate(df.__columns):
            name = col._name
            if not name:
                raise DataFrameException(
                    ("Encountered an unlabeled "
                     "column in the argument DataFrame "
                     "at index {}".format(i)))

            if not self.has_column(name):
                result.add_column(col)

        return result

    def union_columns(self, df):
        """Computes the set-theoretic union of this DataFrame and the
        specified DataFrame instance.

        The union is created with respect to all encountered Columns. This
        operation therefore returns a DataFrame with all Columns from both this
        DataFrame and the specified DataFrame instance, ignoring duplicates.
        In the case of duplicates, the returned DataFrame only holds the Column
        references from this DataFrame. Columns are only matched by their name.
        Therefore, all Columns must be labeled at the time this method is called.
        The specified DataFrame must have the same type and number of rows
        as this DataFrame.

        All Column instances included in the returned DataFrame are only added by
        reference. Therefore, changing values within the returned DataFrame has the
        same effect on the respective DataFrame and vice versa. However, adding or
        removing rows produces an inconsistency between this and the returned DataFrame.
        If the row structure of any DataFrame involved in this operation is to be
        manipulated, then ensure to copy the DataFrame returned by this method

        Args:
            df: The DataFrame instance to be used in the union operation

        Returns:
            A DataFrame holding references to all columns from both this
            DataFrame and the specified DataFrame instance, ignoring duplicates
        """
        self._ensure_valid_column_set_operation(df)
        result = NullableDataFrame() if self.__is_nullable else DefaultDataFrame()
        for i, col in enumerate(self.__columns):
            name = col._name
            if not name:
                raise DataFrameException(
                    ("Encountered an unlabeled "
                     "column at index {}".format(i)))

            result.add_column(col)

        for i, col in enumerate(df.__columns):
            name = col._name
            if not name:
                raise DataFrameException(
                    ("Encountered an unlabeled "
                     "column in the argument DataFrame "
                     "at index {}".format(i)))

            if not result.has_column(name):
                result.add_column(col)

        return result

    def intersection_columns(self, df):
        """Computes the set-theoretic intersection of this DataFrame and the
        specified DataFrame instance.

        The intersection is created with respect to all encountered Columns. This
        operation therefore returns a DataFrame with all Columns from this DataFrame
        that are also in the specified DataFrame instance. The returned DataFrame
        only holds the Column references from this DataFrame. Columns are only
        matched by their name. Therefore, all Columns must be labeled at the time
        this method is called. The specified DataFrame must have the same type
        and number of rows as this DataFrame.

        All Column instances included in the returned DataFrame are only added by
        reference. Therefore, changing values within the returned DataFrame has the
        same effect on the respective DataFrame and vice versa. However, adding or
        removing rows produces an inconsistency between this and the returned
        DataFrame. If the row structure of any DataFrame involved in this operation
        is to be manipulated, then ensure to copy the DataFrame returned by this method

        Args:
            df: The DataFrame instance to be used in the intersection operation

        Returns:
            A DataFrame holding references to all Columns from this DataFrame also
            present in the specified DataFrame instance
        """
        self._ensure_valid_column_set_operation(df)
        result = NullableDataFrame() if self.__is_nullable else DefaultDataFrame()
        for i, col in enumerate(self.__columns):
            name = col._name
            if not name:
                raise DataFrameException(
                    ("Encountered an unlabeled "
                     "column at index {}".format(i)))

            if df.has_column(name):
                result.add_column(col)

        return result

    def difference_rows(self, df):
        """Computes the set-theoretic difference of this DataFrame and the
        specified DataFrame instance.

        The difference is created with respect to all encountered rows. This operation
        therefore returns a DataFrame with all rows that are part of either this
        DataFrame or the specified DataFrame instance but not both. Both DataFrame
        instances must have either labeled or unlabeled Columns. The specified
        DataFrame must have the same Column structure and order as this DataFrame,
        however, it may be of any type.

        All rows included in the returned DataFrame are copies of the original values
        with the exception of values from binary columns which are passed by reference.

        Args:
            df: The DataFrame instance to be used in the difference operation

        Returns:
            A DataFrame holding all rows that are either in this DataFrame or the
            specified DataFrame but not in both
        """
        self._ensure_valid_row_set_operation(df)
        result = NullableDataFrame() if self.__is_nullable else DefaultDataFrame()
        for _, col in enumerate(self.__columns):
            result.add_column(raven.struct.dataframe.column.Column.of_type(col.type_code()))

        if self.has_column_names():
            result.set_column_names(self.get_column_names())

        arg_rows = df.rows()
        hash0 = [0] * self.__next
        hash1 = [0] * arg_rows
        for i in range(self.__next):
            hash0[i] = hash(tuple(self.get_row(i)))

        for i in range(arg_rows):
            hash1[i] = hash(tuple(df.get_row(i)))

        for i in range(self.__next):
            row = self.get_row(i)
            match = False
            for j in range(arg_rows):
                if hash0[i] == hash1[j]:
                    if row == df.get_row(j):
                        match = True
                        break

            if not match:
                for k in range(i):
                    if hash0[i] == hash0[k]:
                        if row == self.get_row(k):
                            match = True

                if not match:
                    result.add_row(row)

        for i in range(arg_rows):
            row = df.get_row(i)
            match = False
            for j in range(self.__next):
                if hash1[i] == hash0[j]:
                    if row == self.get_row(j):
                        match = True
                        break

            if not match:
                for k in range(i):
                    if hash1[i] == hash1[k]:
                        if row == df.get_row(k):
                            match = True

                if not match:
                    result.add_row(row)

        return result

    def union_rows(self, df):
        """Computes the set-theoretic union of this DataFrame and the
        specified DataFrame instance.

        The union is created with respect to all encountered rows. This operation
        therefore returns a DataFrame with all rows from both this DataFrame and
        the specified DataFrame instance, ignoring duplicates. Both DataFrame instances
        must have either labeled or unlabeled Columns. The specified DataFrame must
        have the same Column structure and order as this DataFrame, however, it may
        be of any type.

        All rows included in the returned DataFrame are copies of the original values
        with the exception of values from binary columns which are passed by reference.

        Args:
            df: The DataFrame instance to be used in the union operation

        Returns:
            A DataFrame holding all rows from both this DataFrame and the specified
            DataFrame instance, ignoring duplicates
        """
        self._ensure_valid_row_set_operation(df)
        result = NullableDataFrame() if self.__is_nullable else DefaultDataFrame()
        for _, col in enumerate(self.__columns):
            result.add_column(raven.struct.dataframe.column.Column.of_type(col.type_code()))

        if self.has_column_names():
            result.set_column_names(self.get_column_names())

        arg_rows = df.rows()
        hash0 = [0] * self.__next
        hash1 = [0] * arg_rows
        for i in range(self.__next):
            hash0[i] = hash(tuple(self.get_row(i)))

        for i in range(arg_rows):
            hash1[i] = hash(tuple(df.get_row(i)))

        for i in range(self.__next):
            row = self.get_row(i)
            match = False
            for k in range(i):
                if hash0[k] == hash0[i]:
                    if row == self.get_row(k):
                        match = True

            if not match:
                result.add_row(row)

        for i in range(arg_rows):
            row = df.get_row(i)
            match = False
            for j in range(self.__next):
                if hash0[j] == hash1[i]:
                    if row == self.get_row(j):
                        match = True
                        break

            if not match:
                for k in range(i):
                    if hash1[k] == hash1[i]:
                        if row == df.get_row(k):
                            match = True

                if not match:
                    result.add_row(row)

        return result

    def intersection_rows(self, df):
        """Computes the set-theoretic intersection of this DataFrame and the
        specified DataFrame instance.

        The intersection is created with respect to all encountered rows. This
        operation therefore returns a DataFrame with all rows from this DataFrame
        that are also in the specified DataFrame instance. Both DataFrame
        instances must have either labeled or unlabeled Columns. The specified
        DataFrame must have the same Column structure and order as this DataFrame,
        however, it may be of any type.

        All rows included in the returned DataFrame are copies of the original
        values with the exception of values from binary columns which are
        passed by reference.

        Args:
            df: The DataFrame instance to be used in the intersection operation

        Returns:
            A DataFrame holding all rows from this DataFrame that are also in
            the specified DataFrame instance
        """
        self._ensure_valid_row_set_operation(df)
        result = NullableDataFrame() if self.__is_nullable else DefaultDataFrame()
        for _, col in enumerate(self.__columns):
            result.add_column(raven.struct.dataframe.column.Column.of_type(col.type_code()))

        if self.has_column_names():
            result.set_column_names(self.get_column_names())

        arg_rows = df.rows()
        hash0 = [0] * self.__next
        hash1 = [0] * arg_rows
        for i in range(self.__next):
            hash0[i] = hash(tuple(self.get_row(i)))

        for i in range(arg_rows):
            hash1[i] = hash(tuple(df.get_row(i)))

        for i in range(self.__next):
            row = self.get_row(i)
            match = False
            for j in range(arg_rows):
                if hash0[i] == hash1[j]:
                    if row == df.get_row(j):
                        match = True
                        break

            if match:
                # check for duplicate row already
                # in the result DataFrame
                for k in range(i):
                    if hash0[i] == hash0[k]:
                        # hashes match. Check for equality
                        if row == self.get_row(k):
                            # duplicate row
                            match = False

                if match:
                    result.add_row(row)

        return result

    def group_minimum_by(self, col):
        """Groups minimum values in all numeric Columns by the unique
        values in the specified Column.

        Every unique value in the specified Column is represented by a row in
        the returned DataFrame. The summary Column is located at index 0. All
        subsequent Columns hold the minimum values for the corresponding unique
        entry in the specified Column.

        All Columns must be labeled at the time this method is called. All
        Columns in the returned DataFrame have the same type and name
        as their correspondent.

        Args:
            col: The index or name of the Column to group minimum values for.
                Must be an int or str

        Returns:
            A DataFrame holding all minimum values in all numeric Columns for each
            unique value in the specified Column
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        return dataframeutils._group_operation(self, col, 1)

    def group_maximum_by(self, col):
        """Groups maximum values in all numeric Columns by the unique
        values in the specified Column.

        Every unique value in the specified Column is represented by a row in
        the returned DataFrame. The summary Column is located at index 0. All
        subsequent Columns hold the maximum values for the corresponding unique
        entry in the specified Column.

        All Columns must be labeled at the time this method is called. All
        Columns in the returned DataFrame have the same type and name
        as their correspondent

        Args:
            col: The index or name of the Column to group maximum values for.
                Must be an int or str

        Returns:
            A DataFrame holding all maximum values in all numeric Columns for each
            unique value in the specified Column
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        return dataframeutils._group_operation(self, col, 2)

    def group_average_by(self, col):
        """Groups average values in all numeric Columns by the unique
        values in the specified Column.

        Every unique value in the specified Column is represented by a row in
        the returned DataFrame. The summary Column is located at index 0. All
        subsequent Columns hold the average values for the corresponding unique
        entry in the specified Column.

        All Columns must be labeled at the time this method is called. All
        Columns in the returned DataFrame have the same name as their
        correspondent. All numeric Columns are represented by DoubleColumns or
        NullableDoubleColumns depending on the type of this DataFrame.

        Args:
            col: The index or name of the Column to group average values for.
                Must be an int or str

        Returns:
            A DataFrame holding all average values in all numeric Columns for
            each unique value in the specified Column
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        return dataframeutils._group_operation(self, col, 3)

    def group_sum_by(self, col):
        """Groups sum values in all numeric Columns by the unique
        values in the specified Column.

        Every unique value in the specified Column is represented by a row in
        the returned DataFrame. The summary Column is located at index 0. All
        subsequent Columns hold the sums for the corresponding unique
        entry in the specified Column.

        All Columns must be labeled at the time this method is called. All
        Columns in the returned DataFrame have the same name as their
        correspondent. All numeric Columns are represented by DoubleColumns or
        NullableDoubleColumns depending on the type of this DataFrame.

        Args:
            col: The index or name of the Column to group sum values for.
                Must be an int or str

        Returns:
            A DataFrame holding all sum values in all numeric Columns for
            each unique value in the specified Column
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        return dataframeutils._group_operation(self, col, 4)

    def join(self, df, col1=None, col2=None):
        """Combines all rows from this and the specified DataFrame which have
        matching values in their Columns with the corresponding specified name.

        If neither the 'col1' nor the 'col2' argument is specified, then the
        Column name common to both DataFrames is determined automatically, in
        which case both DataFrames must have exactly one Column with an identical
        name and element type.

        If only one of the two 'col*' arguments is specified, then both DataFrames
        must have one Column with the specified name.

        If both the 'col1' and 'col2' arguments are specified, then this DataFrame
        must have a Column with a name equal to 'col1' and the DataFrame specified
        by the 'df' argument must have a Column with a name equal to 'col2'. Both
        Columns must have an identical element type.

        All Columns in both DataFrame instances must be labeled by the time this
        method is called. The specified DataFrame may be of any type.

        All Columns in the DataFrame argument that are also existent in
        this DataFrame are excluded in the result DataFrame returned by this method.
        Therefore, in the case of duplicate Columns, the returned DataFrame only
        contains the corresponding Column from this DataFrame.

        Args:
            df1: The DataFrame to join. Must not be None
            col1: The name of the Column in this DataFrame to match values for.
                Must be a str
            col2: The name of the Column in the specified DataFrame argument
                to match values for. Must be a str

        Returns:
            A DataFrame with joined rows from both this and the specified DataFrame
            that have matching values in the Columns with the specified names
        """
        if df is None:
            raise DataFrameException(
                "DataFrame argument must not be None")

        if col1 is not None and not isinstance(col1, str):
            raise DataFrameException(
                ("Invalid argument 'col1'. Expected "
                 "str but found {}").format(type(col1)))

        if col2 is not None and not isinstance(col2, str):
            raise DataFrameException(
                ("Invalid argument 'col2'. Expected "
                 "str but found {}").format(type(col2)))

        if not col1 and not col2:
            if not self.has_column_names():
                raise DataFrameException(
                    "DataFrame must has column labels")

            if not df.has_column_names():
                raise DataFrameException(
                    "DataFrame argument must have column labels")

            col = None
            colnames = df.get_column_names()
            for name in colnames:
                if name in self.__names:
                    if col is not None:
                        raise DataFrameException(
                            "DataFrame argument has more than one matching column")

                    col = name

            if col is None:
                raise DataFrameException(
                    "DataFrame argument has no matching column")

            # set the column argument to the common name
            col1 = col

        if col1 and not col2:
            col2 = col1

        if col2 and not col1:
            col1 = col2

        return dataframeutils.join(self, col1, df, col2)

    def average(self, col):
        """ Computes the average of all entries in the specified Column.

        If the underlying DataFrame implementation supports null values,
        then None values are excluded from the computation and do not contribute
        to the total number of entries. The average can only be computed for
        numeric Columns.

        Args:
            col: The index or name of the Column to compute the average for.
                Must be an int or str

        Returns:
            The average of all entries in the specified Column, as a float
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        c = self.__columns[col]
        if not c.is_numeric():
            msg = ("'{}'".format(c._name)
                   if (c._name is not None)
                   else "at index {}".format(col))

            raise DataFrameException(("Unable to compute average. "
                                      "Column {} is not numeric").format(msg))

        if self.rows() == 0:
            return float("NaN")

        sum_value = None
        amount = 0
        if self.__is_nullable:
            array = c._values[c._values != None]
            amount = array.shape[0]
            if amount > 0:
                sum_value = np.sum(array)

        else:
            sum_value = np.sum(c._values[0:self.__next])
            amount = self.rows()

        return sum_value / amount if amount > 0 else float("NaN")

    def median(self, col):
        """Computes the median of all entries in the specified Column.

        If the underlying DataFrame implementation supports null values,
        then None values are excluded from the computation. The median
        can only be computed for numeric Columns.

        Args:
            col: The index or name of the Column to compute the median for.
                Must be an int or str

        Returns:
            The median of all entries in the specified Column, as a float
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        c = self.__columns[col]
        if not c.is_numeric():
            msg = ("'{}'".format(c._name)
                   if (c._name is not None)
                   else "at index {}".format(col))

            raise DataFrameException(("Unable to compute median. "
                                      "Column {} is not numeric").format(msg))

        if self.rows() == 0:
            return float("NaN")

        self.flush()
        values = c.as_array()
        if self.__is_nullable:
            # create a copy of the column excluding all None values
            values = [val for val in values if val is not None]
            # check against empty list
            if len(values) == 0:
                return float("NaN")

            values = np.array(values)

        return float(np.median(values, axis=0))

    def minimum(self, col, rank=None):
        """Computes the minimum or ranked minima in the specified Column.

        This method can be used in two ways. If only the 'col' argument
        is specified, then this method computes the minimum of all
        entries in the specified Column and returns the computed value as
        an int or float number.

        If the 'rank' argument is specified, then this method computes
        the n-minimum entries in the specified Column and returns the
        corresponding rows as a DataFrame. The rank specifies the
        maximum number of rows to return (the number n). The returned
        DataFrame is ordered ascendingly according to the values in the
        specified Column, i.e. the minimum is located at row 0, the
        second minimum at row 1, etc.

        If the underlying DataFrame implementation supports null values,
        then None values are excluded from the computation.
        The minimum can only be computed for numeric Columns.

        Args:
            col: The index or name of the Column to compute the
                minimum for. Must be an int or str
            rank: The maximum number of rows to return, as a
                positive int. This argument may optionally be None

        Returns:
            The minimum of all entries in the specified Column, as an
            int or float. Returns a DataFrame containing at most n
            rows, ordered ascendingly by the specified Column if the
            'rank' argument is specified
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        c = self.__columns[col]
        if not c.is_numeric():
            msg = ("'{}'".format(c._name)
                   if (c._name is not None)
                   else "at index {}".format(col))

            raise DataFrameException(("Unable to compute minimum. "
                                      "Column {} is not numeric").format(msg))

        if rank is not None:
            if not isinstance(rank, int):
                raise DataFrameException(
                    ("Invalid argument 'rank'. Expected int "
                     "but found {}").format(type(rank)))

            return self._minimum_ranked(col, rank)

        if self.rows() == 0:
            return float("NaN")

        min_value = None
        if self.__is_nullable:
            array = c._values[c._values != None]
            if array.shape[0] == 0:
                return float("NaN")

            min_value = np.amin(array)

        else:
            min_value = np.amin(c._values[0:self.__next])

        return float(min_value) if dataframeutils.is_numeric_fp(c) else int(min_value)

    def maximum(self, col, rank=None):
        """Computes the maximum or ranked maxima in the specified Column.

        This method can be used in two ways. If only the 'col' argument
        is specified, then this method computes the maximum of all
        entries in the specified Column and returns the computed value as
        an int or float number.

        If the 'rank' argument is specified, then this method computes
        the n-maximum entries in the specified Column and returns the
        corresponding rows as a DataFrame. The rank specifies the
        maximum number of rows to return (the number n). The returned
        DataFrame is ordered descendingly according to the values in the
        specified Column, i.e. the maximum is located at row 0, the
        second maximum at row 1, etc.

        If the underlying DataFrame implementation supports null values,
        then None values are excluded from the computation.
        The maximum can only be computed for numeric Columns.

        Args:
            col: The index or name of the Column to compute the
                maximum for. Must be an int or str
            rank: The maximum number of rows to return, as a
                positive int. This argument may optionally be None

        Returns:
            The maximum of all entries in the specified Column, as an
            int or float. Returns a DataFrame containing at most n
            rows, ordered descendingly by the specified Column if the
            'rank' argument is specified
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        c = self.__columns[col]
        if not c.is_numeric():
            msg = ("'{}'".format(c._name)
                   if (c._name is not None)
                   else "at index {}".format(col))

            raise DataFrameException(("Unable to compute maximum. "
                                      "Column {} is not numeric").format(msg))

        if rank is not None:
            if not isinstance(rank, int):
                raise DataFrameException(
                    ("Invalid argument 'rank'. Expected int "
                     "but found {}").format(type(rank)))

            return self._maximum_ranked(col, rank)

        if self.rows() == 0:
            return float("NaN")

        max_value = None
        if self.__is_nullable:
            array = c._values[c._values != None]
            if array.shape[0] == 0:
                return float("NaN")

            max_value = np.amax(array)

        else:
            max_value = np.amax(c._values[0:self.__next])

        return float(max_value) if dataframeutils.is_numeric_fp(c) else int(max_value)

    def sum(self, col):
        """Computes the sum of all entries in the specified Column.

        If the underlying DataFrame implementation supports null values,
        then None values are excluded from the computation. The sum can
        only be computed for numeric Columns.

        Args:
            col: The index or name of the Column to compute the sum for.
                Must be an int or str

        Returns:
            The sum of all entries in the specified Column, as an int
            or float.
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        c = self.__columns[col]
        if not c.is_numeric():
            msg = ("'{}'".format(c._name)
                   if (c._name is not None)
                   else "at index {}".format(col))

            raise DataFrameException(
                ("Unable to compute sum. "
                 "Column {} is not numeric").format(msg))

        if self.rows() == 0:
            return float("NaN")

        sum_value = None
        if self.__is_nullable:
            array = c._values[c._values != None]
            if array.shape[0] == 0:
                return float("NaN")

            sum_value = np.sum(array)
        else:
            sum_value = np.sum(c._values[0:self.__next])

        return float(sum_value) if dataframeutils.is_numeric_fp(c) else int(sum_value)

    def absolute(self, col):
        """Computes the absolute value for all numeric values in the
        specified Column.

        All values are replaced by their absolute value.
        If the underlying DataFrame implementation supports null values,
        then None values are excluded from the computation. The absolute can
        only be computed for numeric Columns.

        Args:
            col: The index or name of the Column to compute the absolutes for.
                Must be an int or str

        Returns:
            This DataFrame instance
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        c = self.__columns[col]
        if not c.is_numeric():
            msg = ("'{}'".format(c._name)
                   if (c._name is not None)
                   else "at index {}".format(col))

            raise DataFrameException(("Unable to compute absolutes. "
                                      "Column {} is not numeric").format(msg))

        values = c.as_array()
        for i in range(0, self.__next, 1):
            if values[i] is not None:
                values[i] = abs(values[i])

        return self

    def ceil(self, col):
        """Computes the value from the ceil function for all numeric values
        in the specified Column.

        The ceil function rounds numbers to the next largest integer that is equal
        or greater than the input value. All values in the specified Column are
        replaced by their ceil value. If the underlying DataFrame implementation
        supports null values, then None values are excluded from the computation.
        The ceil can only be computed for numeric Columns.

        Args:
            col: The index or name of the Column to ceil values for.
                Must be an int or str

        Returns:
            This DataFrame instance
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        c = self.__columns[col]
        if not c.is_numeric():
            msg = ("'{}'".format(c._name)
                   if (c._name is not None)
                   else "at index {}".format(col))

            raise DataFrameException(("Unable to compute ceil values. "
                                      "Column {} is not numeric").format(msg))

        values = c.as_array()
        if dataframeutils.is_numeric_fp(c):
            for i in range(0, self.__next, 1):
                if values[i] is not None:
                    values[i] = float(np.ceil(values[i]))

        return self

    def floor(self, col):
        """Computes the value from the floor function for all numeric values
        in the specified Column.

        The floor function returns the largest integer less than or equal to
        the input. All values in the specified Column are replaced by their
        floor value. If the underlying DataFrame implementation supports null
        values, then None values are excluded from the computation.
        The floor can only be computed for numeric Columns.

        Args:
            col: The index or name of the Column to floor values for.
                Must be an int or str

        Returns:
            This DataFrame instance
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        c = self.__columns[col]
        if not c.is_numeric():
            msg = ("'{}'".format(c._name)
                   if (c._name is not None)
                   else "at index {}".format(col))

            raise DataFrameException(("Unable to compute floor values. "
                                      "Column {} is not numeric").format(msg))

        values = c.as_array()
        if dataframeutils.is_numeric_fp(c):
            for i in range(0, self.__next, 1):
                if values[i] is not None:
                    values[i] = float(np.floor(values[i]))

        return self

    def round(self, col, dec_places):
        """Rounds all values in the specified Column to the specified number
        of decimal places.

        All values in the specified Column are replaced by their rounded value.
        If the underlying DataFrame implementation supports null values, then None
        values are excluded from the computation.
        Rounding can only be conducted for numeric Columns.

        Args:
            col: The index or name of the Column to round values for.
                Must be an int or str
            dec_places: The number of decimal places to round to,
                as a non-negative int

        Returns:
            This DataFrame instance
        """
        if not isinstance(dec_places, int):
            raise DataFrameException(
                ("Invalid argument 'dec_places'. Expected a "
                 "non-negative int but found {}".format(type(dec_places))))

        if dec_places < 0:
            raise DataFrameException(
                ("Invalid argument 'dec_places'. Expected a "
                 "non-negative int but found {}".format(dec_places)))

        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        c = self.__columns[col]
        if not c.is_numeric():
            msg = ("'{}'".format(c._name)
                   if (c._name is not None)
                   else "at index {}".format(col))

            raise DataFrameException(("Unable to round values. "
                                      "Column {} is not numeric").format(msg))

        values = c.as_array()
        if dataframeutils.is_numeric_fp(c):
            for i in range(self.__next):
                if values[i] is not None:
                    values[i] = float(np.around(values[i], decimals=dec_places))

        return self

    def clip(self, col, low=None, high=None):
        """Applies a range threshold to all numeric values in the specified Column.

        This operation ensures that all numeric values in the specified Column are
        within the specified range. If the underlying DataFrame implementation supports
        null values, then None values are excluded from the computation.
        If a particular threshold side is None, then no threshold is applied to all
        numeric values for that side. The lower clip boundary must be smaller than
        the upper boundary.

        Args:
            col: The index or name of the Column to clip numeric values in.
                Must be an int or str
            low: The lower boundary for all numeric values. Must be an int or float.
                May be None
            high: The upper boundary for all numeric values. Must be an int or float.
                May be None

        Returns:
            This DataFrame instance
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        c = self.__columns[col]
        if not c.is_numeric():
            msg = ("'{}'".format(c._name)
                   if (c._name is not None)
                   else "at index {}".format(col))

            raise DataFrameException(("Unable to clip values. "
                                      "Column {} is not numeric").format(msg))

        if low is None and high is None:
            return self #NO-OP

        if low is not None and not isinstance(low, (int, float)):
            raise DataFrameException(
                ("Invalid argument 'low'. Expected "
                 "int or float but found {}".format(type(low))))

        if high is not None and not isinstance(high, (int, float)):
            raise DataFrameException(
                ("Invalid argument 'high'. Expected "
                 "int or float but found {}".format(type(high))))

        if low is not None and high is not None:
            if low >= high:
                raise DataFrameException(
                    "Invalid threshold range: low={} high={}".format(low, high))

        values = c.as_array()
        if dataframeutils.is_numeric_fp(c):
            for i in range(0, self.__next, 1):
                if values[i] is not None:
                    values[i] = float(np.clip(values[i], a_min=low, a_max=high))
        else:
            for i in range(0, self.__next, 1):
                if values[i] is not None:
                    values[i] = int(np.clip(values[i], a_min=low, a_max=high))

        return self

    def sort_by(self, col):
        """Sorts the entire DataFrame according to the values in the
        specified Column.

        The DataFrame is sorted in ascending order.

        Args:
            col: The index or name of the Column to sort the DataFrame by.
                Must be an int or str

        Returns:
            This DataFrame instance
        """
        return self.sort_ascending_by(col)

    def sort_ascending_by(self, col):
        """Sorts the entire DataFrame according to the values in the
        specified Column.

        The DataFrame is sorted in ascending order.

        Args:
            col: The index or name of the Column to sort the DataFrame by.
                Must be an int or str

        Returns:
            This DataFrame instance
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        self._sort_quicksort(col, ascend=True)
        return self

    def sort_descending_by(self, col):
        """Sorts the entire DataFrame according to the values in the
        specified Column.

        The DataFrame is sorted in descending order.

        Args:
            col: The index or name of the Column to sort the DataFrame by.
                Must be an int or str

        Returns:
            This DataFrame instance
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        self._sort_quicksort(col, ascend=False)
        return self

    def head(self, rows=5):
        """Returns the first n rows of this DataFrame.

        The returned DataFrame is not backed by this DataFrame, so changing
        entries in one DataFrame has no effect on the other DataFrame and vice versa.

        Args:
            rows: The number of anterior rows to return. Must be a non-negative int

        Returns:
            A DataFrame containing at most n anterior rows
        """
        if not isinstance(rows, int):
            raise DataFrameException(
                ("Invalid argument 'rows'. Expected "
                 "int but found {}".format(type(rows))))

        if rows < 0:
            raise DataFrameException("Invalid argument 'rows': {}".format(rows))

        if self.__next == -1:
            return NullableDataFrame() if self.__is_nullable else DefaultDataFrame()

        if rows > self.__next:
            rows = self.__next

        cols = [None] * len(self.__columns)
        for i, col in enumerate(self.__columns):
            cols[i] = raven.struct.dataframe.column.Column.of_type(
                col.type_code(),
                rows if rows >= 0 else 0)

        df = NullableDataFrame(cols) if self.__is_nullable else DefaultDataFrame(cols)
        if self.has_column_names():
            df.set_column_names(self.get_column_names())

        for i in range(rows):
            df.set_row(i, self.get_row(i))

        return df

    def tail(self, rows=5):
        """Returns the last n rows of this DataFrame.

        The returned DataFrame is not backed by this DataFrame, so changing
        entries in one DataFrame has no effect on the other DataFrame and vice versa.

        Args:
            rows: The number of posterior rows to return. Must be a non-negative int

        Returns:
            A DataFrame containing at most n posterior rows
        """
        if not isinstance(rows, int):
            raise DataFrameException(
                ("Invalid argument 'rows'. Expected "
                 "int but found {}".format(type(rows))))

        if rows < 0:
            raise DataFrameException("Invalid argument 'rows': {}".format(rows))

        if self.__next == -1:
            return NullableDataFrame() if self.__is_nullable else DefaultDataFrame()

        if rows > self.__next:
            rows = self.__next

        cols = [None] * len(self.__columns)
        for i, col in enumerate(self.__columns):
            cols[i] = raven.struct.dataframe.column.Column.of_type(
                col.type_code(),
                rows if rows >= 0 else 0)

        df = NullableDataFrame(cols) if self.__is_nullable else DefaultDataFrame(cols)
        if self.has_column_names():
            df.set_column_names(self.get_column_names())

        if rows >= 0:
            offset = self.__next - rows
            for i in range(rows):
                df.set_row(i, self.get_row(offset + i))

        return df

    def info(self):
        """Creates an informative string about this DataFrame.

        Returns:
            A string providing information describing this DataFrame
        """
        if self.__columns is None:
            return "uninitialized DataFrame instance"

        s = ""
        s += "Type:    "
        s += "Nullable" if self.is_nullable() else "Default"
        s += "\n"
        s += "Columns: "
        cols = self.columns()
        s += str(cols)
        s += "\n"
        s += "Rows:    "
        s += str(self.rows())
        s += "\n"
        types = DefaultDataFrame(
            stringcolumn.StringColumn("column", cols),
            stringcolumn.StringColumn("type", cols),
            bytecolumn.ByteColumn("code", cols))

        cnames = self.get_column_names()
        if cnames is None:
            cnames = [None] * len(self.__columns)
            for i, _ in enumerate(self.__columns):
                cnames[i] = str(i)

        for i, name in enumerate(cnames):
            types.set_row(i, [name,
                              self.__columns[i].type_name(),
                              self.__columns[i].type_code()])

        s += str(types)
        return s

    def to_array(self):
        """Returns this DataFrame as a list of lists.

        The first dimension contains the Columns of the DataFrame and the
        second dimension contains the entries of each Column (i.e. rows).
        The returned list is not backed by the DataFrame, so changing entries
        in the list has no effect on the DataFrame and vice versa.

        Returns:
            A list of lists representing this DataFrame
        """
        if self.__next == -1:
            return None

        self.flush()
        tc1 = stringcolumn.StringColumn.TYPE_CODE
        tc2 = stringcolumn.NullableStringColumn.TYPE_CODE
        string_code = tc2 if self.__is_nullable else tc1
        # convert char columns to strings
        cols = [col.convert_to(string_code)
                if col.type_name() == "char" else col
                for col in self.__columns]

        return [col.as_array().tolist() for col in cols]

    def to_string(self):
        """Returns a human readable string representation of this DataFrame.

        Returns:
            A string representation of this DataFrame
        """
        if self.__columns is None:
            return "uninitialized DataFrame instance"

        nl = "\n"
        maxl = [None] * len(self.__columns)
        max_idx = len(str(self.__next-1))
        for i in range(len(self.__columns)):
            k = 0
            for j in range(self.__next):
                val = self.__columns[i].get_value(j)
                if isinstance(val, bytearray):
                    srepr = object.__repr__(val)
                    idx = srepr.find("0x")
                    if idx >= 0:
                        srepr = "[B@" + srepr[idx+2:-1]

                    val = srepr

                val = str(val)
                if len(val) > k:
                    k = len(val)

            maxl[i] = k

        nn = [None] * len(self.__columns)
        if self.__names is not None:
            for i in range(len(self.__columns)):
                s = None
                for key, value in self.__names.items():
                    if value == i:
                        s = key
                        break

                if s:
                    nn[i] = s
                else:
                    nn[i] = str(i)

        else:
            for i in range(len(self.__columns)):
                nn[i] = (str(i) + " ")

        for i in range(len(self.__columns)):
            if maxl[i] >= len(nn[i]):
                maxl[i] = maxl[i]
            else:
                maxl[i] = len(nn[i])

        sb = ""
        for i in range(max_idx):
            sb += "_"

        sb += "|"
        for i in range(len(self.__columns)):
            sb += " "
            sb += nn[i]
            for j in range((maxl[i] - len(nn[i])), 0, -1):
                sb += " "

        sb += nl
        for i in range(self.__next):
            sb += str(i)
            for _ in range(max_idx - len(str(i))):
                sb += " "

            sb += "| "
            for j in range(len(self.__columns)):
                val = self.__columns[j].get_value(i)
                if val is not None:
                    if isinstance(val, bytearray):
                        srepr = object.__repr__(val)
                        idx = srepr.find("0x")
                        if idx >= 0:
                            srepr = "[B@" + srepr[idx+2:-1]

                        s = srepr
                    elif isinstance(val, float):
                        if np.isnan(val):
                            s = "NaN"
                        elif np.isposinf(val):
                            s = "Infinity"
                        elif np.isneginf(val):
                            s = "-Infinity"
                        else:
                            s = str(val)
                    else:
                        s = str(val)
                else:
                    s = "null"

                sb += s
                for k in range((maxl[j] - len(s)), -1, -1):
                    sb += " "

            sb += nl

        return sb

    def hash_code(self):
        """Returns a hash code value for this DataFrame.

        This method has to be provided by all DataFrame implementations
        in order to fulfill the general contract of hash_code() and equals().

        Please note that the hash value from the internally used numpy arrays
        is computed by calling the tobytes() method of the underlying array in
        each Column. This creates a temporary copy of the content of the numpy array.

        Returns:
            A hash code value for this DataFrame, as an int
        """
        return hash(self)

    def equals(self, df):
        """Indicates whether this DataFrame's Column structure and content
        is equal to the structure and content of the specified DataFrame.

        The order and types of the underlying Columns matters.

        Args:
            df: The reference DataFrame with which to compare.
                May be any object or None

        Returns:
            True if this DataFrame is equal to the df argument, False otherwise
        """
        if df is None:
            return False

        if not isinstance(df, DataFrame):
            return False

        if self.__is_nullable ^ df.is_nullable():
            return False

        if self.rows() != df.rows() or self.columns() != df.columns():
            return False

        names1 = self.get_column_names()
        names2 = df.get_column_names()
        if (names1 is None) ^ (names2 is None):
            return False

        for i in range(df.columns()):
            if names1 is not None and names2 is not None:
                # compare column names
                if not names1[i] == names2[i]:
                    return False

            # compare column types
            if self.get_column(i).type_code() != df.get_column(i).type_code():
                return False

        # ensure both DataFrames have the same capacity
        self.flush()
        df.flush()
        # compare data
        for i in range(df.columns()):
            col2 = df.get_column(i)
            col1 = self.get_column(i)
            if not col2.equals(col1):
                return False

        return True

    def memory_usage(self):
        """Indicates the current memory usage of this DataFrame in bytes.

        The returned int value refers to the minimum amount of memory needed to
        store the values of all Columns in the underlying arrays.

        Please note that the memory usage is computed for the raw payload data
        of the underlying Columns, comparable to the space needed in an uncompressed
        serialized form. Other data e.g. Column labels, internal representations,
        encodings etc., are not taken into account. The actual memory required by the
        underlying DataFrame instance might be considerably higher than the value
        indicated by this method.

        Returns:
            The current memory usage of this DataFrame in bytes, as an int
        """
        if self.__next == -1:
            return 0

        self.flush()
        size = 0
        for col in self.__columns:
            size += col.memory_usage()

        return size

    def clone(self):
        """Creates and returns a copy of this DataFrame.

        Returns:
            A copy of this DataFrame
        """
        return dataframeutils.copy_of(self)

    def __str__(self):
        return self.to_string()

    def __hash__(self):
        return self._internal_hash_code()

    def __eq__(self, other):
        return self.equals(other)

    def __iter__(self):
        return Iterator(self)

    def __getitem__(self, position):
        return dataframeutils.getitem_impl(self, position)

    def __setitem__(self, position, value):
        dataframeutils.setitem_impl(self, position, value)

    def _enforce_types(self, row):
        """Enforces that all entries in the given row adhere to the
        Column element type in the DataFrame.

        Args:
            row: The row to check against type missmatches. Must be a list

        Raises:
            DataFrameException: If a row item has an invalid type
        """
        if self.__next == -1 or len(row) != len(self.__columns):
            raise DataFrameException(
                ("Row length does not match number of columns: {} (the DataFrame "
                 "has {} columns)").format(len(row), self.columns()))

        for i in range(len(self.__columns)):
            try:
                self.__columns[i]._check_type(row[i])
            except DataFrameException:
                s = ("'{}'".format(self.__columns[i]._name)
                     if (self.__columns[i]._name is not None)
                     else "at index {}".format(i))

                raise DataFrameException(
                    ("Invalid row item type at position {} for "
                     "column {}. Expected {} but found {}")
                    .format(i, s, self.__columns[i].type_name(), type(row[i])))

    def _enforce_name(self, col):
        """Enforces that all requirements are met in order to access a
        Column by its name.

        This method raises an exception in the case of failure or returns
        the index of the Column in the case of success.

        Args:
            col: The name to check. Must be a str

        Returns:
            The index of the Column with the specified name

        Raises:
            DataFrameException: If the specified name is invalid
        """
        if not col:
            raise DataFrameException(
                "Invalid argument 'col'. Argument must not be None or empty")

        if self.__names is None:
            raise DataFrameException("Column names not set")

        try:
            return self.__names[col]
        except KeyError:
            raise DataFrameException("Invalid column name: '{}'".format(col)) from None

    def _get_typed_value(self, col, row, typecode):
        """Gets the value in the specified Column at the specified row
        index as the correctly typed value.

        Args:
            col: The index or name of the Column. Must be an int or str
            row: The row index of the entry to get. Must be an int
            typecode: The unique type code of the underlying Column.
                Must be an int

        Returns:
            The DataFrame entry at the specified Column and row
        """
        if isinstance(col, str):
            col = self._enforce_name(col)

        if row < 0 or row >= self.__next:
            raise DataFrameException("Invalid row index: {}".format(row))

        if self.__columns[col].type_code() != typecode:
            expected = raven.struct.dataframe.column.Column.of_type(typecode)
            msg = ("'{}'".format(self.__columns[col]._name)
                   if (self.__columns[col]._name is not None)
                   else "at index {}".format(col))

            raise DataFrameException(
                ("Cannot get {} value from column {}. Expected {} "
                 "but found {}").format(
                     expected.type_name(),
                     msg,
                     type(expected).__name__,
                     type(self.__columns[col]).__name__))

        return self.__columns[col].get_value(row)

    def _set_typed_value(self, col, row, value, typecode):
        """Sets the specified value in the specified Column at the
        specified row index.

        Args:
            col: The index or name of the Column. Must be an int or str
            row: The row index of the entry to set. Must be an int
            value: The value to set
            typecode: The unique type code of the underlying Column.
                Must be an int
        """
        if not self.__is_nullable and value is None:
            raise DataFrameException("DefaultDataFrame cannot use None values")

        if isinstance(col, str):
            col = self._enforce_name(col)

        if row < 0 or row >= self.__next:
            raise DataFrameException("Invalid row index: {}".format(row))

        if self.__columns[col].type_code() != typecode:
            expected = raven.struct.dataframe.column.Column.of_type(typecode)
            msg = ("'{}'".format(self.__columns[col]._name)
                   if (self.__columns[col]._name is not None)
                   else "at index {}".format(col))

            raise DataFrameException(
                ("Cannot set {} value in column {}. Expected {} "
                 "but found {}").format(
                     expected.type_name(),
                     msg,
                     type(expected).__name__,
                     type(self.__columns[col]).__name__))

        self.__columns[col][row] = value

    def _resize(self):
        """Resizes all Columns sequentially."""
        for col in self.__columns:
            col._resize()

    def _flush_all(self, buffer):
        """Sequentially performs a flush operation on all Columns.

        A buffer can be set to keep some extra space between the current
        entries and the Column capacity.

        Args:
            buffer: A buffer applied to each Column. Using 0 (zero)
                will apply no buffer at all and will shrink each Column
                to its minimum required length
        """
        for col in self.__columns:
            col._match_length(self.__next+buffer)

    def _internal_hash_code(self):
        """Internally used hash method."""
        h = 0
        mod = 2**64
        names = self.get_column_names()
        if names is not None:
            for i, col in enumerate(self.__columns):
                h = (h + hash(names[i])) % mod
                h = (h + col.type_code()) % mod

        if self.__columns is not None:
            for i, col in enumerate(self.__columns):
                h = (h + self.__columns[i].hash_code()) % mod

        return h

    def _replace_by_match(self, col, regex, replacement):
        """Replaces all values in the specified Column that match the
        specified regular expression.

        All matched values are replaced with the value returned by the specified
        replacement function. If the underlying DataFrame implementation doesn't
        support null values, then the value returned by the specified replacement
        function must not be None.

        Args:
            col: The index or name of the Column to replace values in.
                Must be an in or str
        regex: The regular expression that all Column values to be replaced
            must match. Must be a str. May be None or empty
        replacement: The replacement function to determine the new value for
            each matched position

        Returns:
            The number of values that were replaced by this operation, as an int
        """
        # wrapper function if the replacement arg
        # is a constant value
        def wrap_fn(replacement_obj):
            return lambda i, v: replacement_obj

        if isinstance(col, str):
            col = self._enforce_name(col)

        if regex is not None and not isinstance(regex, str):
            raise DataFrameException(
                ("Invalid argument 'regex'. Expected "
                 "str but found {}".format(type(regex))))

        if self.__next == -1 or col < 0 or col >= len(self.__columns):
            raise DataFrameException("Invalid column index: {}".format(col))

        if replacement is None:
            return 0 #NO-OP

        if not hasattr(replacement, "__call__"): # is not a function
            replacement = wrap_fn(replacement)

        if not regex:
            regex = ".*" # match everything

        if regex == "null":
            regex = "None"

        if regex == "NaN":
            regex = "nan"

        column = self.__columns[col]
        pattern = regex_matcher.compile(regex)
        replaced = 0
        argcount = len(inspect.getfullargspec(replacement)[0])
        for i in range(self.__next):
            current_value = column.get_value(i)
            if not pattern.fullmatch(str(current_value)):
                continue

            replacement_value = None
            try:
                if argcount == 1:
                    replacement_value = replacement(current_value)
                elif argcount == 2:
                    replacement_value = replacement(i, current_value)
                else:
                    raise DataFrameException(
                        ("Replacement function has an "
                         "invalid number of input arguments. "
                         "Expected 1 or 2 but found {}").format(argcount))

            except (ValueError, TypeError) as ex:
                raise DataFrameException(
                    ("Value replacement function "
                     "has raised {}".format(type(ex)))) from ex

            if replacement_value == current_value:
                continue

            try:
                column[i] = replacement_value
            except DataFrameException as ex:
                msg1 = ("for column '{}'".format(column._name)
                        if column._name
                        else "at column index {}".format(col))

                msg2 = (ex.message[18:]
                        if (ex.message is not None
                            and ex.message.startswith("Invalid argument.")
                            and len(ex.message) > 20)
                        else ex.message)

                raise DataFrameException(
                    ("Invalid replacement type {}. {}").format(
                        msg1, msg2)) from ex

            replaced += 1

        return replaced

    def _minimum_ranked(self, col, rank):
        """Computes the n-minimum entries in the specified Column and returns
        the corresponding rows as a DataFrame.

        The rank specifies the maximum number of rows to return (the number n).
        The returned DataFrame is ordered ascendingly according to the values
        in the specified Column, i.e. the minimum is located at row 0, the
        second minimum at row 1, etc.

        If the underlying DataFrame implementation supports null values, then None
        values are excluded from the computation. The minimum can only be computed
        for numeric columns.

        Args:
            col: The index of the Column to compute the n-minima for
            rank: The maximum number of rows to return

        Returns:
            A DataFrame containing at most n rows, ordered ascendingly by the
            Column with the specified index
        """
        if rank <= 0:
            raise DataFrameException("Invalid argument 'rank': {}".format(rank))

        if rank > self.__next:
            rank = self.__next

        cols = [None] * len(self.__columns)
        for i, c in enumerate(self.__columns):
            cols[i] = raven.struct.dataframe.column.Column.of_type(c.type_code(), rank)

        result = (NullableDataFrame(cols)
                  if self.__is_nullable
                  else DefaultDataFrame(cols))

        if self.has_column_names():
            result.set_column_names(self.get_column_names())

        indices = [-1] * rank
        column = self.__columns[col]
        for i in range(rank):
            first = True
            min_value = None
            for j in range(self.__next):
                value = column.get_value(j)
                if value is not None and (first or value < min_value):
                    taken = False
                    for k in range(rank):
                        if indices[k] == j:
                            taken = True
                            break

                    if not taken:
                        first = False
                        min_value = value
                        indices[i] = j

        removed_offset = 0
        for i in range(rank):
            if indices[i] != -1:
                result.set_row(i, self.get_row(indices[i]))
            else:
                result.remove_row(i - removed_offset)
                removed_offset += 1

        result.flush()
        return result

    def _maximum_ranked(self, col, rank):
        """Computes the n-maximum entries in the specified Column and returns
        the corresponding rows as a DataFrame.

        The rank specifies the maximum number of rows to return (the number n).
        The returned DataFrame is ordered descendingly according to the values
        in the specified Column, i.e. the maximum is located at row 0, the
        second maximum at row 1, etc.

        If the underlying DataFrame implementation supports null values, then None
        values are excluded from the computation. The maximum can only be computed
        for numeric columns.

        Args:
            col: The index of the Column to compute the n-maxima for
            rank: The maximum number of rows to return

        Returns:
            A DataFrame containing at most n rows, ordered descendingly by the
            Column with the specified index
        """
        if rank <= 0:
            raise DataFrameException("Invalid argument 'rank': {}".format(rank))

        if rank > self.__next:
            rank = self.__next

        cols = [None] * len(self.__columns)
        for i, c in enumerate(self.__columns):
            cols[i] = raven.struct.dataframe.column.Column.of_type(c.type_code(), rank)

        result = (NullableDataFrame(cols)
                  if self.__is_nullable
                  else DefaultDataFrame(cols))

        if self.has_column_names():
            result.set_column_names(self.get_column_names())

        indices = [-1] * rank
        column = self.__columns[col]
        for i in range(rank):
            first = True
            max_value = None
            for j in range(self.__next):
                value = column.get_value(j)
                if value is not None and (first or value > max_value):
                    taken = False
                    for k in range(rank):
                        if indices[k] == j:
                            taken = True
                            break

                    if not taken:
                        first = False
                        max_value = value
                        indices[i] = j

        removed_offset = 0
        for i in range(rank):
            if indices[i] != -1:
                result.set_row(i, self.get_row(indices[i]))
            else:
                result.remove_row(i - removed_offset)
                removed_offset += 1

        result.flush()
        return result

    def _replace_by_datafarame(self, df):
        """Replaces all Columns in this DataFrame with matched Columns
        from the specified DataFrame.

        If both DataFrame instances have labeled Columns, then matching is
        performed via Column names. If both DataFrame instances are not labeled,
        then all Columns are set from lower indices to higher indices, i.e. left
        to right, from the specified DataFrame.

        Please note that DataFrames must be both either labeled or unlabeled.
        Both DataFrames must have the same number of rows.

        Args:
            df: The DataFrame instance holding all Columns that should replace the
                corresponding Columns in this instance. It must have the same number
                of rows as this DataFrame. Passing None as a replacement DataFrame will
                result in no change being applied

        Returns:
            The number of Column instances that were replaced by this operation
        """
        if df is None:
            return 0 #NO-OP

        if not self.__is_nullable and df.is_nullable():
            raise DataFrameException(
                "DefaultDataFrame cannot use NullableColumn instance")

        if df.rows() != self.__next:
            raise DataFrameException(
                ("Row count differs. Expected {} rows but found {}")
                .format(self.__next, df.rows()))

        if self.has_column_names() ^ df.has_column_names():
            raise DataFrameException(
                ("Cannot replace columns. DataFrames must be both "
                 "either labeled or unlabeled"))

        self.flush()
        df.flush()
        replaced = 0
        if self.has_column_names():
            for i in range(df.columns()):
                col = df.get_column(i)
                name = col.get_name()
                if name and self.has_column(name):
                    self.set_column(name, col.as_nullable()
                                    if self.__is_nullable
                                    else col)

                    replaced += 1

        else:
            for i in range(df.columns()):
                col = df.get_column(i)
                if replaced < self.columns():
                    self.set_column(replaced, col.as_nullable()
                                    if self.__is_nullable
                                    else col)

                    replaced += 1

        return replaced

    def _remove_rows_by_match(self, col, regex):
        """Removes all rows that match the specified regular expression in
        the Column at the specified index.

        Args:
            col: The index of the Column that the specified regex
                is matched against
            regex: The regular expression that row entries in the specified
                Column must match

        Returns:
            The number of removed rows, as an int
        """
        if regex == "null":
            regex = "None"

        if regex == "NaN":
            regex = "nan"

        column = self.__columns[col]
        pattern = regex_matcher.compile(regex)
        i = 0
        k = -1
        removed = 0
        while i < self.__next:
            if pattern.fullmatch(str(column[i])):
                if k == -1:
                    k = i
                i += 1
            else:
                if k != -1:
                    self.remove_rows(from_index=k, to_index=i)
                    rem_range = (i - k)
                    removed += rem_range
                    i -= rem_range
                    k = -1
                else:
                    i += 1

        if k != -1:
            self.remove_rows(from_index=k, to_index=i)
            removed += (i - k)

        return removed

    def _remove_rows_by_range(self, from_index, to_index):
        """Removes all rows from (inclusive) the specified index
        to (exclusive) the specified index.

        Args:
            from_index: The index from which all rows should be removed (inclusive).
                Must be an int
            to_index: The index to which all rows should be removed (exclusive).
                Must be an int

        Returns:
            This DataFrame instance
        """
        for column in self.__columns:
            column._remove(from_index, to_index, self.__next)

        self.__next -= (to_index - from_index)
        if (self.__next * 3) < self.__columns[0].capacity():
            self._flush_all(4)

        return self

    def _ensure_valid_column_set_operation(self, df):
        """Ensures that conditions are met for set-theoretic operations with Columns

        Args:
            df: The DataFrame argument to check

        Raises:
            DataFrameException: If the necessary conditions are not met
        """
        if self.__next == -1:
            raise DataFrameException("Uninitialized DataFrame instance")

        if df is None:
            raise DataFrameException("DataFrame argument must not be None")

        if self.rows() != df.rows():
            raise DataFrameException(
                ("Invalid number of rows for argument DataFrame. "
                 "Expected {} but found {}".format(self.rows(), df.rows())))

        if not self.has_column_names() or not df.has_column_names():
            raise DataFrameException("Both DataFrame instances must have labeled columns")

        if self.capacity() != self.rows():
            self.flush()

        if df.capacity() != df.rows():
            df.flush()

    def _ensure_valid_row_set_operation(self, df):
        """Ensures that conditions are met for set-theoretic operations with rows

        Args:
            df: The DataFrame argument to check

        Raises:
            DataFrameException: If the necessary conditions are not met
        """
        if self.__next == -1:
            raise DataFrameException("Uninitialized DataFrame instance")

        if df is None:
            raise DataFrameException("DataFrame argument must not be None")

        if self.columns() != df.columns():
            raise DataFrameException(
                ("Invalid number of columns for argument DataFrame. "
                 "Expected {} but found {}".format(
                     self.columns(), df.columns())))

        if self.has_column_names() ^ df.has_column_names():
            raise DataFrameException(
                ("Both DataFrame instances must have either labeled "
                 "columns or unlabeled columns"))

    def _internal_next(self):
        """Internal method providing access to the next counter.

        Returns:
            The value of the internally used next index pointer, as an int
        """
        return self.__next

    def _internal_columns(self):
        """Internal method providing access to the list of columns.

        Changes to the content of the returned list are
        reflected by this DataFrame and vice versa.

        Returns:
            A reference to the internally used list of Column objects, as a list
        """
        return self.__columns

    def _presort_nulls(self, unsorted, next_pos):
        ptr = next_pos - 1
        i = 0
        while i < ptr:
            while unsorted[i] is None:
                if i == ptr:
                    break

                self._swap(i, ptr)
                ptr -= 1

            i += 1

        return ptr - 1 if unsorted[ptr] is None else ptr

    def _presort_floats(self, unsorted, right):
        if right <= -1:
            return right

        ptr = right
        i = 0
        while i < ptr:
            while np.isnan(unsorted[i]):
                if i == ptr:
                    break

                self._swap(i, ptr)
                ptr -= 1

            i += 1

        return ptr - 1 if np.isnan(unsorted[ptr]) else ptr

    def _sort_quicksort(self, col, ascend):
        col = self.__columns[col]
        left = 0
        right = self.__next - 1
        if self.is_nullable(): # NullableDataFrame
            right = self._presort_nulls(col.as_array(), self.__next)
            if col.type_code() == binarycolumn.NullableBinaryColumn.TYPE_CODE:
                self._sort_quicksort_binary_impl(col.as_array(), left, right, ascend)
            else:
                self._sort_quicksort_impl0(col, left, right, ascend)
        else: # DefaultDataFrame
            if col.type_code() == binarycolumn.BinaryColumn.TYPE_CODE:
                self._sort_quicksort_binary_impl(col.as_array(), left, right, ascend)
            else:
                self._sort_quicksort_impl0(col, left, right, ascend)

    def _sort_quicksort_impl0(self, col, left, right, ascend):
        if self.is_nullable(): # NullableDataFrame
            if col.type_code() in (floatcolumn.NullableFloatColumn.TYPE_CODE,
                                   doublecolumn.NullableDoubleColumn.TYPE_CODE):

                right = self._presort_floats(col.as_array(), right)
        else: # DefaultDataFrame
            if col.type_code() in (floatcolumn.FloatColumn.TYPE_CODE,
                                   doublecolumn.DoubleColumn.TYPE_CODE):

                right = self._presort_floats(col.as_array(), right)

        self._sort_quicksort_impl1(col.as_array(), left, right, ascend)

    def _sort_quicksort_impl1(self, unsorted, left, right, ascend):
        if right <= -1:
            return

        lr_range = left + right
        mid = unsorted[int(lr_range/2)]
        l = left
        r = right
        while l < r:
            if ascend:
                while unsorted[l] < mid:
                    l += 1
                while unsorted[r] > mid:
                    r -= 1
            else:
                while unsorted[l] > mid:
                    l += 1
                while unsorted[r] < mid:
                    r -= 1

            if l <= r:
                self._swap(l, r)
                l += 1
                r -= 1

        if left < r:
            self._sort_quicksort_impl1(unsorted, left, r, ascend)

        if right > l:
            self._sort_quicksort_impl1(unsorted, l, right, ascend)

    def _sort_quicksort_binary_impl(self, unsorted, left, right, ascend):
        if right <= -1:
            return

        lr_range = left + right
        mid = unsorted[int(lr_range/2)]
        l = left
        r = right
        while l < r:
            if ascend:
                while len(unsorted[l]) < len(mid):
                    l += 1
                while len(unsorted[r]) > len(mid):
                    r -= 1
            else:
                while len(unsorted[l]) > len(mid):
                    l += 1
                while len(unsorted[r]) < len(mid):
                    r -= 1

            if l <= r:
                self._swap(l, r)
                l += 1
                r -= 1

        if left < r:
            self._sort_quicksort_binary_impl(unsorted, left, r, ascend)

        if right > l:
            self._sort_quicksort_binary_impl(unsorted, l, right, ascend)

    def _swap(self, i, j):
        for col in self.__columns:
            array = col.as_array()
            cache = array[i]
            array[i] = array[j]
            array[j] = cache

    @staticmethod
    def Default(*columns):
        """Constructs a DefaultDataFrame.

        Constructs a new DefaultDataFrame with the specified columns.
        If a Column was labeled during its construction, that Column will be
        referenceable by that name. All Columns which have not been labeled during
        their construction will have no name assigned to them.
        The order of the Columns within the constructed DataFrame is defined
        by the order of the arguments passed to this constructor. All Columns
        must have the same size.

        This implementation cannot use Column instances which permit null values.

        Args:
            columns: The Column instances to be used by the
                constructed DefaultDataFrame instance
        """
        return DefaultDataFrame(*columns)

    @staticmethod
    def Nullable(*columns):
        """Constructs a NullableDataFrame.

        Constructs a new NullableDataFrame with the specified columns.
        If a Column was labeled during its construction, that Column will be
        referenceable by that name. All Columns which have not been labeled
        during their construction will have no name assigned to them.
        The order of the Columns within the constructed DataFrame is defined
        by the order of the arguments passed to this constructor. All Columns
        must have the same size.

        This implementation must use Column instances which permit null values.
        If a given Column is not nullable, then this constructor will convert
        that Column before it is added to the constructed
        NullableDataFrame instance.

        Args:
            columns: The Column instances to be used by the
                constructed NullableDataFrame instance
        """
        return NullableDataFrame(*columns)

    @staticmethod
    def ByteColumn(name=None, values=None):
        """Constructs a new ByteColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the ByteColumn as a string
            values: The content of the ByteColumn.
                Must be a list or numpy array with dtype int8, or an int
        """
        return bytecolumn.ByteColumn(name, values)

    @staticmethod
    def ShortColumn(name=None, values=None):
        """Constructs a new ShortColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the ShortColumn as a string
            values: The content of the ShortColumn.
                Must be a list or numpy array with dtype int16, or an int
        """
        return shortcolumn.ShortColumn(name, values)

    @staticmethod
    def IntColumn(name=None, values=None):
        """Constructs a new IntColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the IntColumn as a string
            values: The content of the IntColumn.
                Must be a list or numpy array with dtype int32, or an int
        """
        return intcolumn.IntColumn(name, values)

    @staticmethod
    def LongColumn(name=None, values=None):
        """Constructs a new LongColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the LongColumn as a string
            values: The content of the LongColumn.
                Must be a list or numpy array with dtype int64, or an int
        """
        return longcolumn.LongColumn(name, values)

    @staticmethod
    def StringColumn(name=None, values=None):
        """Constructs a new StringColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the StringColumn as a string
            values: The content of the StringColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        return stringcolumn.StringColumn(name, values)

    @staticmethod
    def FloatColumn(name=None, values=None):
        """Constructs a new FloatColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the FloatColumn as a string
            values: The content of the FloatColumn.
                Must be a list or numpy array with dtype float32, or an int
        """
        return floatcolumn.FloatColumn(name, values)

    @staticmethod
    def DoubleColumn(name=None, values=None):
        """Constructs a new DoubleColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the DoubleColumn as a string
            values: The content of the DoubleColumn.
                Must be a list or numpy array with dtype float64, or an int
        """
        return doublecolumn.DoubleColumn(name, values)

    @staticmethod
    def CharColumn(name=None, values=None):
        """Constructs a new CharColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the CharColumn as a string
            values: The content of the CharColumn.
                Must be a list or numpy array with dtype uint8, or an int
        """
        return charcolumn.CharColumn(name, values)

    @staticmethod
    def BooleanColumn(name=None, values=None):
        """Constructs a new BooleanColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the BooleanColumn as a string
            values: The content of the BooleanColumn.
                Must be a list or numpy array with dtype bool, or an int
        """
        return booleancolumn.BooleanColumn(name, values)

    @staticmethod
    def BinaryColumn(name=None, values=None):
        """Constructs a new BinaryColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the BinaryColumn as a string
            values: The content of the BinaryColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        return binarycolumn.BinaryColumn(name, values)

    @staticmethod
    def NullableByteColumn(name=None, values=None):
        """Constructs a new NullableByteColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the NullableByteColumn as a string
            values: The content of the NullableByteColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        return bytecolumn.NullableByteColumn(name, values)

    @staticmethod
    def NullableShortColumn(name=None, values=None):
        """Constructs a new NullableShortColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the NullableShortColumn as a string
            values: The content of the NullableShortColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        return shortcolumn.NullableShortColumn(name, values)

    @staticmethod
    def NullableIntColumn(name=None, values=None):
        """Constructs a new NullableIntColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the NullableIntColumn as a string
            values: The content of the NullableIntColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        return intcolumn.NullableIntColumn(name, values)

    @staticmethod
    def NullableLongColumn(name=None, values=None):
        """Constructs a new NullableLongColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the NullableLongColumn as a string
            values: The content of the NullableLongColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        return longcolumn.NullableLongColumn(name, values)

    @staticmethod
    def NullableStringColumn(name=None, values=None):
        """Constructs a new NullableStringColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the NullableStringColumn as a string
            values: The content of the NullableStringColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        return stringcolumn.NullableStringColumn(name, values)

    @staticmethod
    def NullableFloatColumn(name=None, values=None):
        """Constructs a new NullableFloatColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the NullableFloatColumn as a string
            values: The content of the NullableFloatColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        return floatcolumn.NullableFloatColumn(name, values)

    @staticmethod
    def NullableDoubleColumn(name=None, values=None):
        """Constructs a new NullableDoubleColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the NullableDoubleColumn as a string
            values: The content of the NullableDoubleColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        return doublecolumn.NullableDoubleColumn(name, values)

    @staticmethod
    def NullableCharColumn(name=None, values=None):
        """Constructs a new NullableCharColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the NullableCharColumn as a string
            values: The content of the NullableCharColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        return charcolumn.NullableCharColumn(name, values)

    @staticmethod
    def NullableBooleanColumn(name=None, values=None):
        """Constructs a new NullableBooleanColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the NullableBooleanColumn as a string
            values: The content of the NullableBooleanColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        return booleancolumn.NullableBooleanColumn(name, values)

    @staticmethod
    def NullableBinaryColumn(name=None, values=None):
        """Constructs a new NullableBinaryColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the NullableBinaryColumn as a string
            values: The content of the NullableBinaryColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        return binarycolumn.NullableBinaryColumn(name, values)

    @staticmethod
    def copy(df):
        """Creates and returns a copy of the specified DataFrame.

        Args:
            df: The DataFrame instance to copy

        Returns:
            A copy of the specified DataFrame or None if the argument is None
        """
        return dataframeutils.copy_of(df)

    @staticmethod
    def like(df):
        """Creates and returns a DataFrame which has the same Column structure
        and Column names as the specified DataFrame instance but is otherwise empty.

        Args:
            df: The DataFrame from which to copy the Column structure

        Returns:
            A DataFrame with the same Column structure and names as the specified
            DataFrame, or None if the specified DataFrame is None
        """
        return dataframeutils.like(df)

    @staticmethod
    def merge(*dataframes):
        """Merges all given DataFrame instances into one DataFrame.

        All DataFames are merged by Columns. All DataFrames must have an
        equal number of rows but may be of any type. All Columns are added to
        the returned DataFrame in the order of the arguments passed to this
        method. Only passing one DataFrame to this method will simply
        return that instance.

        Columns with duplicate names are included in the returned DataFrame
        and a postfix is added to each duplicate column name.
        All Columns of the returned DataFrame are backed by their origin,
        which means that changes to the original DataFrame are reflected in
        the merged DataFrame and vice versa. This does not apply, however,
        if Columns need to be converted to a nullable type. For example, if
        one DataFrame argument is nullable, then all Columns from non-nullable
        DataFrame arguments are converted to their corresponding
        nullable equivalent.

        If Columns should be independent from their origin, then simply pass
        a clone (copy) of each DataFrame argument to this method.

        Example:
            merged = DataFrame.merge(DataFrame.copy(df1), DataFrame.copy(df2))

        Args:
            dataframes: The DataFrames to be merged

        Returns:
            A DataFrame composed of all Columns of the given DataFrames
        """
        return dataframeutils.merge(*dataframes)

    @staticmethod
    def convert_to(df, target_type):
        """Converts the given DataFrame from a DefaultDataFrame to a NullableDataFrame
        or vice versa.

        Converting a DefaultDataFrame to a NullableDataFrame will not change
        any internal values, except that now you can add/insert null values to it.
        Converting a NullableDataFrame to a DefaultDataFrame will convert all None
        occurrences to the primitive defaults according to the Column they are located.

        Example:
            (if 'mydf' is a DefaultDataFrame)
            DataFrame df = DataFrame.convert(mydf, "nullable")

        Args:
            df: The DataFrame instance to convert. Must not be None
            target_type: The type to convert the given DataFrame to.
                May be 'default' or 'nullable'

        Returns:
            A DataFrame converted from the type of the argument passed to this method
            to the type specified
        """
        return dataframeutils.convert(df, target_type)

    @staticmethod
    def serialize(df, compress=False):
        """Serializes the specified DataFrame to a bytearray.

        The compression of the returned bytearray is controlled by
        the additional boolean flag of this method.

        Args:
            df: The DataFrame to serialize. Must not be None
            compress: A boolean flag indicating whether to compress the serialized bytes.
                Must be a bool

        Returns:
            A bytearray representing the given DataFrame in a serialized form

        Raises:
            DataFrameException: If any errors occur during serialization or compression
        """
        return raven.io.dataframe.dataframes.serialize(df, compress=compress)

    @staticmethod
    def deserialize(bytes_data):
        """Deserializes the specified bytearray to a DataFrame.

        If the given bytearray is compressed, it will be automatically
        decompressed before the deserialization is executed.

        Args:
            bytes_data: The bytearray representing the DataFrame to deserialize.
                Must be a bytearray. Must not be None

        Returns:
            A DataFrame from the given bytearray

        Raises:
            DataFrameException: If any errors occur during deserialization or
                decompression, or if the given bytearray does not
                constitute a DataFrame
        """
        return raven.io.dataframe.dataframes.deserialize(bytes_data)

    @staticmethod
    def read(filepath):
        """Reads the specified DataFrame file.

        If the specified file path denotes a single DataFrame file, then that DataFrame is
        read and returned as a single DataFrame instance. If the specified file path denotes
        a directory, then all DataFrame files in that directory are read, i.e. all files
        ending with a '.df' fil extension, and a dict is returned mapping all encountered
        file names (without the '.df' extension) to the corresponding DataFrame instance read.

        Args:
            filepath: The DataFrame file(s) to read. Must be a str representing
                the path to a single file to read or a path to a directory containing
                one or more DataFrame files to read. Must not be None

        Returns:
            A DataFrame from the specified file, or a dict mapping all found files in
            the specified directory to the corresponding DataFrame

        Raises:
            FileNotFoundError: If the specified file cannot be found or if the
                directory does not contain any DataFrame files
            PermissionError: If the permission for reading the
                specified file was denied
            DataFrameException: If any errors occur during deserialization
                or the file format is invalid
        """
        return raven.io.dataframe.dataframes.read_file(filepath)

    @staticmethod
    def write(filepath, df):
        """Persists the given DataFrame to the specified file.

        If the specified file path denotes a single file, then the 'df' argument must be
        a single DataFrame instance. If the specified file path denotes a directory, then
        the 'df' argument must be a dict containing the mapping of str file names to
        DataFrame instances to persist.

        Args:
            filepath: The file or directory to write the DataFrame(s) to. Must be a str
                representing the path to the file to write or the path to the directory
                in which to write the DataFrames to. Must not be None
            df: The DataFrame(s) to persist. Must be either a single DataFrame instance
                or a dict mapping file names to DataFrame instances. Must not be None

        Raises:
            PermissionError: If the permission for writing the
                specified file was denied
            DataFrameException: If any errors occur during file persistence
                or if any errors occur during serialization
        """
        raven.io.dataframe.dataframes.write_file(filepath, df)

    @staticmethod
    def to_base64(df):
        """Serializes the given DataFrame to a Base64 encoded string.

        Args:
            df: The DataFrame to serialize to a Base64 encoded string.
                Must not be None

        Returns:
            A Base64 encoded string representing the given DataFrame

        Raises:
            DataFrameException: If any errors occur during serialization
        """
        return raven.io.dataframe.dataframes.to_base64(df)

    @staticmethod
    def from_base64(string):
        """Deserializes the given Base64 encoded string to a DataFrame.

        Args:
            string: The Base64 encoded string representing the DataFrame to deserialize.
                Must not be None

        Returns:
            A DataFrame from the given Base64 string

        Raises:
            DataFrameException: If any errors occur during deserialization
        """
        return raven.io.dataframe.dataframes.from_base64(string)

    @staticmethod
    def read_csv(filepath, separator=",", header=True, encoding="utf-8", types=None):
        """Reads the CSV-file denoted by the specified file path and returns a DataFrame
        representing its content.

        The columns in the specified CSV-file must be separated by the
        specified separator character. Any character except double quotes can be used
        as a separator. If the 'header' argument is True, then the first line of
        the CSV-file will be treated as a header line denoting the column names.

        By default, all Column elements in the returned DataFrame are of type string.
        Therefore, all Columns are of type StringColumn or NullableStringColumn
        respectively. Each Column type can be specified individually by passing the
        type names directly to the 'types' argument as a tuple of strings. The order
        of the types within the tuple argument will specify to which Column that
        type is assigned to.

        Supported type names are:

            "byte", "short", "int", "long", "float", "double", "string", "char", "boolean"

        For example:

          >>> from raven.struct.dataframe import DataFrame
          >>> df = DataFrame.read_csv("myfile.csv", types=("string", int", "float", "boolean"))

        The above code will read a CSV-file named 'myfile.csv' and return a DataFrame
        with the first Column as a StringColumn, the second Column as an IntColumn,
        the third Column as a FloatColumn and the fourth Column as a BooleanColumn.

        If the CSV-file has a header, then the 'header' argument must be True.

        Args:
            filepath: The CSV-file to read. Must be a str representing
                the path to the file to read
            separator: The separator used in the specified file to read.
                Must be a str of length 1
            header: A boolean flag indicating whether to treat the first line
                as a header. Must be a bool
            encoding: The text encoding used in the specified file.
                Must be a str
            types: The type of each Column within the specified file. All types
                are specified by their corresponding type name.
                Must be a tuple of str

        Returns:
            A DataFrame representing the content of the specified CSV-file

        Raises:
            ValueError: If an argument is invalid
            PermissionError: If the permission for reading the specified
                file was denied
            IOError: If any errors occur during reading
        """
        return raven.io.dataframe.csvfiles.read(filepath, separator, header, encoding, types)

    @staticmethod
    def write_csv(filepath, df, separator=",", header=True, encoding="utf-8"):
        """Writes the content of the specified DataFrame to the file denoted
        by the specified file path.

        The file is written in a CSV-format. The entries of each Column are
        separated by the specified separator. This function will write a header
        to the CSV-file if the corresponding DataFrame has any Column names set.
        This behaviour can be controlled with the 'header' argument.

        The columns in the specified CSV-file are separated by the specified
        separator character. Any character except double quotes can be used
        as a separator.

        Args:
            filepath: The file to write. May be a path to a file.
                Must be a str. Must not be None
            df: The DataFrame to write to the specified file. Must not be None
            separator: The separator character to be used.
                Must be a str of length 1
            header: A boolean flag indicating whether to write the Column names
                to the first line of the CSV-file as a header. Must be a bool
            encoding: The text encoding to be used for the specified file.
                Must be a str

        Returns:
            The number of bytes written to the specified CSV-file

        Raises:
            PermissionError: If the permission for writing the
                specified file was denied
            IOError: If any errors occur during writing
        """
        return raven.io.dataframe.csvfiles.write(filepath, df, separator, header, encoding)


class DefaultDataFrame(DataFrame):
    """A default DataFrame implementation.

    A DefaultDataFrame does not allow the use of null values.

    This implementation is NOT thread-safe.
    """

    def __init__(self, *columns):
        """Constructs a new DefaultDataFrame with the specified columns.

        If a Column was labeled during its construction, that Column will be
        referenceable by that name. All Columns which have not been labeled during
        their construction will have no name assigned to them.
        The order of the Columns within the constructed DataFrame is defined
        by the order of the arguments passed to this constructor. All Columns
        must have the same size.

        This implementation DOES NOT permit null values.

        Args:
            columns: The Column instances to be used by the
                constructed DefaultDataFrame instance
        """
        if len(columns) > 0:
            if isinstance(columns[0], (list, tuple)):
                columns = columns[0]

        columns = list(columns)
        super(DefaultDataFrame, self).__init__(is_nullable=False, columns=columns)


class NullableDataFrame(DataFrame):
    """A DataFrame implementation allowing the use of null values.

    This implementation is NOT thread-safe.
    """

    def __init__(self, *columns):
        """Constructs a new NullableDataFrame with the specified columns.

        If a Column was labeled during its construction, that Column will be
        referenceable by that name. All Columns which have not been labeled
        during their construction will have no name assigned to them.
        The order of the Columns within the constructed DataFrame is defined
        by the order of the arguments passed to this constructor. All Columns
        must have the same size.

        This implementation must use Column instances which permit null values.
        If a given Column is not nullable, then this constructor will convert
        that Column before it is added to the constructed
        NullableDataFrame instance.

        Args:
            columns: The Column instances to be used by the
                constructed NullableDataFrame instance
        """
        if len(columns) > 0:
            if isinstance(columns[0], (list, tuple)):
                columns = columns[0]

        columns = list(columns)
        super(NullableDataFrame, self).__init__(is_nullable=True, columns=columns)

class Iterator:
    """An iterator over a DataFrame."""

    # pylint: disable=invalid-name
    def __init__(self, df):
        self.df = df
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < (self.df.columns()):
            col = self.df.get_column(self.current)
            self.current += 1
            return col
        else:
            raise StopIteration

class DataFrameException(Exception):
    """Exception raised at runtime to indicate an
    illegal or failed operation regarding DataFrames.

    Attributes:
        message: A message describing the error which
            caused the exception to be raised
    """

    def __init__(self, message=None):
        """Constructs a new DataFrameException with
        the specified error message.

        Args:
            message: The exception message
        """
        super().__init__()
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        else:
            return ""
