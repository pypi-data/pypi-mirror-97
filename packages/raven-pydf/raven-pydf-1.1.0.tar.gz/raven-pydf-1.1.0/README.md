# Pydf: An Implementation of the DataFrame specification in Python

This is the official implementation of the DataFrame specification provided by Raven Computing.

## Getting Started

This library is available on PyPI.

Install via:
```
pip install raven-pydf
```

For more information see [pypi.org](https://pypi.org/project/raven-pydf/).

After installation you can use the entire DataFrame API by importing one class:
```python
from raven.struct.dataframe import DataFrame

# read a DataFrame file into memory
df = DataFrame.read("/path/to/myFile.df")

# show the first 10 rows on stdout
print(df.head(10))
```
Alternatively, you can import all concrete Column types directly, for example:
```python
from raven.struct.dataframe import (DefaultDataFrame,
                                    IntColumn,
                                    FloatColumn,
                                    StringColumn)

# create a DataFrame with 3 columns and 3 rows
df = DefaultDataFrame(
        IntColumn("A", [1, 2, 3]),
        FloatColumn("B", [4.4, 5.5, 6.6])
        StringColumn("C", ["cat", "dog", "horse"]))

print(df)
```

## Compatibility

This library requires **Python3.7** or higher.

Internally, this library uses [Numpy](https://github.com/numpy/numpy) for array operations. The minimum required version is v1.19.0

## Documentation

The unified documentation is available [here](https://www.raven-computing.com/docs/dataframe?language=python).

## Development

If you want to change code of this library or if you want to include it manually as a dependency without installing via PIP, you can do so by cloning this repository.

### Setup

We are using virtual environments and the [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) utilities for all of our Python projects. If you are running on *Linux* then you can set up your development environment by sourcing the **setup.sh** script. This will create a virtual environment *pydf* for you and install all dependencies:
```
source setup.sh
```

### Running Tests

Execute all unit tests via:
```
python -m unittest
```

### Linting

Run *pylint* to perform static code analysis of the source code via:
```
pylint raven
```

## License

This library is licensed under the Apache License Version 2 - see the [LICENSE](LICENSE) for details.

