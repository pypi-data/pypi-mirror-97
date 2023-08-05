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
"""Provides the abstract base class for all column implementations."""

from abc import ABC, ABCMeta, abstractmethod

import numpy as np

import raven.struct.dataframe.core as dataframe

__author__ = "Phil Gaiser"

# pylint: disable=C0103, R1705, R0911, R0912, R0912

class Column(ABC):
    """A labeled Column to be used in a DataFrame.

    Each Column is a container for data of a specific type. Although it can be
    constructed and initialized independently, a Column is always managed by a
    DataFrame instance.

    A concrete Column can only use data of one specific type.
    This abstract class defines methods all Columns to be used in DataFrames
    must implement. Additonal methods may be provided by concrete
    implementations.

    Concrete Columns can be differentiated either by their underlying class
    or by their unique type code. The type code is exposed as a public
    constant by each implementing class. Additionally, the type_code() member
    method, which must be implemented by all concrete Columns, gives
    dynamic access to the type code of a Column instance at runtime. For a
    more human readable indication, the type_name() method returns a
    string denoting the type of the elements which can be stored by the
    corresponding Column. The type name is the same for default and
    nullable columns which work with the same element type while the type
    code is always unique across all Column classes.

    Generally, there are two main groups of columns. Those that accept null
    values and those that do not. Regardless of this differentiation, all
    concrete Columns must extend this abstract base class. The term 'null'
    or 'null value' is equivalent to the term 'None' and 'NoneType' and
    may be used interchangeably.

    Each Column can have a distinct label associated with it. That label
    represents the name of that Column by which it can be referenced and
    accessed when it is being used inside a DataFrame.

    Even though users can get and set values inside Columns directly through
    the get_value() and set_value() methods defined by the Column class,
    it is generally recommended to always perform operations regarding Columns
    by using the appropriate methods of the DataFrame that the Column is
    part of. With the exception of Column construction, generally, working
    with Column instances directly is regarded as more lower-level compared to
    using the public DataFrame API to manipulate Columns. As a consequence,
    concrete Column implementations can raise exceptions other
    than DataFrameException, for example ValueError when an invalid
    argument is passed to a method of a Column.

    Columns do not distinguish between their size and their capacity.
    The row count size is always managed by a DataFrame and any required
    resizing is also explicitly precipitated by it. Therefore, the value
    returned by the capacity() method always indicates the true length of
    the array used internally to store the Column values. However, this may
    include any buffered space allocated by a DataFrame in order make its
    operations more efficient. This has to be taken into account when a
    user works with data in Columns directly.

    This class provides various static methods to construct concrete
    Column instances.

    Every Column is cloneable by means of the clone() method.
    """

    __metaclass__ = ABCMeta

    def __init__(self, name=None, values=None):
        """Assigns this Column instance the specified name and values.

        This constructor should be called by all subclasses.

        Args:
            name: The name to assign to this Column. Must be a string
            values: The values to assign to this Column. Must be a numpy array
        """
        if name is not None and not isinstance(name, str):
            raise dataframe.DataFrameException(
                ("Invalid argument 'name'. "
                 "Expected str but found {}").format(type(name)))

        if not isinstance(values, np.ndarray):
            raise dataframe.DataFrameException(
                ("Invalid argument 'values'. "
                 "Expected numpy.ndarray but found {}").format(type(values)))

        self._name = name
        self._values = values

    @abstractmethod
    def type_code(self):
        """Returns the unique type code of this column

        Returns:
            The type code of this Column
        """
        raise NotImplementedError

    @abstractmethod
    def type_name(self):
        """Returns the standardized name of the element types of this column

        Returns:
            The type name of this Column
        """
        raise NotImplementedError

    @abstractmethod
    def is_nullable(self):
        """Indicates whether this column accepts null values.

        In Python, the term 'null' and 'null value' is equivalent to 'None'
        and 'None type' respectively, with regard to the DataFrame API

        Returns:
            True if this Column can work with null values, False if
            using null values with this Column will result in exceptions
            at runtime
        """
        raise NotImplementedError

    @abstractmethod
    def is_numeric(self):
        """Indicates whether this column contains numeric values

        Returns:
            True if this column uses numeric values, False otherwise
        """
        raise NotImplementedError

    @abstractmethod
    def get_default_value(self):
        """Gets the default value for this Column.

        For nullable columns, default values are always null

        Returns:
            The default value for this Column
        """
        raise NotImplementedError

    @abstractmethod
    def convert_to(self, typecode):
        """Converts this Column to a Column instance of the specified type code.

        The elements of this column are not changed by this operation.
        The returned Column holds a copy of all elements converted to
        the type of the column with the specified type code.

        Please note that any existing buffered space will be included in
        the converted Column.

        Args:
            typecode: The type code of the Column to convert this column to

        Returns:
            A Column instance with the specified type code which holds all
            entries of this Column converted to the corresponding element type
        """
        raise NotImplementedError

    @abstractmethod
    def _check_type(self, value):
        """Validates whether the specified value can be used by this Column.

        This method should raise a DataFrameException if the specified value
        cannot be used by this Column, i.e. if explicitly setting the
        value would result in an error at runtime

        Raises:
            DataFrameException: If the specified value cannot
                be used by this Column
        """
        raise NotImplementedError

    @abstractmethod
    def _create_array(self, size):
        """Creates an internal array of the specified size, initialized
        with default values of the corresponding type.

        The array is of the type that the underlying Column
        implementation supports.

        Args:
            size: The size of the internal array to create
        """
        raise NotImplementedError

    def get_value(self, index):
        """Gets the value at the specified index

        Args:
            index: The index of the value to get

        Returns:
            The value at the specified index

        Raises:
            ValueError: If the specified index is out of bounds
        """
        self._check_bounds(index)
        return self._values[index]

    def set_value(self, index, value):
        """Sets the value at the specified index

        Args:
            index: The index of the value to set
            value: The value to set at the specified position

        Raises:
            DataFrameException: If the specified index is out of bounds or
                if the object provided is of the wrong type
        """
        self._check_bounds(index)
        self._check_type(value)
        self._values[index] = value

    def get_name(self):
        """Gets the label of this Column.

        The name is the label by which this Column instance can
        be referenced when using DataFrame API calls.

        Returns:
            The name of this Column, as a str
        """
        return self._name

    def capacity(self):
        """Returns the current capacity of this Column, i.e. the length
        of its internal array.

        Returns:
            The capacity of this Column
        """
        return self._values.size if self._values is not None else 0

    def as_array(self):
        """Returns a reference to the internal numpy array of
        this Column instance.

        Returns:
            The numpy array which is used by this Column to store its elements
        """
        return self._values

    def as_default(self):
        """Returns this Column as a default (non-nullable) Column.

        If this Column supports null values, then a converted version
        is returned. If this Column is already non-nullable, then this
        instance is returned. The element type of this Column is not changed
        by this operation

        Returns:
            A Column guaranteed to be non-nullable
        """
        if self.is_nullable():
            if self.type_code() <= 18:
                return self.convert_to(self.type_code() - 9)
            else:# is binary column
                return self.convert_to(self.type_code() - 1)
        else:
            return self

    def as_nullable(self):
        """Returns this Column as a nullable Column.

        If this Column does not support null values, then a converted
        version is returned. If this Column already supports nullable values,
        then this instance is returned. The element type of this Column is
        not changed by this operation

        Returns:
            A Column guaranteed to support null values
        """
        if not self.is_nullable():
            if self.type_code() <= 18:
                return self.convert_to(self.type_code() + 9)
            else:# is binary column
                return self.convert_to(self.type_code() + 1)
        else:
            return self

    def clone(self):
        """Creates and returns a copy of this Column

        Returns:
            A copy of this Column
        """
        copy = Column.of_type(self.type_code())
        # pylint: disable=protected-access
        copy._name = self._name
        copy._values = np.copy(self._values)
        return copy

    def memory_usage(self):
        """Indicates the current memory usage of this Column in bytes.

        The returned value refers to the minimum amount of memory needed to
        store all values plus allocated buffered space in the underlying
        array of this column.

        Please note that the memory usage is computed for the raw payload data
        of the underlying column, comparable to the space needed in an
        uncompressed serialized form. Other data e.g. column labels, internal
        representations, encodings etc., are not taken into account. The
        actual memory required by the underlying Column instance might
        be considerably higher

        Returns:
            An int denoting the current memory usage of this Column in bytes
        """
        return self._values.nbytes

    def equals(self, col):
        """Indicates whether this Column is equal to the specified Column.

        Please note that the capacity of both columns may be taken into
        account when computing the equality.

        Args:
            col: The reference Column with which to compare

        Returns:
            True if this Column is equal to the specified Column argument,
            False otherwise
        """
        if self is col:
            return True

        if not isinstance(col, Column):
            return False

        if self.type_code() != col.type_code():
            return False

        if (self._name is None) ^ (col._name is None):
            return False

        if self._name is not None and col._name is not None:
            if not self._name == col._name:
                return False

        if self._values.shape[0] != col._values.shape[0]:
            return False

        # check the array dtype. Raw numerical arrays are
        # handled by numpy code directly. We have to compare
        # nullable columns (dtype='object') manually because
        # numpy can't handle NaNs in such a case
        if self._values.dtype.name == "object":
            for i in range(self._values.shape[0]):
                # cache values
                x1 = self._values[i]
                x2 = col._values[i]
                # pylint: disable=C0123
                # compare element types
                if type(x1) != type(x2):
                    return False

                # check whether elements are floats or doubles
                if isinstance(x1, float):
                    x1_isnan = np.isnan(x1)
                    x2_isnan = np.isnan(x2)
                    # check whether only one of two elements is NaN
                    if x1_isnan ^ x2_isnan:
                        return False

                    # both elements being NaN are considered equal.
                    # Check normal numbers for equality
                    if not x1_isnan and x1 != x2:
                        return False

                # default case. We just check for equality
                else:
                    if x1 != x2:
                        return False

            return True
        else:
            # call numpy function for better performance
            return np.array_equal(self._values, col._values, equal_nan=True)

    def hash_code(self):
        """Computes and returns a hash code value for this Column.

        The capacity of the column may be taken into account
        when computing the hash code.

        Please note that the hash value from the internally
        used numpy array is computed by calling the tobytes() method
        of the underlying array. This creates a temporary copy of the
        content of the numpy array.

        Returns:
            An int representing the hash code value for this Column
        """
        return hash(self)

    def __hash__(self):
        return hash((self._name, self._values.tobytes()))

    def __eq__(self, other):
        return self.equals(other)

    def __getitem__(self, index):
        return self._values[index]

    def __setitem__(self, index, value):
        self._check_type(value)
        self._values[index] = value

    @staticmethod
    def like(col, length=0):
        """Creates a new Column instance which has the same type and name as
        the specified Column and the specified length. The returned Column will
        be initialized with default values.

        Args:
            col: The Column to structurally copy
            length: The length of the Column to return. Must be an int

        Returns:
            A Column with the type and name of the specified Column and
            the specified length, or None if the specified Column is None
        """
        # pylint: disable=protected-access
        if col is None:
            return None

        column = Column.of_type(col.type_code(), length)
        column._name = col._name
        return column

    # pylint: disable=import-outside-toplevel
    @staticmethod
    def of_type(type_code, length=0):
        """Creates a new Column instance with the specified type code.

        This function can be used to construct an empty column which has the
        same type as another column but is not a copy of that column's content
        and has the specified length. The returned Column will be initialized
        with default values if the length argument is positive.

        Args:
            type_code: The unique type code of the Column to create
            length: The initial length of the Column to create. Must be an int
        Returns:
            An empty Column of the specified type and length or None if
            the specified type code is unknown
        """
        if not isinstance(length, int):
            raise ValueError("Invalid length argument. Must be an int")

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

        if type_code == bytecolumn.ByteColumn.TYPE_CODE:
            return bytecolumn.ByteColumn(values=length)
        if type_code == shortcolumn.ShortColumn.TYPE_CODE:
            return shortcolumn.ShortColumn(values=length)
        if type_code == intcolumn.IntColumn.TYPE_CODE:
            return intcolumn.IntColumn(values=length)
        if type_code == longcolumn.LongColumn.TYPE_CODE:
            return longcolumn.LongColumn(values=length)
        if type_code == stringcolumn.StringColumn.TYPE_CODE:
            return stringcolumn.StringColumn(values=length)
        if type_code == floatcolumn.FloatColumn.TYPE_CODE:
            return floatcolumn.FloatColumn(values=length)
        if type_code == doublecolumn.DoubleColumn.TYPE_CODE:
            return doublecolumn.DoubleColumn(values=length)
        if type_code == charcolumn.CharColumn.TYPE_CODE:
            return charcolumn.CharColumn(values=length)
        if type_code == booleancolumn.BooleanColumn.TYPE_CODE:
            return booleancolumn.BooleanColumn(values=length)
        if type_code == binarycolumn.BinaryColumn.TYPE_CODE:
            return binarycolumn.BinaryColumn(values=length)
        if type_code == bytecolumn.NullableByteColumn.TYPE_CODE:
            return bytecolumn.NullableByteColumn(values=length)
        if type_code == shortcolumn.NullableShortColumn.TYPE_CODE:
            return shortcolumn.NullableShortColumn(values=length)
        if type_code == intcolumn.NullableIntColumn.TYPE_CODE:
            return intcolumn.NullableIntColumn(values=length)
        if type_code == longcolumn.NullableLongColumn.TYPE_CODE:
            return longcolumn.NullableLongColumn(values=length)
        if type_code == stringcolumn.NullableStringColumn.TYPE_CODE:
            return stringcolumn.NullableStringColumn(values=length)
        if type_code == floatcolumn.NullableFloatColumn.TYPE_CODE:
            return floatcolumn.NullableFloatColumn(values=length)
        if type_code == doublecolumn.NullableDoubleColumn.TYPE_CODE:
            return doublecolumn.NullableDoubleColumn(values=length)
        if type_code == charcolumn.NullableCharColumn.TYPE_CODE:
            return charcolumn.NullableCharColumn(values=length)
        if type_code == booleancolumn.NullableBooleanColumn.TYPE_CODE:
            return booleancolumn.NullableBooleanColumn(values=length)
        if type_code == binarycolumn.NullableBinaryColumn.TYPE_CODE:
            return binarycolumn.NullableBinaryColumn(values=length)

        # Default value for unknown type code
        return None

    def _check_bounds(self, index):
        """Checks array bounds for the specified index.

        This method raises a DataFrameException if the specified
        index is out of bounds.
        """
        if index < 0 or index >= self._values.shape[0]:
            raise dataframe.DataFrameException("Invalid row index: {}".format(index))

    def _insert_value_at(self, index, next_pos, value):
        """Inserts the specified value at the given index into the column.

        Shifts all entries currently at that position and any
        subsequent entries down (adds one to their indices)

        Args:
            index: The index to insert the value at
            next_pos: The index of the next free position
            value: The value to insert
        """
        for i in range(next_pos, index, -1):
            self._values[i] = self._values[i-1]

        self._values[index] = value

    def _remove(self, i_from, i_to, next_pos):
        """Removes all entries from the first index given, to the second index.

        Shifts all entries currently next to the last position removed and any
        subsequent entries up.

        Args:
            i_from: The index from which to start removing (inclusive)
            i_to: The index to which to remove to (exclusive)
            next_pos: The index of the next free position
        """
        i = i_from
        for _ in range(next_pos - i_to):
            self._values[i] = self._values[(i_to - i_from) + i]
            i += 1

        i = next_pos - 1
        for _ in range(i_to - i_from):
            self[i] = self.get_default_value()
            i -= 1

    def _resize(self):
        """Resizes the internal array holding the column entries.

        The used resizing strategy doubles the array capacity
        """
        new_entries = None
        valsize = self._values.shape[0]
        if valsize > 0:
            new_entries = self._create_array(valsize * 2)
        else:
            new_entries = self._create_array(2)

        for i in range(valsize):
            new_entries[i] = self._values[i]

        self._values = new_entries

    def _match_length(self, length):
        """Resizes the internal array to match the given length

        Args:
            length: The length to resize the column to
        """
        valsize = self._values.shape[0]
        if length != valsize:
            tmp = self._create_array(length)
            for i in range(length):
                if i < valsize:
                    tmp[i] = self._values[i]
                else:
                    break

            self._values = tmp
