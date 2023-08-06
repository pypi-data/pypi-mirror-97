# aiotempfile

## Overview

Provides asynchronous temporary files.

## Compatibility

* Tested with python 3.8

## Installation
### From [pypi.org](https://pypi.org/project/aiotempfile/)

```
$ pip install aiotempfile
```

### From source code

```bash
$ git clone https://github.com/crashvb/aiotempfile
$ cd aiotempfile
$ virtualenv env
$ source env/bin/activate
$ python -m pip install --editable .[dev]
```

## Usage

This implementation is a derivation of [aiofiles](https://pypi.org/project/aiofile/) and functions the same way.

```python
import aiotempfile
async with aiotempfile.open() as file:
    file.write(b"data")
```

If the context manager is not used, files will need be explicitly closed; otherwise, they will only be removed during the interepreter teardown.

```python
import aiotempfile
file = await aiotempfile.open()
file.write(b"data")
file.close()
```

### Environment Variables

| Variable | Default Value | Description |
| ---------| ------------- | ----------- |
| AIOTEMPFILE_DEBUG | | Adds additional debug logging.

## Development

[Source Control](https://github.com/crashvb/aiotempfile)
