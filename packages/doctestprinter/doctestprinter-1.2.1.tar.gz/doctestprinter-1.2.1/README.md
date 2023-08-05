# doctestprinter
[![Coverage Status](https://coveralls.io/repos/gitlab/david.scheliga/doctestprinter/badge.svg?branch=master)](https://coveralls.io/gitlab/david.scheliga/doctestprinter?branch=master)
[![Build Status](https://travis-ci.com/david.scheliga/doctestprinter.svg?branch=master)](https://travis-ci.com/david.scheliga/doctestprinter)
[![PyPi](https://img.shields.io/pypi/v/doctestprinter.svg?style=flat-square&label=PyPI)](https://https://pypi.org/project/doctestprinter/)
[![Python Versions](https://img.shields.io/pypi/pyversions/doctestprinter.svg?style=flat-square&label=PyPI)](https://https://pypi.org/project/doctestprinter/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/doctestprinter/badge/?version=latest)](https://doctestprinter.readthedocs.io/en/latest/?badge=latest)

**doctestprinter** contains convenience functions to print outputs more adequate
for doctests.

![doctestprinter icon](https://doctestprinter.readthedocs.io/en/latest/_images/doctestprinter-icon.svg "A doctest printer")

Example features:

- removes trailing whitespaces: pandas.DataFrame generates trailing whitespaces,
  which interferes with auto text 'trailing whitespace' removal features,
  leading to failed tests.
- maximum line width: break long sequences at whitespaces to a paragraph.

## Installation

Installing the latest release using pip is recommended.

```` shell script
    $ pip install doctestprinter
````

The latest development state can be obtained from gitlab using pip.

```` shell script
    $ pip install git+https://gitlab.com/david.scheliga/doctestprinter.git@dev
````


## Basic Usage

The default method is `doctestprinter.doctest_print`.

```` python

    >>> from doctestprinter import doctest_print
    >>> sample_object = list(range(80))
    >>> doctest_print(sample_object, max_line_width=70)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
    20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
    38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
    56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73,
    74, 75, 76, 77, 78, 79]

````

[Read-the-docs](https://doctestprinter.readthedocs.io/en/latest/) for further
 functionality.

## Contribution

Any contribution by reporting a bug or desired changes are welcomed. The preferred 
way is to create an issue on the gitlab's project page, to keep track of everything 
regarding this project.

### Contribution of Source Code
#### Code style
This project follows the recommendations of [PEP8](https://www.python.org/dev/peps/pep-0008/).
The project is using [black](https://github.com/psf/black) as the code formatter.

#### Workflow

1. Fork the project on Gitlab.
2. Commit changes to your own branch.
3. Submit a **pull request** from your fork's branch to our branch *'dev'*.

## Authors

* **David Scheliga** 
    [@gitlab](https://gitlab.com/david.scheliga)
    [@Linkedin](https://www.linkedin.com/in/david-scheliga-576984171/)
    - Initial work
    - Maintainer

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the
[LICENSE](LICENSE) file for details

## Acknowledge

[Code style: black](https://github.com/psf/black)