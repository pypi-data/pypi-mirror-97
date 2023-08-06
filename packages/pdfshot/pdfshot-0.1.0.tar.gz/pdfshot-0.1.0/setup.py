# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdfshot']

package_data = \
{'': ['*']}

install_requires = \
['pdf2image>=1.14.0,<2.0.0', 'typer[all]>=0.3.2,<0.4.0', 'yaspin>=1.4.1,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['pdfshot = pdfshot.console:app']}

setup_kwargs = {
    'name': 'pdfshot',
    'version': '0.1.0',
    'description': 'A Python CLI to export pages from PDF files as images.',
    'long_description': '# pdfshot\n\nA Python CLI to export pages from PDF files as images.\n\n## Quickstart\n\n- Install [poppler](http://macappstore.org/poppler/) (macOS): `brew install poppler`.\n\n**Usage**:\n\n```console\n$ pdfshot [OPTIONS] INPUT_PATH PDF_PAGE\n```\n\n**Arguments**:\n\n* `INPUT_PATH`: The input PDF file.  [required]\n* `PDF_PAGE`: The page number of the PDF file to export as an image.Page numbering starts at 1 (1-based indexing).  [required]\n\n**Options**:\n\n* `--version`: Show the version and exit.\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n## Notes\n\n- [pdf2image](https://github.com/Belval/pdf2image):\n  - To **only convert** PDF files to images.\n- Commands:\n  - `poetry init` + `poetry install`.\n  - `poetry add "typer[all]"`.\n  - `which pdfshot`.\n- [Typer](https://github.com/tiangolo/typer):\n  - CLI arguments (_required_ by default): CLI parameters (`./myproject`, for example) passed in some specific order to the CLI application (`ls`, for example).\n  - CLI options (_optional_ by default): _CLI parameters_ (`--size`, for example) passed to the CLI application with a specific name.\n  - [Data validation](https://typer.tiangolo.com/tutorial/options/callback-and-context/).\n  - [Numeric validation](https://typer.tiangolo.com/tutorial/parameter-types/number/).\n  - For commands, think of `git` (`git push`, `git clone`, etc.).\n- [Poetry](https://python-poetry.org/):\n  - [Outdated metadata after version bump for local package](https://github.com/python-poetry/poetry/issues/3289) (open) issue.\n\n## References\n\n- [Building a Package](https://typer.tiangolo.com/tutorial/package/).\n- [Version CLI Option, is_eager](https://typer.tiangolo.com/tutorial/options/version/).\n',
    'author': 'João Palmeiro',
    'author_email': 'joaommpalmeiro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
