# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wap', 'wap.commands']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.17.0,<0.18.0',
 'attrs>=20.3.0,<21.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'requests>=2.25.1,<3.0.0',
 'strictyaml>=1.3.2,<2.0.0']

entry_points = \
{'console_scripts': ['wap = wap.__main__:main']}

setup_kwargs = {
    'name': 'wow-addon-packager',
    'version': '0.8.1',
    'description': 'A developer-friendly World of Warcraft addon packager',
    'long_description': 'wap (WoW Addon Packager)\n========================\n\n.. teaser-begin\n\n.. image:: https://github.com/t-mart/wap/actions/workflows/ci.yml/badge.svg?branch=master\n   :target: https://github.com/t-mart/wap/actions/workflows/ci.yml\n   :alt: GitHub Actions status for master branch\n\n.. image:: https://codecov.io/gh/t-mart/wap/branch/master/graph/badge.svg?token=AVOA4QWTBL\n   :target: https://codecov.io/gh/t-mart/wap\n   :alt: Code Coverage on codecov.io\n\n.. image:: https://img.shields.io/pypi/v/wow-addon-packager\n   :target: https://pypi.org/project/wow-addon-packager/\n   :alt: Latest release on PyPI\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Code styled with black\n\n.. image:: https://img.shields.io/github/license/t-mart/wap\n   :target: https://github.com/t-mart/wap/blob/master/LICENSE\n   :alt: MIT licensed\n\n.. image:: https://readthedocs.org/projects/wow-addon-packager/badge/?version=latest\n   :target: https://wow-addon-packager.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n|\n\n``wap`` is a developer-friendly World of Warcraft addon packager.\n\n.. image:: https://raw.githubusercontent.com/t-mart/wap/master/docs/_static/images/demo.gif\n   :alt: wap demo\n\nFeatures\n--------\n\n- Packages retail or classic WoW addons (or both!)\n- Uploads your addons to CurseForge\n- Automatically installs your addons to your AddOns folder when a file changes in your project\n- Generates valid TOC files automagically\n- Sets up new addon projects quickly, ready to go with one command\n- Consolidates all configuration in one easy-to-edit file\n- Supports and is tested on Windows, macOS, and Linux\n- Has awesome `documentation`_\n\n.. _`documentation`: https://wow-addon-packager.readthedocs.io/en/stable\n\n.. teaser-end\n\n\n``wap`` in 5 minutes\n--------------------\n\n.. five-minutes-begin\n\nThis entire set of instructions is runnable without editing a single line of code!\n\n1. `Download Python 3.9 or greater`_ and install it.\n\n2. Install ``wap`` with pip:\n\n   .. code-block:: console\n\n      $ pip install --upgrade --user wow-addon-packager\n\n3. Create a new project:\n\n   .. code-block:: console\n\n      $ wap quickstart MyAddon  # or whatever name you\'d like!\n\n   and answer the prompted questions. Don\'t worry too much about your answers -- you can\n   always change them later in your configuration file.\n\n   Then change to your new project\'s directory\n\n   .. code-block:: console\n\n      $ cd "MyAddon"\n\n4. Package your addon\n\n   .. code-block:: console\n\n      $ wap package\n\n5. Install your addon so you can test it out in your local WoW installation:\n\n   Windows\n      .. code-block:: console\n\n         $ wap dev-install --wow-addons-path "C:\\Program Files (x86)\\World of Warcraft\\_retail_\\Interface\\AddOns"\n\n   macOS\n      .. code-block:: console\n\n         $ wap dev-install --wow-addons-path "/Applications/World of Warcraft/_retail_/Interface/AddOns"\n\n   .. note::\n\n      Also check out the ``watch`` command for automatic repackage and re-dev-installation!\n\n6. Upload your project to CurseForge\n\n   .. code-block:: console\n\n      $ wap upload --addon-version "dev" --curseforge-token "<your-token>"\n\n   You can generate a new token at Curseforge\'s `My API Tokens`_ page.\n\n.. _`My API Tokens`: https://authors.curseforge.com/account/api-tokens\n.. _`Download Python 3.9 or greater`: https://www.python.org/downloads/\n\n.. five-minutes-end\n\n\nFurther Help\n------------\n\nSee the `official documentation site`_. There\'s a lot more information there!\n\nAlso, the ``wap`` command is fully documented in its help text. View it with:\n\n.. code-block:: console\n\n   $ wap --help\n   $ wap build --help\n   $ wap upload --help\n   ... etc\n\n.. badge-begin\n\nBadge\n-----\n\nIf you\'d like to show others in your documentation that you are using ``wap`` to package\nyour addon, you can include the following official badge (hosted by https://shields.io/):\n\n.. image:: https://img.shields.io/badge/packaged%20by-wap-d33682\n   :target: https://github.com/t-mart/wap\n   :alt: Packaged by wap\n\nMarkdown\n   .. code-block:: markdown\n\n      [![Packaged by wap](https://img.shields.io/badge/packaged%20by-wap-d33682)](https://github.com/t-mart/wap)\n\nreStructuredText\n   .. code-block:: rst\n\n      .. image:: https://img.shields.io/badge/packaged%20by-wap-d33682\n         :target: https://github.com/t-mart/wap\n         :alt: Packaged by wap\n\n.. badge-end\n\nContributing\n------------\n\nSee `how to contribute`_ in the official docs.\n\nTODOs\n-----\n\n- localization via curseforge?\n- Dockerfile github action `<https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action>`_\n\n.. _`how to contribute`: https://wow-addon-packager.readthedocs.io/en/stable/contributing.html\n.. _`official documentation site`: https://wow-addon-packager.readthedocs.io/en/stable\n\nCopyright (c) 2021 Tim Martin\n',
    'author': 'Tim Martin',
    'author_email': 'tim@timmart.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/t-mart/wap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
