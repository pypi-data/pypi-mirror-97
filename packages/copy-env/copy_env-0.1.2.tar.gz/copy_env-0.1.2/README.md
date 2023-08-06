# copy_env

## Short Description
A package to copy environment requirements from one venv to another.

## Long Description
**copy_env** is a Python package allowing the user to copy requirements
from one venv to another. Users may interact with this package by importing
the copy_env function or from the command line as a script.

## Examples
### Command Line
C:\example\path\lib\site-packages> python \_\_init\_\_.py --source C:\example\path\python.exe --destination C:\other\example\python.exe
C:\example\path\lib\site-packages> python \_\_init\_\_.py -s C:\example\path\python.exe -d C:\other\example\python.exe

### Importing
    from copy_env import copy_env

    source: str = C:\example\path
    destination: str = C:\other\example

    copy_env(source, destination)
