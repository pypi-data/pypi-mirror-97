# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdbr']

package_data = \
{'': ['*']}

install_requires = \
['rich>=9.11.0,<10.0.0']

extras_require = \
{':extra == "ipython"': ['jedi==0.17.2'],
 'celery': ['celery>=4.4.7,<5.0.0'],
 'ipython': ['ipython==7.16']}

entry_points = \
{'console_scripts': ['pdbr = pdbr.pdbr_shell:cli']}

setup_kwargs = {
    'name': 'pdbr',
    'version': '0.4.1',
    'description': 'Pdb with Rich library.',
    'long_description': '# pdbr\n\n[![PyPI version](https://badge.fury.io/py/pdbr.svg)](https://pypi.org/project/pdbr/) [![Python Version](https://img.shields.io/pypi/pyversions/pdbr.svg)](https://pypi.org/project/pdbr/) [![](https://github.com/cansarigol/pdbr/workflows/Test/badge.svg)](https://github.com/cansarigol/pdbr/actions?query=workflow%3ATest)\n\npdbr is intended to make the PDB results more colorful. it uses [Rich](https://github.com/willmcgugan/rich) library to carry out that.\n\n\n## Installing\n\nInstall with `pip` or your favorite PyPi package manager.\n\n```\npip install pdbr\n```\n\n\n## Breakpoint\n\nIn order to use ```breakpoint()```, set **PYTHONBREAKPOINT** with "pdbr.set_trace"\n\n```python\nimport os\n\nos.environ["PYTHONBREAKPOINT"] = "pdbr.set_trace"\n```\n\nor just import pdbr\n\n```python\nimport pdbr\n```\n\n## New commands\n### vars(v)\nGet the local variables list as table.\n\n### varstree(vt)\nGet the local variables list as tree.\n\n### inspect(i) / inspectall(ia)\n[rich.inspect](https://rich.readthedocs.io/en/latest/introduction.html?s=03#rich-inspector)\n\n![](/images/image5.png)\n\n### pp\n[rich.pretty.pprint](https://rich.readthedocs.io/en/latest/reference/pretty.html?highlight=pprint#rich.pretty.pprint)\n\n### nn, uu, dd\nSame with n(ext), u(p), d(own) commands + with local variables.\n\n![](/images/image8.png)\n\n## Config\n### Style\nIn order to use Rich\'s traceback, style, and theme, set **setup.cfg**.\n\n```\n[pdbr]\nstyle = yellow\nuse_traceback = True\ntheme = friendly\n```\n\n### History\n**store_history** setting is used to keep and reload history, even the prompt is closed and opened again.\n```\n[pdbr]\n...\nstore_history=.pdbr_history\n```\n\n## Celery\nIn order to use **Celery** remote debugger with pdbr, use ```celery_set_trace``` as below sample. For more information see the [Celery user guide](https://docs.celeryproject.org/en/stable/userguide/debugging.html).\n\n```python\nfrom celery import Celery\n\napp = Celery(\'tasks\', broker=\'pyamqp://guest@localhost//\')\n\n@app.task\ndef add(x, y):\n    \n    import pdbr; pdbr.celery_set_trace()\n    \n    return x + y\n\n```\n\n![](/images/image6.png)\n\n\n## IPython \n\nBeing able to use [ipython](https://ipython.readthedocs.io/), install pdbr with it like below or just install your own version.\n\n```\npip install pdbr[ipython]\n```\n### Cli\n`pdbr` command in terminal start an `IPython` terminal app instance. Unlike default `TerminalInteractiveShell`, the new shell uses pdbr as debugger class instead of `ipdb`.\n#### %debug magic sample\n![](/images/image9.png)\n### Terminal\n#### Django shell sample\n![](/images/image7.png)\n\n## Vscode user snippet\n\nTo create or edit your own snippets, select **User Snippets** under **File > Preferences** (**Code > Preferences** on macOS), and then select **python.json**. \n\nPlace the below snippet in json file for **pdbr**.\n\n```\n{\n  ...\n  "pdbr": {\n        "prefix": "pdbr",\n        "body": "import pdbr; pdbr.set_trace()",\n        "description": "Code snippet for pdbr debug"\n    },\n}\n```\n\nFor **Celery** debug.\n\n```\n{\n  ...\n  "rdbr": {\n        "prefix": "rdbr",\n        "body": "import pdbr; pdbr.celery_set_trace()",\n        "description": "Code snippet for Celery pdbr debug"\n    },\n}\n```\n\n## Samples\n![](/images/image1.png)\n\n![](/images/image3.png)\n\n![](/images/image4.png)\n\n### Traceback\n![](/images/image2.png)\n',
    'author': 'Can Sarigol',
    'author_email': 'ertugrulsarigol@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cansarigol/pdbr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
