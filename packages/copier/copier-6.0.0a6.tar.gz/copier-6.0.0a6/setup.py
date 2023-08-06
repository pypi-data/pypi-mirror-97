# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['copier']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.7.1,<3.0.0',
 'colorama>=0.4.3,<0.5.0',
 'iteration_utilities>=0.10.1,<0.11.0',
 'jinja2>=2.11.2,<3.0.0',
 'packaging>=20.4,<21.0',
 'pathspec>=0.8.0,<0.9.0',
 'plumbum>=1.6.9,<2.0.0',
 'pydantic>=1.7.2,<2.0.0',
 'pyyaml-include>=1.2,<2.0',
 'pyyaml>=5.3.1,<6.0.0',
 'questionary>=1.8.1,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['backports.cached-property>=1.0.0,<2.0.0',
                             'importlib-metadata>=3.4.0,<4.0.0',
                             'typing-extensions>=3.7.4,<4.0.0'],
 'docs': ['mkdocs-material>=5.5.2,<6.0.0',
          'mkdocs-mermaid2-plugin>=0.5.0,<0.6.0',
          'mkdocstrings>=0.15.0,<0.16.0']}

entry_points = \
{'console_scripts': ['copier = copier.cli:CopierApp.run']}

setup_kwargs = {
    'name': 'copier',
    'version': '6.0.0a6',
    'description': 'A library for rendering project templates.',
    'long_description': '# ![Copier](https://github.com/copier-org/copier/raw/master/img/copier-logotype.png)\n\n[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/copier-org/copier)\n[![codecov](https://codecov.io/gh/copier-org/copier/branch/master/graph/badge.svg)](https://codecov.io/gh/copier-org/copier)\n[![CI](https://github.com/copier-org/copier/workflows/CI/badge.svg)](https://github.com/copier-org/copier/actions?query=branch%3Amaster)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n![](https://img.shields.io/pypi/pyversions/copier)\n![](https://img.shields.io/pypi/v/copier)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Documentation Status](https://readthedocs.org/projects/copier/badge/?version=latest)](https://copier.readthedocs.io/en/latest/?badge=latest)\n\nA library for rendering project templates.\n\n-   Works with **local** paths and **git URLs**.\n-   Your project can include any file and `Copier` can dynamically replace values in any\n    kind of text file.\n-   It generates a beautiful output and takes care of not overwrite existing files\n    unless instructed to do so.\n\n![Sample output](https://github.com/copier-org/copier/raw/master/img/copier-output.png)\n\n## Installation\n\n1. Install Python 3.6.1 or newer (3.8 or newer if you\'re on Windows).\n1. Install Git 2.24 or newer.\n1. To use as a CLI app: `pipx install copier`\n1. To use as a library: `pip install copier`\n\n## Quick usage\n\n-   Use it in your Python code:\n\n    ```python\n    from copier import copy\n\n    # Create a project from a local path\n    copy("path/to/project/template", "path/to/destination")\n\n    # Or from a git URL.\n    copy("https://github.com/copier-org/copier.git", "path/to/destination")\n\n    # You can also use "gh:" as a shortcut of "https://github.com/"\n    copy("gh:copier-org/copier.git", "path/to/destination")\n\n    # Or "gl:" as a shortcut of "https://gitlab.com/"\n    copy("gl:copier-org/copier.git", "path/to/destination")\n    ```\n\n-   Or as a command-line tool:\n\n    ```bash\n    copier path/to/project/template path/to/destination\n    ```\n\n## Browse or tag public templates\n\nYou can browse public copier templates in GitHub using\n[the `copier-template` topic](https://github.com/topics/copier-template). Use them as\ninspiration!\n\nIf you want your template to appear in that list, just add the topic to it! 🏷\n\n## Credits\n\nSpecial thanks go to [jpscaletti](https://github.com/jpscaletti) for originally creating\n`Copier`. This project would not be a thing without him.\n\nMany thanks to [pykong](https://github.com/pykong) who took over maintainership on the\nproject, promoted it, and laid out the bases of what the project is today.\n\nBig thanks also go to [Yajo](https://github.com/Yajo) for his relentless zest for\nimproving `Copier` even further.\n\nThanks a lot, [pawamoy](https://github.com/pawamoy) for polishing very important rough\nedges and improving the documentation and UX a lot.\n',
    'author': 'Ben Felder',
    'author_email': 'ben@felder.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pykong/copier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
