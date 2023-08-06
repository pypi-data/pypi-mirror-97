# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['boozelib']
extras_require = \
{'dev': ['bump2version>=1.0.0,<2.0.0',
         'pre-commit>=2.3.0,<3.0.0',
         'towncrier>=19.2.0,<20.0.0'],
 'doc': ['sphinx-autobuild>=2020.9.1,<2021.0.0'],
 'test': ['nox>=2019.11.9,<2020.0.0']}

setup_kwargs = {
    'name': 'boozelib',
    'version': '0.7.0',
    'description': 'A Python module containing a couple of tools to calculate the blood alcohol content of people.\n',
    'long_description': '# boozelib\n\n**VERSION**: `0.7.0`\n\nA Python module containing a couple of tools to calculate the\n**blood alcohol content** of people.\n\nIt\'s at home at GitHub: <https://github.com/brutus/boozelib/>.\n\nAs a side note: I created this library mainly to have a very simple module to\ntry different Python testing and packaging best practice. _This is in no way a\nserious medical approach and also accepts a rather big level of abstraction._\nDepending on your use case, this might be okay; but I would not deem it fit for\nserious health and / or legal stuff 😉 🍻\n\n# Install\n\nYou can install it from [PyPi], it is known as `boozelib` and has no\ndependencies:\n\n```shell\npip install --user boozelib\n```\n\n# Usage\n\nThe two main functions are:\n\n-   `get_blood_alcohol_content(age, weight, height, sex, volume, percent)`\n\n    Return the **blood alcohol contents** raise (per mill) for a person after a\n    drink.\n\n    Given a drink containing _volume_ (ml) of _percent_ (vol/vol) alcohol, for a\n    person with _age_ (years), _weight_ (kg) and _height_ (cm) — using a\n    formular for "female body types" if _sex_ is true.\n\n-   `get_blood_alcohol_degradation(age, weight, height, sex, minutes=1, degradation=None)`\n\n    Return the **alcohol degradation** (per mill) for a person over _minutes_.\n\n    For a person with _age_ (years), _weight_ (kg) and _height_ (cm), using the\n    formular for "female body types" if _sex_ is true, over the given _minutes_.\n    If _degradation_ is not set, `ALCOHOL_DEGRADATION` is used as default.\n\nThis uses some constants and one variable you might want to review:\n\n-   `ALCOHOL_DEGRADATION`: the default value for alcohol degradation; meaning\n    the amount of alcohol (in gram) your body is degrading per minute, per\n    kilogram body weight. This is usually a value between `0.0017` and `0.0025`\n    (about 0.1—0.2 per thousand per hour).\n\n## Examples\n\nReturn the **blood alcohol contents** raise (per mill) for a person after a\ndrink:\n\n```python\nfrom boozelib import get_blood_alcohol_content\n\nget_blood_alcohol_content(\n\tage=32, weight=48, height=162, sex=True, volume=500, percent=4.9\n)\n# ⇒ 0.5480779730398769\n```\n\nAnd to calculate alcohol degradation:\n\n```python\nfrom boozelib import get_blood_alcohol_degradation\n\nget_blood_alcohol_degradation(\n\tage=32, weight=48, height=162, sex=True, minutes=60\n)\n# ⇒ 0.20133476560648536\n```\n\nYou can change the default for _alcohol degradation_ globally via setting\n`boozelib.ALCOHOL_DEGRADATION`. Or change the value for _alcohol degradation_\nper call:\n\n```python\nget_blood_alcohol_degradation(\n\tage=32, weight=48, height=162, sex=True, minutes=60, degradation=0.002\n)\n# ⇒ 0.16106781248518828\n```\n\n# Documentation\n\nSee the source or the [documentation] for more information and the used\n[formulas].\n\n# Development Setup\n\n[Poetry] is used to manage a _virtual environment_ for the development setup.\n\nA `Makefile` is provided, that collects some common tasks. You have to run\nthe following **once**, to setup your environment:\n\n```shell\nmake setup\n```\n\n# Testing\n\n[nox] is used as a test runner (with [ward] as the framework). If you have the\n_development environment_ activated, you can just run:\n\n```shell\nmake tests\n```\n\nIf something fails, please get in touch.\n\n# Thanks and Contributions\n\n-   Big hugs to Mathilda for hanging around and helping me figuring out all\n    that math and biology stuff.\n\nIf you find bugs, issues or anything else, please use the [issue tracker] on\nGitHub. Issues and PRs are welcome ❤️\n\n[documentation]: https://boozelib.readthedocs.org/\n[formulas]: https://boozelib.readthedocs.org/en/latest/background.html\n[issue tracker]: https://github.com/brutus/boozelib/issues\n[nox]: https://nox.thea.codes/\n[poetry]: https://python-poetry.org/\n[pypi]: https://pypi.org/project/BoozeLib/\n[ward]: https://wardpy.com/\n',
    'author': 'Brutus',
    'author_email': 'brutus.dmc@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/brutus/boozelib/',
    'package_dir': package_dir,
    'py_modules': modules,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
