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
Provides serialization and I/O support for DataFrames.
"""

import os
import zlib
import base64

from struct import pack
from struct import unpack

import numpy as np

import raven.struct.dataframe.core as dataframe
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

# pylint: disable=C0103, R1702, R0912, R0914, R0915

def serialize(df, compress=False):
    """Serializes the given DataFrame to a bytearray.

    The compression of the returned bytearray is controlled by the additional
    boolean flag of this method.

    Args:
        df: The DataFrame to serialize. Must not be None
        compress: A boolean flag indicating whether the returned bytearray should
            be compressed. Must be a bool

    Returns;
        A bytearray representing the given DataFrame in a serialized form

    Raises:
        DataFrameException: If any errors occur during serialization or compression
    """
    if df is None:
        raise dataframe.DataFrameException("DataFrame argument must not be None")

    if not isinstance(df, dataframe.DataFrame):
        raise ValueError(
            ("Invalid argument 'df'. "
             "Expected raven.struct.dataframe.DataFrame but found {}").format(type(df)))

    if not isinstance(compress, bool):
        raise ValueError(
            ("Invalid argument 'compress'. "
             "Expected bool but found {}").format(type(compress)))

    return _compress(_serialize_v2(df)) if compress else _serialize_v2(df)

def deserialize(data):
    """Deserializes the given bytearray to a DataFrame.

    If the given bytearray is compressed, it will be automatically decompressed
    before the deserialization is executed.

    Args:
        data: The bytearray representing the DataFrame to deserialize.
            Must not be None

    Returns:
        A DataFrame from the given bytearray

    Raises:
        DataFrameException: If any errors occur during deserialization or
            decompression, or if the given bytearray does not
            constitute a DataFrame
    """
    return _deserialize_v2(_check_header(data))

def write_file(filepath, df):
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
    if not isinstance(filepath, str):
        raise ValueError(
            ("Invalid argument 'filepath'. "
             "Expected str but found {}").format(type(filepath)))

    if os.path.isdir(filepath):
        if not isinstance(df, dict):
            raise ValueError(
                ("Invalid argument 'df'. "
                 "Expected dict mapping str to "
                 "DataFrame but found {}").format(type(df)))

        for k, v in df.items():
            if not isinstance(k, str):
                raise ValueError(
                    ("Invalid key type. Expected "
                     "str but found {}").format(type(k)))

            if not isinstance(v, dataframe.DataFrame):
                raise ValueError(
                    ("Invalid value type. Expected "
                     "DataFrame but found {}").format(type(v)))

            name = k if k.endswith(".df") else k + ".df"
            _write_file0(os.path.join(filepath, name), v)

    else:
        if not isinstance(df, dataframe.DataFrame):
            raise ValueError(
                ("Invalid argument 'df'. "
                 "Expected DataFrame but found {}").format(type(df)))

        _write_file0(filepath, df)

def read_file(filepath):
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
    if not isinstance(filepath, str):
        raise ValueError(
            ("Invalid argument 'filepath'. "
             "Expected str but found {}").format(type(filepath)))

    if os.path.isdir(filepath):
        files = [f for f in os.listdir(filepath) if f.endswith(".df")]
        if len(files) == 0:
            raise FileNotFoundError(
                ("The specified directory does not contain "
                 "any DataFrame (.df) files: '{}'")
                .format(filepath))

        dataframes = dict()
        for f in files:
            name = f[:-3]
            dataframes[name] = _read_file0(os.path.join(filepath, f))

        return dataframes

    else:
        return _read_file0(filepath)

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
    if not isinstance(string, str):
        raise ValueError(
            ("Invalid argument. Expected str but found {}").format(type(string)))

    return deserialize(bytearray(base64.b64decode(string)))

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
    return base64.b64encode(_compress(serialize(df))).decode("utf-8")

def _read_file0(filepath):
    """Reads the specified file and returns a DataFrame constituted by the
    content of that file.

    Args:
        filepath: The DataFrame file to read. Must be a str representing
            the path to the file to read

    Returns:
        A DataFrame from the specified file

    Raises:
        FileNotFoundError: If the specified file cannot be found
        PermissionError: If the permission for reading the
            specified file was denied
        DataFrameException: If any errors occur during deserialization
            or the file format is invalid
    """
    with open(filepath, mode="rb") as f:
        data = f.read()
        data = bytearray(data)

    return deserialize(_decompress(data))

def _write_file0(filepath, df):
    """Persists the given DataFrame to the specified file.

    Args:
        filepath: The file to write the DataFrame to. Must be a str representing
            the path to the file to write
        df: The DataFrame to persist. Must not be None

    Raises:
        PermissionError: If the permission for writing the
            specified file was denied
        DataFrameException: If any errors occur during file persistence
            or if any errors occur during serialization
    """
    data = _compress(serialize(df))
    with open(filepath, "wb") as f:
        f.write(data)

def _compress(data):
    """Compresses the given bytearray such that it represents
    a serialized DataFrame.

    Args:
        data: The bytes to compress, as a bytearray

    Returns:
        The compressed bytearray
    """
    data = bytearray(zlib.compress(data))
    data[0] = 0x64
    data[1] = 0x66
    return data

def _decompress(data):
    """Decompresses the given bytearray.

    Args:
        data: The bytearray to decompress

    Returns:
        The decompressed bytearray
    """
    if not len(data) > 2:
        raise dataframe.DataFrameException("Invalid data format")

    if data[0] != 0x64 or data[1] != 0x66:
        raise dataframe.DataFrameException(
            ("Invalid data format. Is not a .df file. "
             "Starts with 0x{} 0x{}").format(
                 bytearray(data[0].to_bytes(1, byteorder="big", signed=True)).hex(),
                 bytearray(data[1].to_bytes(1, byteorder="big", signed=True)).hex()))

    data[0] = 0x78
    data[1] = 0x9c
    data = zlib.decompress(data)
    return bytearray(data)

def _check_header(data):
    """Validates the first few header bytes of a serialized DataFrame.

    If the serialized DataFrame is compressed, then this function performs
    decomression and returns the result

    Args:
        data: A bytearray representing the serialized DataFrame

    Returns:
        The argument bytearray, possibly decomressed

    Raises:
        DataFrameException: If the validation failed
    """
    if not isinstance(data, bytearray):
        raise ValueError(
            ("Invalid argument 'data'. "
             "Expected bytearray but found {}").format(type(data)))

    if data[0] == 0x64 and data[1] == 0x66:
        data = _decompress(data)

    # validate the first bytes of the header and
    # the used format version must start with '{v:'
    if (data[0] != 0x7b or data[1] != 0x76 or data[2] != 0x3a
            or (data[3] != 0x32 and data[3] != 0x31)):

        raise dataframe.DataFrameException("Unsupported encoding")

    if data[3] != 0x32: # encoding version 2
        raise dataframe.DataFrameException(
            ("Unsupported encoding version (v:{})").format(data[3]))

    return data

def _serialize_v2(df):
    """Serialization to the binary-based version 2 format (v2).

    Args:
        df: The DataFrame to serialize

    Returns:
        A bytearray representing the given DataFrame
    """
    buffer = bytearray()
    #HEADER
    # must start with {v:2;
    buffer.append(0x7b)
    buffer.append(0x76)
    buffer.append(0x3a)
    buffer.append(0x32)
    buffer.append(0x3b)

    # impl: default=0x64 nullable=0x6e
    buffer.append(0x6e if df.is_nullable() else 0x64)

    rows = df.rows()
    if rows > 0xffffffff:
        raise dataframe.DataFrameException(
            ("Unable to serialize DataFrame with "
             "row count greater than 0xffffffff"))

    buffer.extend(rows.to_bytes(4, byteorder="big", signed=False))
    cols = df.columns()
    if cols > 0xffffffff:
        raise dataframe.DataFrameException(
            ("Unable to serialize DataFrame with "
             "column count greater than 0xffffffff"))

    buffer.extend(cols.to_bytes(4, byteorder="big", signed=False))

    if df.has_column_names():
        for name in df.get_column_names():
            buffer.extend(bytearray(name, "utf-8"))
            # add null byte as name delimeter
            buffer.append(0x00)

    else:
        # set indices as strings
        for i in range(cols):
            buffer.extend(bytearray(str(i), "utf-8"))
            buffer.append(0x00)

    for col in df:
        buffer.append(col.type_code())

    if df.is_nullable(): # NullableDataFrame
        # The specification requires a lookup list for differentiating between
        # default values (for example: zeros for numbers) and actual null values.
        # This is implemented here as a bit vector initialized with all bits
        # set to zero.
        # As the lookup list is part of the header, we must first serialize the
        # entire payload and build the lookup list and then bind all the parts
        # together at the end
        header = buffer
        buffer = bytearray()

        # the lookup list
        lookup_bits = BitVector()
        #PAYLOAD
        for col in df:
            type_code = col.type_code()
            val = col.as_array()
            if type_code == bytecolumn.NullableByteColumn.TYPE_CODE:
                for i in range(rows):
                    if val[i] is None:
                        buffer.append(0x00)
                        lookup_bits.add1()
                    elif val[i] == 0:
                        buffer.append(0x00)
                        lookup_bits.add0()
                    else:
                        buffer.extend(int(val[i]).to_bytes(1, byteorder="big", signed=True))

            elif type_code == shortcolumn.NullableShortColumn.TYPE_CODE:
                for i in range(rows):
                    if val[i] is None:
                        buffer.extend(b'\x00\x00')
                        lookup_bits.add1()
                    elif val[i] == 0:
                        buffer.extend(b'\x00\x00')
                        lookup_bits.add0()
                    else:
                        buffer.extend(int(val[i]).to_bytes(2, byteorder="big", signed=True))

            elif type_code == intcolumn.NullableIntColumn.TYPE_CODE:
                for i in range(rows):
                    if val[i] is None:
                        buffer.extend(b'\x00\x00\x00\x00')
                        lookup_bits.add1()
                    elif val[i] == 0:
                        buffer.extend(b'\x00\x00\x00\x00')
                        lookup_bits.add0()
                    else:
                        buffer.extend(int(val[i]).to_bytes(4, byteorder="big", signed=True))

            elif type_code == longcolumn.NullableLongColumn.TYPE_CODE:
                for i in range(rows):
                    if val[i] is None:
                        buffer.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00')
                        lookup_bits.add1()
                    elif val[i] == 0:
                        buffer.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00')
                        lookup_bits.add0()
                    else:
                        buffer.extend(int(val[i]).to_bytes(8, byteorder="big", signed=True))

            elif type_code == stringcolumn.NullableStringColumn.TYPE_CODE:
                for i in range(rows):
                    if val[i] is None:
                        lookup_bits.add1()
                    elif len(val[i]) == 0:
                        lookup_bits.add0()
                    else:
                        buffer.extend(val[i].encode("utf-8"))

                    # add null character as string delimeter
                    buffer.append(0x00)

            elif type_code == floatcolumn.NullableFloatColumn.TYPE_CODE:
                for i in range(rows):
                    if val[i] is None:
                        buffer.extend(b'\x00\x00\x00\x00')
                        lookup_bits.add1()
                    # bit representation of zero is strictly
                    # defined so we compare directly
                    elif val[i] == 0.0:
                        buffer.extend(b'\x00\x00\x00\x00')
                        lookup_bits.add0()
                    else:
                        buffer.extend(pack(">f", val[i]))

            elif type_code == doublecolumn.NullableDoubleColumn.TYPE_CODE:
                for i in range(rows):
                    if val[i] is None:
                        buffer.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00')
                        lookup_bits.add1()
                    # bit representation of zero is strictly
                    # defined so we compare directly
                    elif val[i] == 0.0:
                        buffer.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00')
                        lookup_bits.add0()
                    else:
                        buffer.extend(pack(">d", val[i]))

            elif type_code == charcolumn.NullableCharColumn.TYPE_CODE:
                for i in range(rows):
                    if val[i] is None:
                        buffer.append(0x00)
                    else:
                        buffer.extend(val[i].to_bytes(1, byteorder="big", signed=True))

            elif type_code == booleancolumn.NullableBooleanColumn.TYPE_CODE:
                bits = BitVector()
                for i in range(rows):
                    if val[i] is None:
                        bits.add0()
                        lookup_bits.add1()
                    else:
                        if val[i]:
                            bits.add1()
                        else:
                            bits.add0()
                            lookup_bits.add0()
                buffer.extend(bits.tobytearray())

            elif type_code == binarycolumn.NullableBinaryColumn.TYPE_CODE:
                for i in range(rows):
                    dataLength = len(val[i]) if val[i] is not None else 0
                    buffer.extend(dataLength.to_bytes(4, byteorder="big"))
                    if val[i] is not None:
                        buffer.extend(val[i])

            else:
                raise dataframe.DataFrameException("Unknown column type: {}".format(type_code))

        #END PAYLOAD
        # copy operations to stick everything together
        payload = buffer
        # allocate buffer for the final result
        buffer = header
        # Number of byte blocks of the lookup list.
        # The specification requires that the lookup
        # list has a minimum length of one block
        blength = int(((lookup_bits.size()-1)/8) + 1)
        buffer.extend(blength.to_bytes(4, byteorder="big", signed=False))
        # copy lookup bits
        buffer.extend(lookup_bits.tobytearray())
        # add header closing brace '}'
        buffer.append(0x7d)
        # copy payload buffer
        buffer.extend(payload)

    else:# DefaultDataFrame
        buffer.append(0x7d) # add header closing brace '}'
        #END HEADER
        # As DefaultDataFrames do not have null values, no lookup list
        # is required and we just serialize all bytes as they are to
        # the payload section
        #PAYLOAD
        for col in df:
            type_code = col.type_code()
            val = col.as_array()
            if type_code == bytecolumn.ByteColumn.TYPE_CODE:
                for i in range(rows):
                    buffer.extend(int(val[i]).to_bytes(1, byteorder="big", signed=True))

            elif type_code == shortcolumn.ShortColumn.TYPE_CODE:
                for i in range(rows):
                    buffer.extend(int(val[i]).to_bytes(2, byteorder="big", signed=True))

            elif type_code == intcolumn.IntColumn.TYPE_CODE:
                for i in range(rows):
                    buffer.extend(int(val[i]).to_bytes(4, byteorder="big", signed=True))

            elif type_code == longcolumn.LongColumn.TYPE_CODE:
                for i in range(rows):
                    buffer.extend(int(val[i]).to_bytes(8, byteorder="big", signed=True))

            elif type_code == stringcolumn.StringColumn.TYPE_CODE:
                for i in range(rows):
                    buffer.extend(val[i].encode("utf-8"))
                    # add null character as string delimeter
                    buffer.append(0x00)

            elif type_code == floatcolumn.FloatColumn.TYPE_CODE:
                for i in range(rows):
                    buffer.extend(pack(">f", val[i]))

            elif type_code == doublecolumn.DoubleColumn.TYPE_CODE:
                for i in range(rows):
                    buffer.extend(pack(">d", val[i]))

            elif type_code == charcolumn.CharColumn.TYPE_CODE:
                for i in range(rows):
                    buffer.extend(int(val[i]).to_bytes(1, byteorder="big", signed=True))

            elif type_code == booleancolumn.BooleanColumn.TYPE_CODE:
                bits = BitVector()
                for i in range(rows):
                    if val[i]:
                        bits.add1()
                    else:
                        bits.add0()
                buffer.extend(bits.tobytearray())

            elif type_code == binarycolumn.BinaryColumn.TYPE_CODE:
                for i in range(rows):
                    buffer.extend(len(val[i]).to_bytes(4, byteorder="big"))
                    buffer.extend(val[i])

            else:
                raise dataframe.DataFrameException("Unknown column type: {}".format(type_code))

        #END PAYLOAD

    return buffer

def _deserialize_v2(buffer):
    """Deserialization from the binary-based version 2 format (v2).

    Args:
        buffer: The bytearray representing the DataFrame to deserialize

    Returns:
        A DataFrame from the given bytearray
    """
    #HEADER
    ptr = 5 # index pointer
    dftype = buffer[ptr]
    if not dftype in (0x64, 0x6e):
        raise dataframe.DataFrameException("Unsupported DataFrame implementation")

    # header format is {v:2;irrrrccccName1.Name2.ttllllbbb}0x...
    # code of the DataFrame implementation
    impl_default = (dftype == 0x64)
    ptr += 1
    rows = int.from_bytes(buffer[ptr:ptr+4], byteorder="big", signed=False)
    ptr += 4
    cols = int.from_bytes(buffer[ptr:ptr+4], byteorder="big", signed=False)
    ptr += 4

    # column labels
    names = []
    for i in range(cols):
        c0 = ptr # first char
        while buffer[ptr] != 0x00:
            ptr += 1
        ptr += 1
        names.append(buffer[c0:ptr-1].decode("utf-8"))

    # column types
    types = []
    for i in range(cols):
        types.append(buffer[ptr])
        ptr += 1

    df = None
    columns = []
    if not impl_default: # NullableDataFrame
        # first read the entire lookup list into memory
        lookup_length = int.from_bytes(buffer[ptr:ptr+4], byteorder="big", signed=False)
        ptr += 4
        lookup_bits = BitVector(buffer[ptr:ptr+lookup_length])

        # list index pointing to the next readable bit within the lookup list
        li = 0
        ptr += lookup_length
        if buffer[ptr] != 0x7d: # header closing brace '}' missing
            raise dataframe.DataFrameException("Invalid format")

        #END HEADER

        #PAYLOAD
        for i in range(cols):
            val = np.empty(rows, dtype=np.object)
            if types[i] == bytecolumn.NullableByteColumn.TYPE_CODE:
                for j in range(rows):
                    ptr += 1
                    b = int.from_bytes(buffer[ptr:ptr+1], byteorder="big", signed=True)
                    if b == 0:
                        if not lookup_bits.get(li):
                            val[j] = 0

                        li += 1
                    else:
                        val[j] = b

                columns.append(bytecolumn.NullableByteColumn(names[i], val))

            elif types[i] == shortcolumn.NullableShortColumn.TYPE_CODE:
                for j in range(rows):
                    ptr += 2
                    b = int.from_bytes(buffer[ptr-1:ptr+1], byteorder="big", signed=True)
                    if b == 0:
                        if not lookup_bits.get(li):
                            val[j] = 0

                        li += 1
                    else:
                        val[j] = b

                columns.append(shortcolumn.NullableShortColumn(names[i], val))

            elif types[i] == intcolumn.NullableIntColumn.TYPE_CODE:
                for j in range(rows):
                    ptr += 4
                    b = int.from_bytes(buffer[ptr-3:ptr+1], byteorder="big", signed=True)
                    if b == 0:
                        if not lookup_bits.get(li):
                            val[j] = 0

                        li += 1
                    else:
                        val[j] = b

                columns.append(intcolumn.NullableIntColumn(names[i], val))

            elif types[i] == longcolumn.NullableLongColumn.TYPE_CODE:
                for j in range(rows):
                    ptr += 8
                    b = int.from_bytes(buffer[ptr-7:ptr+1], byteorder="big", signed=True)
                    if b == 0:
                        if not lookup_bits.get(li):
                            val[j] = 0

                        li += 1
                    else:
                        val[j] = b

                columns.append(longcolumn.NullableLongColumn(names[i], val))

            elif types[i] == stringcolumn.NullableStringColumn.TYPE_CODE:
                for j in range(rows):
                    ptr += 1
                    c0 = ptr # marks the first character of each string
                    while buffer[ptr] != 0x00:
                        ptr += 1

                    if (ptr-c0) == 0:
                        if not lookup_bits.get(li):
                            val[j] = ""

                        li += 1
                    else:
                        val[j] = buffer[c0:ptr].decode("utf-8")

                columns.append(stringcolumn.NullableStringColumn(names[i], val))

            elif types[i] == floatcolumn.NullableFloatColumn.TYPE_CODE:
                for j in range(rows):
                    ptr += 4
                    # since Python does not have float32, we need to do a conversion
                    # over numpy and str to get the same precision as the original value
                    f = float(str(np.float32(unpack(">f", buffer[ptr-3:ptr+1])[0])))
                    if f == 0.0:
                        if not lookup_bits.get(li):
                            val[j] = 0.0

                        li += 1
                    else:
                        val[j] = f

                columns.append(floatcolumn.NullableFloatColumn(names[i], val))

            elif types[i] == doublecolumn.NullableDoubleColumn.TYPE_CODE:
                for j in range(rows):
                    ptr += 8
                    f = unpack(">d", buffer[ptr-7:ptr+1])[0]
                    if f == 0.0:
                        if not lookup_bits.get(li):
                            val[j] = 0.0

                        li += 1
                    else:
                        val[j] = f

                columns.append(doublecolumn.NullableDoubleColumn(names[i], val))

            elif types[i] == charcolumn.NullableCharColumn.TYPE_CODE:
                for j in range(rows):
                    ptr += 1
                    c = int.from_bytes(buffer[ptr:ptr+1], byteorder="big", signed=False)
                    if c == 0:
                        val[j] = None
                    else:
                        val[j] = chr(c)

                columns.append(charcolumn.NullableCharColumn(names[i], val))

            elif types[i] == booleancolumn.NullableBooleanColumn.TYPE_CODE:
                length = int(rows/8 if (rows%8 == 0) else ((rows/8) + 1))
                ptr += 1 # focus on next readable position
                bits = BitVector(buffer[ptr:ptr+length])
                for j in range(rows):
                    if not bits.get(j):
                        if not lookup_bits.get(li):
                            val[j] = False

                        li += 1
                    else:
                        val[j] = True

                # let the base pointer jump forward to the last read byte
                ptr += (length-1)
                columns.append(booleancolumn.NullableBooleanColumn(names[i], val))

            elif types[i] == binarycolumn.NullableBinaryColumn.TYPE_CODE:
                for j in range(rows):
                    ptr += 1
                    length = int.from_bytes(buffer[ptr:ptr+4], byteorder="big", signed=False)
                    ptr += 3
                    if length != 0:
                        data = bytearray(length)
                        for k in range(length):
                            ptr += 1
                            data[k] = buffer[ptr]

                        val[j] = data

                columns.append(binarycolumn.NullableBinaryColumn(names[i], val))

            else:
                raise dataframe.DataFrameException(
                    ("Unknown column with type code {}").format(types[i]))

        #END PAYLOAD
        if cols == 0: # uninitialized instance
            df = dataframe.NullableDataFrame()
        else:
            df = dataframe.NullableDataFrame(columns)

    else: # DefaultDataFrame
        if buffer[ptr] != 0x7d: # header closing brace '}'
            raise dataframe.DataFrameException("Invalid format")

        #END HEADER

        #PAYLOAD
        for i in range(cols):
            if types[i] == bytecolumn.ByteColumn.TYPE_CODE:
                val = np.empty(rows, dtype=np.int8)
                for j in range(rows):
                    ptr += 1
                    val[j] = int.from_bytes(buffer[ptr:ptr+1], byteorder="big", signed=True)

                columns.append(bytecolumn.ByteColumn(names[i], val))

            elif types[i] == shortcolumn.ShortColumn.TYPE_CODE:
                val = np.empty(rows, dtype=np.int16)
                for j in range(rows):
                    ptr += 2
                    val[j] = int.from_bytes(buffer[ptr-1:ptr+1], byteorder="big", signed=True)

                columns.append(shortcolumn.ShortColumn(names[i], val))

            elif types[i] == intcolumn.IntColumn.TYPE_CODE:
                val = np.empty(rows, dtype=np.int32)
                for j in range(rows):
                    ptr += 4
                    val[j] = int.from_bytes(buffer[ptr-3:ptr+1], byteorder="big", signed=True)

                columns.append(intcolumn.IntColumn(names[i], val))

            elif types[i] == longcolumn.LongColumn.TYPE_CODE:
                val = np.empty(rows, dtype=np.int64)
                for j in range(rows):
                    ptr += 8
                    val[j] = int.from_bytes(buffer[ptr-7:ptr+1], byteorder="big", signed=True)

                columns.append(longcolumn.LongColumn(names[i], val))

            elif types[i] == stringcolumn.StringColumn.TYPE_CODE:
                val = np.empty(rows, dtype=np.object)
                for j in range(rows):
                    ptr += 1
                    c0 = ptr # marks the first character of each string
                    while buffer[ptr] != 0x00:
                        ptr += 1

                    if (ptr-c0) == 0:
                        val[j] = stringcolumn.StringColumn.DEFAULT_VALUE
                    else:
                        val[j] = buffer[c0:ptr].decode("utf-8")

                columns.append(stringcolumn.StringColumn(names[i], val))

            elif types[i] == floatcolumn.FloatColumn.TYPE_CODE:
                val = np.empty(rows, dtype=np.float32)
                for j in range(rows):
                    ptr += 4
                    # since Python does not have float32, we need to do a conversion
                    # over numpy and str to get the same precision as the original value
                    val[j] = float(str(np.float32(unpack(">f", buffer[ptr-3:ptr+1])[0])))

                columns.append(floatcolumn.FloatColumn(names[i], val))

            elif types[i] == doublecolumn.DoubleColumn.TYPE_CODE:
                val = np.empty(rows, dtype=np.float64)
                for j in range(rows):
                    ptr += 8
                    val[j] = unpack(">d", buffer[ptr-7:ptr+1])[0]

                columns.append(doublecolumn.DoubleColumn(names[i], val))

            elif types[i] == charcolumn.CharColumn.TYPE_CODE:
                val = np.empty(rows, dtype=np.uint8)
                for j in range(rows):
                    ptr += 1
                    c = int.from_bytes(buffer[ptr:ptr+1], byteorder="big", signed=False)
                    val[j] = c

                columns.append(charcolumn.CharColumn(names[i], val))

            elif types[i] == booleancolumn.BooleanColumn.TYPE_CODE:
                val = np.empty(rows, dtype=np.bool)
                length = int(rows/8 if (rows%8 == 0) else ((rows/8) + 1))
                ptr += 1 # focus on next readable position
                bits = BitVector(buffer[ptr:ptr+length])
                for j in range(rows):
                    val[j] = bits.get(j)

                ptr += (length-1)
                columns.append(booleancolumn.BooleanColumn(names[i], val))

            elif types[i] == binarycolumn.BinaryColumn.TYPE_CODE:
                val = np.empty(rows, dtype=np.object)
                for j in range(rows):
                    ptr += 1
                    length = int.from_bytes(buffer[ptr:ptr+4], byteorder="big", signed=False)
                    ptr += 3
                    data = bytearray(length)
                    for k in range(length):
                        ptr += 1
                        data[k] = buffer[ptr]

                    val[j] = data

                columns.append(binarycolumn.BinaryColumn(names[i], val))

            else:
                raise dataframe.DataFrameException(
                    ("Unknown column with type code {}").format(types[i]))

        #END PAYLOAD
        if cols == 0: # uninitialized instance
            df = dataframe.DefaultDataFrame()
        else:
            df = dataframe.DefaultDataFrame(columns)

    return df

class BitVector:
    """Simple bit vector implementation used in serialization routines."""

    def __init__(self, bits=None):
        if bits is None:
            self.bits = bytearray(512)
            self.block = 0
            self.index = 0
        else:
            self.bits = bits
            self.block = len(bits)
            self.index = len(bits) * 8

    def add1(self):
        """Adds a 1-bit to this BitVector"""
        self._ensure_capacity()
        self.bits[self.block] |= (1 << (7-(self.index%8)))
        self.index += 1
        self.block = self.index // 8

    def add0(self):
        """Adds a 0-bit to this BitVector"""
        self._ensure_capacity()
        self.index += 1
        self.block = self.index // 8

    def get(self, index):
        """Gets the bit at the specified index as a bool

        Args:
            index: The index of the bit to get, as an int

        Returns:
            The bit at the specified index, as a bool
        """
        return self.bits[int(index/8)] & (1 << (7-(index%8))) != 0

    def size(self):
        """Indicates the current size of this BitVector.

        Returns:
            The size of this BitVector as an int
        """
        return self.index

    def tobytearray(self):
        """Returns this BitVector as a bytearray

        Returns:
            A bytearray with the content of this BitVector
        """
        end = self.block+1 if self.index%8 != 0 else self.block
        return self.bits[:end]

    def _ensure_capacity(self):
        """Ensures that an additional bit can be added to this BitVector"""
        if self.block >= len(self.bits):
            self.bits.extend(bytearray(len(self.bits)))
