# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iambic',
 'iambic.ast',
 'iambic.bin',
 'iambic.parse',
 'iambic.plays',
 'iambic.render']

package_data = \
{'': ['*'],
 'iambic.plays': ['comedies/*',
                  'histories/*',
                  'problems/*',
                  'roman/*',
                  'romances/*',
                  'tragedies/*']}

install_requires = \
['html2text>=2020.1.16,<2021.0.0',
 'markdown>=3.2.2,<4.0.0',
 'pymdown-extensions>=7.1,<8.0',
 'tabulate>=0.8.9,<0.9.0',
 'typical>=2.1,<3.0',
 'ujson>=2.0,<3.0']

setup_kwargs = {
    'name': 'iambic',
    'version': '2.4.2',
    'description': 'Data extraction and rendering library for Shakespearean text.',
    'long_description': "iambic: Data extraction and rendering library for Shakespearean text. :scroll: \n==============================================================================\n[![image](https://img.shields.io/pypi/v/iambic.svg)](https://pypi.org/project/iambic/)\n[![image](https://img.shields.io/pypi/l/iambic.svg)](https://pypi.org/project/iambic/)\n[![image](https://img.shields.io/pypi/pyversions/iambic.svg)](https://pypi.org/project/iambic/)\n[![image](https://img.shields.io/github/languages/code-size/seandstewart/iambic.svg?style=flat)](https://github.com/seandstewart/iambic)\n[![image](https://img.shields.io/travis/seandstewart/iambic.svg)](https://travis-ci.org/seandstewart/iambic)\n[![codecov](https://codecov.io/gh/seandstewart/iambic/branch/master/graph/badge.svg)](https://codecov.io/gh/seandstewart/iambic)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Netlify Status](https://api.netlify.com/api/v1/badges/91ace14b-e26e-4026-ac5c-3e5640f2910f/deploy-status)](https://app.netlify.com/sites/iambic/deploys)\n\nLet computers do the hard work for you! `iambic` provides:\n1. The most accurate method for counting lines automatically.\n2. Automatically track which characters are speaking in any scene.\n3. Deterministic, repeatable results, with the ability to store your\n   data as JSON with strictly defined schema for passing over the wire\n   or storing locally or in a NoSQL database between runtimes.\n\n\n## Installation\n\nIn order to install the latest version, simply `pip3 install\n-U iambic`.\n\nThis library requires Python 3.7 or greater.\n\n\n## What is it?\n`iambic` was originally envisioned as a tool for translating\nShakespearean text into actionable information, i.e.:\n1. How many lines are in this particular play?\n2. How many lines does a given character speak in this play?\n3. Which characters speak, in which scenes and acts?\n\nAs a result of the implementation, this tool can be applied \nto any body of text which adhere's to its parsing syntax.\n\n\n## The Schema\nThe full schema specification has been written in JSON\nSchema 7.0 and can be found\n[here](schema.json)\n\n## Documentation\n\nThe full documentation is available at\n[iambic.seandstewart.io](https://iambic.seandstewart.io)\n\n\n## How to Contribute\n1.  Check for open issues or open a fresh issue to start a \n    discussion around a feature idea or a bug.\n2.  Create a branch on Github for your issue or fork\n    [the repository](https://github.com/seandstewart/iambic)\n    on GitHub to start making your changes to the **master**\n    branch.\n3.  Write a test which shows that the bug was fixed or that \n    the feature works as expected.\n4.  Send a pull request and bug the maintainer until it gets\n     merged and published. :)\n",
    'author': 'Sean Stewart',
    'author_email': 'sean_stewart@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/seandstewart/iambic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
