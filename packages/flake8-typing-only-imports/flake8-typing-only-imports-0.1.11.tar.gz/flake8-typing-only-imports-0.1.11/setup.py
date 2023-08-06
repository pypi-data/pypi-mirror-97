# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_typing_only_imports']

package_data = \
{'': ['*']}

entry_points = \
{'flake8.extension': ['TYO = flake8_typing_only_imports:Plugin']}

setup_kwargs = {
    'name': 'flake8-typing-only-imports',
    'version': '0.1.11',
    'description': 'A flake8 plugin that flags imports exclusively used for type annotations',
    'long_description': '<a href="https://pypi.org/project/flake8-typing-only-imports/">\n    <img src="https://img.shields.io/pypi/v/flake8-typing-only-imports.svg" alt="Package version">\n</a>\n<a href="https://codecov.io/gh/sondrelg/flake8-typing-only-imports">\n    <img src="https://codecov.io/gh/sondrelg/flake8-typing-only-imports/branch/master/graph/badge.svg" alt="Code coverage">\n</a>\n<a href="https://pypi.org/project/flake8-typing-only-imports/">\n    <img src="https://github.com/sondrelg/flake8-typing-only-imports/actions/workflows/testing.yml/badge.svg" alt="Test status">\n</a>\n<a href="https://pypi.org/project/flake8-typing-only-imports/">\n    <img src="https://img.shields.io/badge/python-3.7%2B-blue" alt="Supported Python versions">\n</a>\n<a href="http://mypy-lang.org/">\n    <img src="http://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy">\n</a>\n\n# flake8-typing-only-imports\n\n>Plugin is still a work in progress\n\nflake8 plugin that helps identify which imports to put into type-checking blocks,\nand how to adjust your type annotations once imports are moved.\n\n## Installation\n\n```shell\npip install flake8-typing-only-imports\n```\n\n## Codes\n\n| Code   | Description                                         |\n|--------|-----------------------------------------------------|\n| TYO100 | Import should be moved to a type-checking block  |\n| TYO101 | Third-party import should be moved to a type-checking block |\n| TYO200 | Missing \'from \\_\\_future\\_\\_ import annotations\' import |\n| TYO201 | Annotation is wrapped in unnecessary quotes |\n| TYO300 | Annotation should be wrapped in quotes |\n| TYO301 | Annotation is wrapped in unnecessary quotes |\n\n`TYO101` is disabled by default because third-party imports usually\naren\'t a real concern with respect to import circularity issues.\n\n`TYO2XX` and `TYO3XX` are mutually exclusive as they represent\ntwo different ways of solving the same problem. Make sure to ignore or enable just one of the series.\n\n## Motivation\n\nTwo common issues when annotating large code bases are:\n\n1. Import circularity issues\n2. Annotating not-yet-defined structures\n\nThese problems are largely solved by two features:\n\n1. Type checking blocks\n\n    ```python\n    from typing import TYPE_CHECKING\n\n    if TYPE_CHECKING:\n        # this code is not evaluated at runtime\n        from foo import bar\n    ```\n2. Forward references\n    <br><br>\n    Which can be used, like this\n    ```python\n    class Foo:\n        def bar(self) -> \'Foo\':\n            return Foo()\n    ```\n\n    or since [PEP563](https://www.python.org/dev/peps/pep-0563/#abstract) was implemented, like this:\n    ```python\n    from __future__ import annotations\n\n    class Foo:\n        def bar(self) -> Foo:\n            return Foo()\n    ```\n\n   See [this](https://stackoverflow.com/questions/55320236/does-python-evaluate-type-hinting-of-a-forward-reference) excellent stackoverflow response explaining forward references, for more context.\n\nThe aim of this plugin is to automate the management of type annotation imports,\nand the forward references that then become necessary.\n\n\n## As a pre-commit hook\n\nSee [pre-commit](https://github.com/pre-commit/pre-commit) for instructions\n\nSample `.pre-commit-config.yaml`:\n\n```yaml\n- repo: https://gitlab.com/pycqa/flake8\n  rev: 3.7.8\n  hooks:\n  - id: flake8\n    additional_dependencies: [flake8-typing-only-imports]\n```\n\n## Supporting the project\n\nLeave a&nbsp;⭐️&nbsp; if this project helped you!\n\nContributions are always welcome 👏\n',
    'author': 'Sondre Lillebø Gundersen',
    'author_email': 'sondrelg@live.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sondrelg/flake8-typing-only-imports',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
