common_wrangler
==============================
[![Actions Status](https://github.com/team-mayes/common_wrangler/workflows/PythonCI/badge.svg)](https://github.com/team-mayes/common_wrangler/actions)
[![PyPI version](https://badge.fury.io/py/common-wrangler.svg)](https://badge.fury.io/py/common-wrangler)
[![codecov](https://codecov.io/gh/team-mayes/common_wrangler/branch/master/graph/badge.svg)](https://codecov.io/gh/team-mayes/common_wrangler)

This package is available on [pypi](https://pypi.org/project/common-wrangler/), allowing it to be installed with
`pip install common_wrangler`.

Scripts for file and data manipulation, as well as common scripts used in this project as well as 
gaussian_wrangler, ligninkmc, and md_wrangler.

This package contains a common.py that is used in other packages from this developer, such as:
https://github.com/team-mayes/gaussian_wrangler

There are also several scripts that are useful in many scenarios:

*add2dict*: adds entries to a text file (one entry per line), ensuring that the output has no duplicates and is 
sorted. 

*fill_tpl*: set up so that a user can provide a configuration file with values for any parameters, and a 
corresponding template file that has parameter names in brackets. For example, the configuration file can 
have `project_name = common_wrangler` and the template would have `{project_name}` as a field to fill in.

*rename_files*: meant to be used in any terminal to rename any type of file.

Tested on CentOS release 6.10 and on Mojave 10.14.6.

### Copyright

Copyright (c) 2019, hmayes


#### Acknowledgements
 
Project based on the 
[Computational Chemistry Python Cookiecutter](https://github.com/choderalab/cookiecutter-python-comp-chem)
