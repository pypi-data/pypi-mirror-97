# docstring-extractor

This library allows parsing docstrings of an entire Python file. It uses [ast](https://docs.python.org/3/library/ast.html) and [docstring-parser](https://github.com/rr-/docstring_parser).

The main difference between this library and docstring-parser is that this one is able to parse entire Python files.

## Installation:
`pip install docstring-extractor`

## Usage

```python
>>> from canonicalwebteam.docstring_extractor import get_docstrings
>>>
>>> with open("example.py") as file:
...     docstrings = get_docstrings(file)
```

Imaging you have the following Python code:
```python
"""
Example module.

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua.
"""


def test_function():
    """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
    veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
    commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
    velit esse cillum dolore eu fugiat nulla pariatur.

    Parameters:
        a (int): A decimal integer
        b (int): Another decimal integer

    Returns:
        str: A string containing "foo"
    """
    return "foo"
```

The output of the `get_docstrings` function will be the following dict object:

```python
{'type': 'Module',
 'name': 'example',
 'line': 0,
 'docstring': <docstring_parser.common.Docstring at 0x7f06adee7a00>,
 'docstring_text': 'Example module.\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod\ntempor incididunt ut labore et dolore magna aliqua.',
 'content': [
    {'type': 'Function',
       'name': 'test_function',
       'line': 9,
       'docstring': <docstring_parser.common.Docstring at 0x7f06adef7490>,
       'docstring_text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim\nveniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea\ncommodo consequat. Duis aute irure dolor in reprehenderit in voluptate\nvelit esse cillum dolore eu fugiat nulla pariatur.\n\nParameters:\n    a (int): A decimal integer\n    b (int): Another decimal integer\n\nReturns:\n    str: A string containing "foo"',
    'content': []
    }
 ]
}
```

You can see the different properties of the Docstring object [here](https://github.com/rr-/docstring_parser/blob/master/docstring_parser/common.py), as an example if you are interested in obtaining the return type and return description of the first function:

```python
>>> docstrings["content"][0]["docstring"].returns.type_name
'str'
>>> docstrings["content"][0]["docstring"].returns.description
'A string containing "foo"'
```
