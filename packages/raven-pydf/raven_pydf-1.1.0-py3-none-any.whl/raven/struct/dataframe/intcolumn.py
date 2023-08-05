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
Provides an implementation for IntColumn and NullableIntColumn
"""

import numpy as np

import raven.struct.dataframe.core as dataframe
import raven.struct.dataframe.column as column
import raven.struct.dataframe.bytecolumn as bytecolumn
import raven.struct.dataframe.shortcolumn as shortcolumn
import raven.struct.dataframe.longcolumn as longcolumn
import raven.struct.dataframe.floatcolumn as floatcolumn
import raven.struct.dataframe.doublecolumn as doublecolumn
import raven.struct.dataframe.stringcolumn as stringcolumn
import raven.struct.dataframe.charcolumn as charcolumn
import raven.struct.dataframe.booleancolumn as booleancolumn
import raven.struct.dataframe.binarycolumn as binarycolumn

class IntColumn(column.Column):
    """A Column holding int values (int32).
    This implementation DOES NOT support null values.
    """

    TYPE_CODE = 3

    def __init__(self, name=None, values=None):
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
        if values is None:
            values = np.empty(0, dtype=np.int32)

        if isinstance(values, list):
            for value in values:
                self._check_type(value)

            values = np.array(values, dtype=np.int32)

        elif isinstance(values, np.ndarray):
            if values.dtype != "int32":
                raise dataframe.DataFrameException(
                    ("Invalid argument array. Expected "
                     "int array (int32) but found {}".format(values.dtype)))

        elif isinstance(values, int):
            values = np.zeros(values, dtype=np.int32)
        else:
            raise dataframe.DataFrameException(
                ("Invalid argument array. Expected "
                 "list or numpy array but found {}".format(type(values))))

        super().__init__(name, values)

    def _check_type(self, value):
        if value is None:
            raise dataframe.DataFrameException(
                ("Invalid argument. "
                 "IntColumn cannot use None values"))

        if isinstance(value, int):
            if (value < -2147483648) or (value > 2147483647):
                raise dataframe.DataFrameException(
                    "Out of range int (int32): {}".format(value))

        elif not isinstance(value, np.int32):
            raise dataframe.DataFrameException(
                ("Invalid argument. Expected "
                 "int (int32) but found {}".format(type(value))))

    def get_value(self, index):
        """Gets the int value at the specified index

        Args:
            index: The index of the value to get

        Returns:
            The int value at the specified index. Is never None

        Raises:
            ValueError: If the specified index is out of bounds
        """
        self._check_bounds(index)
        return int(self._values[index])

    def type_code(self):
        return IntColumn.TYPE_CODE

    def type_name(self):
        return "int"

    def is_nullable(self):
        return False

    def is_numeric(self):
        return True

    def get_default_value(self):
        return 0

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=invalid-name
    def convert_to(self, typecode):
        converted = None
        if typecode == bytecolumn.ByteColumn.TYPE_CODE:
            converted = bytecolumn.ByteColumn(values=self._values.astype(np.int8))
        elif typecode == shortcolumn.ShortColumn.TYPE_CODE:
            converted = shortcolumn.ShortColumn(values=self._values.astype(np.int16))
        elif typecode == IntColumn.TYPE_CODE:
            converted = self.clone()
        elif typecode == longcolumn.LongColumn.TYPE_CODE:
            converted = longcolumn.LongColumn(values=self._values.astype(np.int64))
        elif typecode == stringcolumn.StringColumn.TYPE_CODE:
            vals = self._values.astype(np.object)
            for i, x in np.ndenumerate(vals):
                vals[i] = str(x)

            converted = stringcolumn.StringColumn(values=vals)
        elif typecode == floatcolumn.FloatColumn.TYPE_CODE:
            converted = floatcolumn.FloatColumn(values=self._values.astype(np.float32))
        elif typecode == doublecolumn.DoubleColumn.TYPE_CODE:
            converted = doublecolumn.DoubleColumn(values=self._values.astype(np.float64))
        elif typecode == charcolumn.CharColumn.TYPE_CODE:
            vals = self._values.astype(np.uint8)
            for i, x in np.ndenumerate(vals):
                vals[i] = ord(str(x)[0])

            converted = charcolumn.CharColumn(values=vals)
        elif typecode == booleancolumn.BooleanColumn.TYPE_CODE:
            converted = booleancolumn.BooleanColumn(values=self._values.astype(np.bool))
        elif typecode == binarycolumn.BinaryColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = bytearray(int(x).to_bytes(4, byteorder="big", signed=True))

            converted = binarycolumn.BinaryColumn(values=vals)
        elif typecode == bytecolumn.NullableByteColumn.TYPE_CODE:
            vals = self._values.astype(np.int8)
            converted = bytecolumn.NullableByteColumn(values=vals.astype(np.object))
        elif typecode == shortcolumn.NullableShortColumn.TYPE_CODE:
            vals = self._values.astype(np.int16)
            converted = shortcolumn.NullableShortColumn(values=vals.astype(np.object))
        elif typecode == NullableIntColumn.TYPE_CODE:
            converted = NullableIntColumn(values=self._values.astype(np.object))
        elif typecode == longcolumn.NullableLongColumn.TYPE_CODE:
            converted = longcolumn.NullableLongColumn(values=self._values.astype(np.object))
        elif typecode == stringcolumn.NullableStringColumn.TYPE_CODE:
            vals = self._values.astype(np.object)
            for i, x in np.ndenumerate(vals):
                vals[i] = str(x)

            converted = stringcolumn.NullableStringColumn(values=vals)
        elif typecode == floatcolumn.NullableFloatColumn.TYPE_CODE:
            vals = self._values.astype(np.float32)
            vals = vals.astype(np.object)
            converted = floatcolumn.NullableFloatColumn(values=vals)
        elif typecode == doublecolumn.NullableDoubleColumn.TYPE_CODE:
            vals = self._values.astype(np.float64)
            vals = vals.astype(np.object)
            converted = doublecolumn.NullableDoubleColumn(values=vals)
        elif typecode == charcolumn.NullableCharColumn.TYPE_CODE:
            vals = self._values.astype(np.object)
            for i, x in np.ndenumerate(vals):
                vals[i] = ord(str(x)[0])

            converted = charcolumn.NullableCharColumn(values=vals)
        elif typecode == booleancolumn.NullableBooleanColumn.TYPE_CODE:
            vals = self._values.astype(np.bool)
            vals = vals.astype(np.object)
            converted = booleancolumn.NullableBooleanColumn(values=vals)
        elif typecode == binarycolumn.NullableBinaryColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = bytearray(int(x).to_bytes(4, byteorder="big", signed=True))

            converted = binarycolumn.NullableBinaryColumn(values=vals)
        else:
            raise dataframe.DataFrameException(
                "Unknown column type code: {}".format(typecode))

        # pylint: disable=protected-access
        converted._name = self._name
        return converted

    def _create_array(self, size=0):
        return np.zeros(size, dtype=np.int32)

class NullableIntColumn(column.Column):
    """A Column holding nullable int values.
    Any values not explicitly set are considered None.
    """

    TYPE_CODE = 12

    def __init__(self, name=None, values=None):
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
        if values is None:
            values = np.empty(0, dtype=np.object)

        if isinstance(values, list):
            for value in values:
                self._check_type(value)

            values = np.array(values, dtype=np.object)

        elif isinstance(values, np.ndarray):
            if values.dtype != "object":
                raise dataframe.DataFrameException(
                    ("Invalid argument array. Expected "
                     "int array (object) but found {}".format(values.dtype)))

            for value in values:
                self._check_type(value)

        elif isinstance(values, int):
            values = np.empty(values, dtype=np.object)
        else:
            raise dataframe.DataFrameException(
                ("Invalid argument array. Expected "
                 "list or numpy array but found {}".format(type(values))))

        super().__init__(name, values)

    def _check_type(self, value):
        if isinstance(value, int):
            if (value < -2147483648) or (value > 2147483647):
                raise dataframe.DataFrameException(
                    "Out of range int (int32): {}".format(value))

        elif value is not None and not isinstance(value, np.int32):
            raise dataframe.DataFrameException(
                ("Invalid argument. Expected "
                 "int (int32) but found {}".format(type(value))))

    def get_value(self, index):
        """Gets the int value at the specified index

        Args:
            index: The index of the value to get

        Returns:
            The int value at the specified index. May be None

        Raises:
            ValueError: If the specified index is out of bounds
        """
        self._check_bounds(index)
        val = self._values[index]
        if val is None:
            return None
        else:
            return int(val)

    def type_code(self):
        return NullableIntColumn.TYPE_CODE

    def type_name(self):
        return "int"

    def is_nullable(self):
        return True

    def is_numeric(self):
        return True

    def get_default_value(self):
        return None

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=invalid-name
    def convert_to(self, typecode):
        converted = None
        if typecode == bytecolumn.ByteColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.int8)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = int(np.int8(x))
                else:
                    vals[i] = 0

            converted = bytecolumn.ByteColumn(values=vals)
        elif typecode == shortcolumn.ShortColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.int16)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = int(np.int16(x))
                else:
                    vals[i] = 0

            converted = shortcolumn.ShortColumn(values=vals)
        elif typecode == IntColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.int32)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = int(np.int32(x))
                else:
                    vals[i] = 0

            converted = IntColumn(values=vals)
        elif typecode == longcolumn.LongColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.int64)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = int(np.int64(x))
                else:
                    vals[i] = 0

            converted = longcolumn.LongColumn(values=vals)
        elif typecode == stringcolumn.StringColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = str(x)
                else:
                    vals[i] = stringcolumn.StringColumn.DEFAULT_VALUE

            converted = stringcolumn.StringColumn(values=vals)
        elif typecode == floatcolumn.FloatColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.float32)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = float(x)
                else:
                    vals[i] = 0.0

            converted = floatcolumn.FloatColumn(values=vals)
        elif typecode == doublecolumn.DoubleColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.float64)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = float(x)
                else:
                    vals[i] = 0.0

            converted = doublecolumn.DoubleColumn(values=vals)
        elif typecode == charcolumn.CharColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.uint8)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = ord(str(x)[0])
                else:
                    vals[i] = charcolumn.CharColumn.DEFAULT_VALUE

            converted = charcolumn.CharColumn(values=vals)
        elif typecode == booleancolumn.BooleanColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.bool)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = (x != 0)
                else:
                    vals[i] = False

            converted = booleancolumn.BooleanColumn(values=vals)
        elif typecode == binarycolumn.BinaryColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = bytearray(int(x).to_bytes(4, byteorder="big", signed=True))
                else:
                    vals[i] = bytearray(int(0).to_bytes(4, byteorder="big", signed=True))

            converted = binarycolumn.BinaryColumn(values=vals)
        elif typecode == bytecolumn.NullableByteColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(np.int8(x)) if x is not None else None

            converted = bytecolumn.NullableByteColumn(values=vals)
        elif typecode == shortcolumn.NullableShortColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(np.int16(x)) if x is not None else None

            converted = shortcolumn.NullableShortColumn(values=vals)
        elif typecode == NullableIntColumn.TYPE_CODE:
            converted = self.clone()
        elif typecode == longcolumn.NullableLongColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(np.int64(x)) if x is not None else None

            converted = longcolumn.NullableLongColumn(values=vals)
        elif typecode == stringcolumn.NullableStringColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = str(x)
                else:
                    vals[i] = None

            converted = stringcolumn.NullableStringColumn(values=vals)
        elif typecode == floatcolumn.NullableFloatColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = float(x)
                else:
                    vals[i] = None

            converted = floatcolumn.NullableFloatColumn(values=vals)
        elif typecode == doublecolumn.NullableDoubleColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = float(x)
                else:
                    vals[i] = None

            converted = doublecolumn.NullableDoubleColumn(values=vals)
        elif typecode == charcolumn.NullableCharColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = ord(str(x)[0])
                else:
                    vals[i] = None

            converted = charcolumn.NullableCharColumn(values=vals)
        elif typecode == booleancolumn.NullableBooleanColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = (x != 0)
                else:
                    vals[i] = None

            converted = booleancolumn.NullableBooleanColumn(values=vals)
        elif typecode == binarycolumn.NullableBinaryColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = bytearray(int(x).to_bytes(4, byteorder="big", signed=True))
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
