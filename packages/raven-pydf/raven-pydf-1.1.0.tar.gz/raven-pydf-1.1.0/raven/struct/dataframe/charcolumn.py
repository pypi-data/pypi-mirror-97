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
"""
Provides an implementation for CharColumn and NullableCharColumn
"""

import numpy as np

import raven.struct.dataframe.core as dataframe
import raven.struct.dataframe.column as column
import raven.struct.dataframe.bytecolumn as bytecolumn
import raven.struct.dataframe.shortcolumn as shortcolumn
import raven.struct.dataframe.intcolumn as intcolumn
import raven.struct.dataframe.longcolumn as longcolumn
import raven.struct.dataframe.floatcolumn as floatcolumn
import raven.struct.dataframe.doublecolumn as doublecolumn
import raven.struct.dataframe.stringcolumn as stringcolumn
import raven.struct.dataframe.booleancolumn as booleancolumn
import raven.struct.dataframe.binarycolumn as binarycolumn

class CharColumn(column.Column):
    """A Column holding single ASCII-character values.
    This implementation DOES NOT support null values.

    The internal array of CharColumn instances is implemented as an
    array of uint8 values. From a user perspective, char values are
    represented as str objects of length one. The internal conversion
    between str and uint8 takes place with the ord() function and the
    inverse (i.e. from uint8 to str) with the char() function.
    Users of this class should be aware of this when performing direct
    array access as no type checks are enforced by the class in such case.

    Only printable ASCII-character values in the range [32,126]
    (as uint8 decimal values) are allowed as elements of CharColumns.
    """

    TYPE_CODE = 8
    DEFAULT_VALUE = "?"

    def __init__(self, name=None, values=None):
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
        if values is None:
            values = np.empty(0, dtype=np.uint8)

        if isinstance(values, list):
            charvals = self._create_array(len(values))
            for i, value in enumerate(values):
                self._check_type(value)
                charvals[i] = ord(value)

            values = charvals

        elif isinstance(values, np.ndarray):
            if values.dtype != "uint8":
                raise dataframe.DataFrameException(
                    ("Invalid argument array. Expected "
                     "char array (uint8) but found {}".format(values.dtype)))

            for i, value in enumerate(values):
                if (value < 32) or (value > 126):
                    raise dataframe.DataFrameException(
                        ("Invalid character value for CharColumn at index {}. "
                         "Only printable ASCII is permitted").format(i))

        elif isinstance(values, int):
            values = np.zeros(values, dtype=np.uint8)
            default_val = ord(CharColumn.DEFAULT_VALUE)
            for i in range(values.shape[0]):
                values[i] = default_val
        else:
            raise dataframe.DataFrameException(
                ("Invalid argument array. Expected "
                 "list or numpy array but found {}".format(type(values))))

        super().__init__(name, values)

    def _check_type(self, value):
        if value is None:
            raise dataframe.DataFrameException(
                ("Invalid argument. "
                 "CharColumn cannot use None values"))

        if isinstance(value, str):
            if len(value) != 1:
                raise dataframe.DataFrameException(
                    ("Invalid character value. Expected string of "
                     "length 1 but found length {}".format(len(value))))

            byte = ord(value)
            if (byte < 32) or (byte > 126):
                raise dataframe.DataFrameException(
                    ("Invalid character value for CharColumn. "
                     "Only printable ASCII is permitted"))

        else:
            raise dataframe.DataFrameException(
                ("Invalid argument. Expected "
                 "char (str) but found {}".format(type(value))))

    def get_value(self, index):
        """Gets the char value at the specified index

        Args:
            index: The index of the value to get

        Returns:
            The char value at the specified index. Is never None

        Raises:
            ValueError: If the specified index is out of bounds
        """
        self._check_bounds(index)
        return chr(self._values[index])

    def set_value(self, index, value):
        """Sets the char value at the specified index

        Args:
            index: The index of the char value to set
            value: The char value to set at the specified position.
                Must be a string

        Raises:
            ValueError: If the specified index is out of bounds or of the
                object provided is of the wrong type
        """
        self._check_bounds(index)
        self._check_type(value)
        self._values[index] = ord(value)

    def type_code(self):
        return CharColumn.TYPE_CODE

    def type_name(self):
        return "char"

    def is_nullable(self):
        return False

    def is_numeric(self):
        return False

    def _insert_value_at(self, index, next_pos, value):
        for i in range(next_pos, index, -1):
            self._values[i] = self._values[i-1]

        self._values[index] = ord(value)

    def get_default_value(self):
        return CharColumn.DEFAULT_VALUE

    def __getitem__(self, index):
        return chr(self._values[index])

    def __setitem__(self, index, value):
        self._check_type(value)
        self._values[index] = ord(value)

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=invalid-name
    def convert_to(self, typecode):
        converted = None
        if typecode == bytecolumn.ByteColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.int8)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x))

            converted = bytecolumn.ByteColumn(values=vals)
        elif typecode == shortcolumn.ShortColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.int16)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x))

            converted = shortcolumn.ShortColumn(values=vals)
        elif typecode == intcolumn.IntColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.int32)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x))

            converted = intcolumn.IntColumn(values=vals)
        elif typecode == longcolumn.LongColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.int64)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x))

            converted = longcolumn.LongColumn(values=vals)
        elif typecode == stringcolumn.StringColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = chr(x)

            converted = stringcolumn.StringColumn(values=vals)
        elif typecode == floatcolumn.FloatColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.float32)
            for i, x in np.ndenumerate(self._values):
                vals[i] = float(chr(x))

            converted = floatcolumn.FloatColumn(values=vals)
        elif typecode == doublecolumn.DoubleColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.float64)
            for i, x in np.ndenumerate(self._values):
                vals[i] = float(chr(x))

            converted = doublecolumn.DoubleColumn(values=vals)
        elif typecode == CharColumn.TYPE_CODE:
            converted = self.clone()
        elif typecode == booleancolumn.BooleanColumn.TYPE_CODE:
            values_true = {"t", "1", "y"}
            values_false = {"f", "0", "n"}
            vals = np.empty([self._values.shape[0]], dtype=np.bool)
            for i, x in np.ndenumerate(self._values):
                x = chr(x).lower()
                is_true = x in values_true
                is_false = x in values_false
                if not is_true and not is_false:
                    raise dataframe.DataFrameException(
                        ("Invalid boolean character: '{}'".format(self._values[i])))

                vals[i] = is_true

            converted = booleancolumn.BooleanColumn(values=vals)
        elif typecode == binarycolumn.BinaryColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = bytearray(chr(x).encode("utf-8"))

            converted = binarycolumn.BinaryColumn(values=vals)
        elif typecode == bytecolumn.NullableByteColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x))

            converted = bytecolumn.NullableByteColumn(values=vals)
        elif typecode == shortcolumn.NullableShortColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x))

            converted = shortcolumn.NullableShortColumn(values=vals)
        elif typecode == intcolumn.NullableIntColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x))

            converted = intcolumn.NullableIntColumn(values=vals)
        elif typecode == longcolumn.NullableLongColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x))

            converted = longcolumn.NullableLongColumn(values=vals)
        elif typecode == stringcolumn.NullableStringColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(vals):
                vals[i] = chr(x)

            converted = stringcolumn.NullableStringColumn(values=vals)
        elif typecode == floatcolumn.NullableFloatColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = float(chr(x))

            converted = floatcolumn.NullableFloatColumn(values=vals)
        elif typecode == doublecolumn.NullableDoubleColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = float(chr(x))

            converted = doublecolumn.NullableDoubleColumn(values=vals)
        elif typecode == NullableCharColumn.TYPE_CODE:
            converted = NullableCharColumn(values=self._values.astype(np.object))
        elif typecode == booleancolumn.NullableBooleanColumn.TYPE_CODE:
            values_true = {"t", "1", "y"}
            values_false = {"f", "0", "n"}
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                x = chr(x).lower()
                is_true = x in values_true
                is_false = x in values_false
                if not is_true and not is_false:
                    raise dataframe.DataFrameException(
                        ("Invalid boolean character: '{}'".format(self._values[i])))

                vals[i] = is_true

            converted = booleancolumn.NullableBooleanColumn(values=vals)
        elif typecode == binarycolumn.NullableBinaryColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = bytearray(chr(x).encode("utf-8"))

            converted = binarycolumn.NullableBinaryColumn(values=vals)
        else:
            raise dataframe.DataFrameException(
                "Unknown column type code: {}".format(typecode))

        # pylint: disable=protected-access
        converted._name = self._name
        return converted

    def _create_array(self, size=0):
        return np.zeros(size, dtype=np.uint8) + ord(self.get_default_value())

class NullableCharColumn(column.Column):
    """A Column holding nullable single ASCII-character values.
    Any values not explicitly set are considered None.

    The internal array of NullableCharColumn instances is implemented as an
    array of nullable uint8 values. From a user perspective, char values are
    represented as str objects of length one. The internal conversion
    between str and uint8 takes place with the ord() function and the
    inverse (i.e. from uint8 to str) with the char() function.
    Users of this class should be aware of this when performing direct
    array access as no type checks are enforced by the class in such case.

    Only printable ASCII-character values in the range [32,126]
    (when viewed as uint8 decimal values) are allowed to be
    used in NullableCharColumns.
    """

    TYPE_CODE = 17

    # pylint: disable=too-many-branches
    def __init__(self, name=None, values=None):
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
        if values is None:
            values = np.empty(0, dtype=np.object)

        if isinstance(values, list):
            charvals = np.zeros(len(values), dtype=np.object)
            for i, value in enumerate(values):
                self._check_type(value)
                if value is None:
                    charvals[i] = None
                else:
                    charvals[i] = ord(value)

            values = charvals

        elif isinstance(values, np.ndarray):
            if values.dtype != "object":
                raise dataframe.DataFrameException(
                    ("Invalid argument array. Expected "
                     "char array (object) but found {}".format(values.dtype)))

            for i, value in enumerate(values):
                if value is not None:
                    if isinstance(value, str):
                        if len(value) != 1:
                            raise dataframe.DataFrameException(
                                ("Invalid character value in numpy array argument. "
                                 "Expected string of length 1 but found "
                                 "length {}".format(len(value))))

                        byte = ord(value)
                        if (byte < 32) or (byte > 126):
                            raise dataframe.DataFrameException(
                                ("Invalid character value for NullableCharColumn at index {}. "
                                 "Only printable ASCII is permitted").format(i))

                        values[i] = byte

                    elif isinstance(value, int):
                        if (value < 32) or (value > 126):
                            raise dataframe.DataFrameException(
                                ("Invalid character value for NullableCharColumn at index {}. "
                                 "Only printable ASCII is permitted").format(i))

                    else:
                        raise dataframe.DataFrameException(
                            ("Invalid argument. Expected "
                             "char (str) but found {}".format(type(value))))

        elif isinstance(values, int):
            values = np.empty(values, dtype=np.object)
        else:
            raise dataframe.DataFrameException(
                ("Invalid argument array. Expected "
                 "list or numpy array but found {}".format(type(values))))

        super().__init__(name, values)

    def _check_type(self, value):
        if value is not None:
            if isinstance(value, str):
                if len(value) != 1:
                    raise dataframe.DataFrameException(
                        ("Invalid character value. Expected string of "
                         "length 1 but found length {}".format(len(value))))

                byte = ord(value)
                if (byte < 32) or (byte > 126):
                    raise dataframe.DataFrameException(
                        ("Invalid character value for NullableCharColumn. "
                         "Only printable ASCII is permitted"))

            else:
                raise dataframe.DataFrameException(
                    ("Invalid argument. Expected "
                     "char (str) but found {}".format(type(value))))

    def get_value(self, index):
        """Gets the char value at the specified index

        Args:
            index: The index of the value to get

        Returns:
            The char value at the specified index. May be None

        Raises:
            ValueError: If the specified index is out of bounds
        """
        self._check_bounds(index)
        val = self._values[index]
        if val is None:
            return None
        else:
            return chr(val)

    def set_value(self, index, value):
        """Sets the char value at the specified index

        Args:
            index: The index of the char value to set
            value: The char value to set at the specified position.
                Must be a string or None

        Raises:
            ValueError: If the specified index is out of bounds or of the
                object provided is of the wrong type
        """
        self._check_bounds(index)
        self._check_type(value)
        if value is None:
            self._values[index] = None
        else:
            self._values[index] = ord(value)

    def type_code(self):
        return NullableCharColumn.TYPE_CODE

    def type_name(self):
        return "char"

    def is_nullable(self):
        return True

    def is_numeric(self):
        return False

    def _insert_value_at(self, index, next_pos, value):
        for i in range(next_pos, index, -1):
            self._values[i] = self._values[i-1]

        if value is None:
            self._values[index] = None
        else:
            self._values[index] = ord(value)

    def get_default_value(self):
        return None

    def __getitem__(self, index):
        val = self._values[index]
        if val is None:
            return None
        else:
            return chr(val)

    def __setitem__(self, index, value):
        self._check_type(value)
        if value is None:
            self._values[index] = None
        else:
            self._values[index] = ord(value)

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=invalid-name
    def convert_to(self, typecode):
        converted = None
        if typecode == bytecolumn.ByteColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.int8)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x)) if x is not None else 0

            converted = bytecolumn.ByteColumn(values=vals)
        elif typecode == shortcolumn.ShortColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.int16)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x)) if x is not None else 0

            converted = shortcolumn.ShortColumn(values=vals)
        elif typecode == intcolumn.IntColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.int32)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x)) if x is not None else 0

            converted = intcolumn.IntColumn(values=vals)
        elif typecode == longcolumn.LongColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.int64)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x)) if x is not None else 0

            converted = longcolumn.LongColumn(values=vals)
        elif typecode == stringcolumn.StringColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = chr(x) if x is not None else stringcolumn.StringColumn.DEFAULT_VALUE

            converted = stringcolumn.StringColumn(values=vals)
        elif typecode == floatcolumn.FloatColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.float32)
            for i, x in np.ndenumerate(self._values):
                vals[i] = float(chr(x)) if x is not None else 0.0

            converted = floatcolumn.FloatColumn(values=vals)
        elif typecode == doublecolumn.DoubleColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.float64)
            for i, x in np.ndenumerate(self._values):
                vals[i] = float(chr(x)) if x is not None else 0.0

            converted = doublecolumn.DoubleColumn(values=vals)
        elif typecode == CharColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.float64)
            for i, x in np.ndenumerate(self._values):
                vals[i] = float(chr(x)) if x is not None else CharColumn.DEFAULT_VALUE

            converted = doublecolumn.DoubleColumn(values=vals)
        elif typecode == booleancolumn.BooleanColumn.TYPE_CODE:
            values_true = {"t", "1", "y"}
            values_false = {"f", "0", "n"}
            vals = np.empty([self._values.shape[0]], dtype=np.bool)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    x = chr(x).lower()
                    is_true = x in values_true
                    is_false = x in values_false
                    if not is_true and not is_false:
                        raise dataframe.DataFrameException(
                            ("Invalid boolean character: '{}'".format(self._values[i])))

                    vals[i] = is_true
                else:
                    vals[i] = False

            converted = booleancolumn.BooleanColumn(values=vals)
        elif typecode == binarycolumn.BinaryColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = bytearray(chr(x).encode("utf-8"))
                else:
                    vals[i] = bytearray.fromhex("00")

            converted = binarycolumn.BinaryColumn(values=vals)
        elif typecode == bytecolumn.NullableByteColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x)) if x is not None else None

            converted = bytecolumn.NullableByteColumn(values=vals)
        elif typecode == shortcolumn.NullableShortColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x)) if x is not None else None

            converted = shortcolumn.NullableShortColumn(values=vals)
        elif typecode == intcolumn.NullableIntColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x)) if x is not None else None

            converted = intcolumn.NullableIntColumn(values=vals)
        elif typecode == longcolumn.NullableLongColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(chr(x)) if x is not None else None

            converted = longcolumn.NullableLongColumn(values=vals)
        elif typecode == stringcolumn.NullableStringColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = chr(x) if x is not None else None

            converted = stringcolumn.NullableStringColumn(values=vals)
        elif typecode == floatcolumn.NullableFloatColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = float(chr(x)) if x is not None else None

            converted = floatcolumn.NullableFloatColumn(values=vals)
        elif typecode == doublecolumn.NullableDoubleColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = float(chr(x)) if x is not None else None

            converted = doublecolumn.NullableDoubleColumn(values=vals)
        elif typecode == NullableCharColumn.TYPE_CODE:
            converted = self.clone()
        elif typecode == booleancolumn.NullableBooleanColumn.TYPE_CODE:
            values_true = {"t", "1", "y"}
            values_false = {"f", "0", "n"}
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    x = chr(x).lower()
                    is_true = x in values_true
                    is_false = x in values_false
                    if not is_true and not is_false:
                        raise dataframe.DataFrameException(
                            ("Invalid boolean character: '{}'".format(self._values[i])))

                    vals[i] = is_true
                else:
                    vals[i] = None

            converted = booleancolumn.NullableBooleanColumn(values=vals)
        elif typecode == binarycolumn.NullableBinaryColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = bytearray(chr(x).encode("utf-8"))
                else:
                    vals[i] = None

            converted = binarycolumn.NullableBinaryColumn(values=vals)
        else:
            raise dataframe.DataFrameException(
                "Unknown column type code: {}".format(typecode))

        # pylint: disable=protected-access
        converted._name = self._name
        return converted

    def _create_array(self, size=0):
        return np.empty(size, dtype=np.object)
