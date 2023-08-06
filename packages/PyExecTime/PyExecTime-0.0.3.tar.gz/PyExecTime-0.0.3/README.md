# PyExecTime

PyExecTime is a python module which can be used to find the execution time of a complete or partial python code. 

## Version

The current version of this module is 0.0.3.

Check it by below command,

```bash
python -m pyexectime.version
```

## Installation

You can use `pip` to install the module or you clone the repository from github and install it manually.

```bash
pip install pyexectime
```

or

```bash
git clone https://github.com/antaripchatterjee/PyExecTime.git
cd PyExecTime
python setup.py install
```

## Usage and Application

You can use the module in two different ways.

### 1. Using contextlib manager `PyExecTime`

```python
# % API Reference % #

class PyExecTime():
    def __init__(self, file=sys.stdout):
        ...
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
    
    def __enter__(self):
        ...
```

Follow the below code to understand the usage of the contextlib manager class `PyExecTime`.

```python
from pyexectime.inspector import PyExecTime

with PyExecTime():
    for i in range(10000):
        print(i, end = ' ')
```

The above code will generate the below output.

```output
0 1 2 3 ....
....
....
.... 9998 9999
[Sat Mar  6 12:41:44 2021 PyExecTime(pyexectime\pyexectime_test.py) <4:6>] -> Execution took 0.000039 seconds
```

### 2. Using decorator function `py_exec_time`
```python
# % API Reference % #

def py_exec_time(file=sys.stdout):
    def wrapper(fn):
        @wraps(fn)
        def inner(*argv, **kwargv):
            ...
        return inner
    return wrapper
```
The same objective can be done using a following code

```python
from pyexectime.inspector import py_exec_time

@py_exec_time()
def write_number(r):
    for i in range(r):
        print(i, end = ' ')

write_number(10000)
```
And the output will be,

```output
0 1 2 3 ....
....
....
.... 9998 9999
[Sat Mar  6 12:41:44 2021 PyExecTime(test.py) <@test_dec:5>] -> Execution took 0.000035 seconds
```

## License

The module has been licensed under [MIT](https://github.com/antaripchatterjee/PyExecTime/blob/master/LICENSE) license.

## Development

Currently this python module is in BETA stage but it can be used safely.
