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
"""Provides support for reading and writing of CSV files.

This module uses DataFrame objects to represent CSV-files in memory.
A CSV-file can be read into a DataFrame by calling the read() function.

For example:

  >>>> import raven.io.csvfiles as csv
  >>>> df = csv.read("myfile.csv")

See the read() function for more arguments.

Analogously, a DataFrame object can be persisted as a CSV-file
by calling the write() function.

For example:

  >>>> import raven.io.csvfiles as csv
  >>>> csv.write("myfile.csv", df)

See the write() function for more arguments.
"""

import re as regex_matcher

import raven.struct.dataframe.core as dataframe
import raven.struct.dataframe.stringcolumn as stringcolumn
import raven.struct.dataframe._dataframeutils as dataframeutils

# pylint: disable=C0103, R0911, R0912, R0914, R0915, R1705

def read(filepath, separator=",", header=True, encoding="utf-8", types=None):
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

      >>> import raven.io.csvfiles as csv
      >>> df = csv.read("myfile.csv", types=("string", int", "float", "boolean"))

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
    if filepath is None:
        raise ValueError("File argument must not be None")

    if len(separator) != 1:
        raise ValueError("Separator must be one character long")

    csv = None
    with open(filepath, mode="r", encoding=encoding) as f:
        csv = [line.rstrip("\n") for line in f]

    return _df_from_csv_format(buffer=csv,
                               separator=separator,
                               header=header,
                               types=types)

def write(filepath, df, separator=",", header=True, encoding="utf-8"):
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
    if filepath is None:
        raise ValueError("File argument must not be None")

    if df is None:
        raise ValueError("DataFrame argument must not be None")

    if len(separator) != 1:
        raise ValueError("Separator must be one character long")

    buffer = _to_csv_format(df, separator, header, encoding)
    with open(filepath, mode="wb") as f:
        f.write(buffer)

    return len(buffer)

def _to_csv_format(df, separator, header, encoding):
    """Internal function for writing the content of
    the specified DataFrame into a CSV-format."""
    buffer = bytearray()
    separator_enc = separator.encode(encoding)
    nl = "\n".encode(encoding)
    nullvalue = "null".encode(encoding)
    cols = df.columns() #cache

    # add header if available and requested
    if df.has_column_names() and header:
        names = df.get_column_names()
        for i, elem in enumerate(names):
            buffer.extend(_escape(elem, separator).encode(encoding))
            if i < (len(names)-1):
                buffer.extend(separator_enc)

        buffer.extend(nl)

    # add rows
    for i in range(df.rows()):
        row = df.get_row(i)
        for j, elem in enumerate(row):
            if elem is not None:
                buffer.extend(_escape(str(elem), separator).encode(encoding))
            else:
                buffer.extend(nullvalue)

            if j < cols-1:
                buffer.extend(separator_enc)

        buffer.extend(nl)

    return buffer

def _df_from_csv_format(buffer, separator, header, types):
    """Internal function for deserializing the content of
    the specified string buffer to a DataFrame."""
    # regex which splits a string by the provided
    # separator if it is not enclosed by double quotes
    pattern = regex_matcher.compile(separator + "(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)")

    df = dataframe.DefaultDataFrame()
    line_index = 0
    try:
        if types is not None:
            if isinstance(types, tuple):
                types = list(types)

            for i, t in enumerate(types):
                types[i] = t.lower()
                df.add_column(_column_from_type(types[i]))

            if header:
                h = pattern.split(buffer[line_index], 0)
                for i, elem in enumerate(h):
                    h[i] = _normalize(elem)

                df.set_column_names(h)
                line_index += 1

            for _ in range(line_index, len(buffer), 1):
                if not buffer[line_index]: # skip empty lines
                    continue

                blocks = pattern.split(_process(buffer[line_index], separator), 0)
                converted = [None] * len(blocks)
                for i, block in enumerate(blocks):
                    try:
                        converted[i] = _convert_type(types[i], _normalize(block))
                    except (ValueError, TypeError) as ex:
                        raise IOError(
                            ("Improperly formatted CSV "
                             "file at line: {}").format(line_index + 1)) from ex

                try:
                    df.add_row(converted)
                except dataframe.DataFrameException: # null value in row
                    df = dataframe.DataFrame.convert_to(df, "NullableDataFrame")
                    df.add_row(converted)

                line_index += 1

        else:
            if header:
                h = pattern.split(buffer[line_index], 0)
                for i, elem in enumerate(h):
                    h[i] = _normalize(elem)
                    df.add_column(stringcolumn.StringColumn())

                df.set_column_names(h)
            else:
                first = pattern.split(buffer[line_index], 0)
                for i, elem in enumerate(first):
                    first[i] = _normalize(elem)
                    df.add_column(stringcolumn.StringColumn())

                df.add_row(first)

            line_index += 1
            for _ in range(line_index, len(buffer), 1):
                if not buffer[line_index]: # skip empty lines
                    continue

                blocks = pattern.split(_process(buffer[line_index], separator), 0)
                for i, block in enumerate(blocks):
                    if blocks[i] == "null":
                        blocks[i] = None
                    else:
                        blocks[i] = _normalize(block)

                try:
                    df.add_row(blocks)
                except dataframe.DataFrameException: # null value in row
                    df = dataframe.DataFrame.convert_to(df, "NullableDataFrame")
                    df.add_row(blocks)

                line_index += 1

    except (IndexError) as ex:
        raise IOError(
            ("Improperly formatted CSV "
             "file at line: {}").format(line_index)) from ex

    return df

def _convert_type(typename, obj):
    """Converts the specified object to the corresponding type
    denoted by the specified type name."""
    if obj == "null":
        return None

    if typename == "byte":
        return int(obj)
    elif typename == "short":
        return int(obj)
    elif typename in ("int", "integer"):
        return int(obj)
    elif typename == "long":
        return int(obj)
    elif typename in ("string", "str"):
        return obj
    elif typename == "float":
        return float(obj)
    elif typename == "double":
        return float(obj)
    elif typename in ("char", "character"):
        s = str(obj)
        if len(s) > 1:
            raise ValueError("Invalid char value: '{}'".format(s))

        return s
    elif typename in ("boolean", "bool"):
        return obj.lower() in ("true", "t", "yes", "y", "1")
    else:
        return obj

def _column_from_type(typename):
    """Returns the corresponding Column from the specified type name argument."""
    if not isinstance(typename, str):
        raise ValueError(
            ("Invalid type name argument. "
             "Expected str but found {}").format(type(typename)))

    if typename == "binary":
        raise ValueError(
            ("Invalid type name argument. "
             "Binary columns are not supported in CSV files"))

    col = dataframeutils.column_from_typename(typename)
    if col is None:
        raise ValueError("Invalid column type: '{}'".format(typename))

    return col

def _escape(s, separator):
    """Escapes the specified string if it contains
    the specified separator character."""
    if separator in s:
        return "\"" + s + "\""
    else:
        return s

def _normalize(s):
    """Normalizes the specified string by removing escaping quotes."""
    if s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    else:
        return s

def _process(line, separator):
    """Processes a text line and handles malformed formats."""
    if line.startswith(separator):
        line = "null" + line

    s = separator + separator
    while s in line:
        line = line.replace(s, separator + "null" + separator)

    if line.endswith(separator):
        line = line + "null"

    return line
