# OpenTEA

![logo](http://cerfacs.fr/coop/whatwedo/logo_opentea_medium.gif)

OpenTEA is a graphical user interface engine. It convert a set of degrees of freedom, expressed in SCHEMA, into graphical forms.

![example](http://cerfacs.fr/coop/whatwedo/opentea_gui_full.png)

The documentation is currently available in [ReadtheDocs](https://opentea.readthedocs.io/en/latest/)


## Installation 

Opentea is OpenSource (Cecill-B) available on PiPY. 

```bash
>pip install opentea
```

then test your installation with

```bash
>opentea3 test-gui trivial
```

## Basic Usage

OpenTEA is a GUI engine, based on the json-SCHEMA description. For example, assume a nested information conforming to the following SCHEMA :

```yaml
---
title: "Trivial form..."
type: object
properties:
  first_tab:
    type: object
    title: Only tab.
    process: custom_callback.py
    properties:
      first_block:
        type: object
        title: Custom Block
        properties:
          number_1:
            title: "Number 1"
            type: number
            default: 32.
          operand:
            title: "Operation"
            type: string
            default: "+"
            enum: ["+", "-", "*", "/"]
          number_2:
            title: "Number 2"
            type: number
            default: 10.
          result:
            title: "result"
            state: disabled
            type: string
            default: "-"
```

The openTEA GUI will show as :
![Trivial GUI](http://cerfacs.fr/coop/whatwedo/opentea_trivial.png)

In this form, a callback can be added to each tab.
The corresponding `custom_callback.py` script is :

```python
"""Module for the first tab."""

from opentea.process_utils import process_tab

def custom_fun(nob):
    """Update the result."""

    operation = nob["first_tab"]["first_block"]["operand"]
    nb1 = nob["first_tab"]["first_block"]["number_1"]
    nb2 = nob["first_tab"]["first_block"]["number_2"]

    res = None
    if operation == "+":
        res = nb1 + nb2
    elif operation == "-":
        res = nb1 - nb2
    elif operation == "*":
        res = nb1 * nb2
    elif operation == "/":
        res = nb1 / nb2
    else:
        res = None

    nob["first_tab"]["first_block"]["result"] = res
    return nob

if __name__ == "__main__":
    process_tab(custom_fun)
```

Note that OpenTEA meomory is a classical nested object named here `nob`. The memory I/O can be done the usual Python way : `nob["first_tab"]["first_block"]["result"] = res`.
*We however encourage the use our nested object helper , available on PyPI, which gives a faster -an still pythonic- access to the nested object. The name of the package is, unsurprisigly [nob](https://pypi.org/project/nob/).*


Finally, the data recorded by the GUI is available as a YAML file, conforming to the SCHEMA Validation:

```yaml
first_tab:
  first_block:
    number_1: 32.0
    number_2: 10.0
    operand: +
    result: 42.0
```

# Command line

A small CLI makes available small tools for developpers. Only two tools are present now.
Call the CLI using `opentea3`:

```bash
Usage: opentea3 [OPTIONS] COMMAND [ARGS]...

  ---------------    O P E N T E A  III  --------------------

  You are now using the Command line interface of Opentea 3, a Python3
  Tkinter GUI engine based on SCHEMA specifications, created at CERFACS
  (https://cerfacs.fr).

  This is a python package currently installed in your python environement.
  See the full documentation at : https://opentea.readthedocs.io/en/latest/.

Options:
  --help  Show this message and exit.

Commands:
  test-gui     Examples of OpenTEA GUIs
  test-schema  Test if a yaml SCHEMA_FILE is valid for an opentea GUI.
```

# Acknowledgments

This work was funded, among many sources, by the CoE [Excellerat](https://www.excellerat.eu/wp/) and the National project [ICARUS](http://cerfacs.fr/coop/whatwedo/ourprojects/). Many thanks to the people from SAFRAN group for their feedback. 