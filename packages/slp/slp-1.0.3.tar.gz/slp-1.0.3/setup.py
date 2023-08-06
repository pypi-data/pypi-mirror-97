# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slp', 'slp.config', 'slp.data', 'slp.modules', 'slp.plbind', 'slp.util']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'loguru>=0.5.3,<0.6.0',
 'nltk>=3.5,<4.0',
 'numpy>=1.20.1,<2.0.0',
 'omegaconf>=2.0.6,<3.0.0',
 'pytorch-ignite==0.2.0',
 'pytorch-lightning>=1.2.0,<2.0.0',
 'pytorch-nlp==0.4.1',
 'requests>=2.25.1,<3.0.0',
 'rpdb>=0.1.6,<0.2.0',
 'scikit-learn>=0.24.1,<0.25.0',
 'scipy>=1.6.1,<2.0.0',
 'sentencepiece>=0.1.95,<0.2.0',
 'spacy>=3.0.3,<4.0.0',
 'toml>=0.10.2,<0.11.0',
 'toolz>=0.11.1,<0.12.0',
 'torch>=1.7.1,<2.0.0',
 'torchvision>=0.8.2,<0.9.0',
 'tqdm>=4.57.0,<5.0.0',
 'transformers==4.3.0',
 'ujson>=4.0.2,<5.0.0',
 'validators>=0.18.2,<0.19.0',
 'wandb>=0.10.20,<0.11.0']

setup_kwargs = {
    'name': 'slp',
    'version': '1.0.3',
    'description': 'Speech, Language and Multimodal Processing models and utilities in PyTorch',
    'long_description': '# slp\n\n<p align="center">\n    <img src="https://github.com/georgepar/slp/actions/workflows/ci.yml/badge.svg" />\n    <a href="https://codeclimate.com/github/georgepar/slp/maintainability" alt="Maintainability">\n        <img src="https://api.codeclimate.com/v1/badges/d3ad9729ad30aa158737/maintainability" /></a>\n    <a href="https://choosealicense.com/licenses/mit/" alt="License: MIT">\n        <img src="https://img.shields.io/badge/license-MIT-green.svg" /></a>\n    <a href="https://img.shields.io/pypi/pyversions/slp">\n        <img alt="Python Version" src="https://img.shields.io/pypi/pyversions/slp" /></a>\n    <a href="https://black.readthedocs.io/en/stable/" alt="Code Style: Black">\n        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>\n</p>\n\n* **Repo:** [https://github.com/georgepar/slp](https://github.com/georgepar/slp)\n* **Documentation:** [https://georgepar.github.io/slp/](https://georgepar.github.io/slp/)\n\n\nslp is a framework for fast and reproducible development of multimodal models, with emphasis on\nNLP models.\n\nIt started as a collection of scripts and code I wrote / collected during my PhD and it evolves\naccordingly.\n\nAs such, the framework is opinionated and it follows a convention over configuration approach.\n\nA heavy emphasis is put on:\n\n- Enforcing best practices and reproducibility of experiments\n- Making common things fast at the top-level and not having to go through extensive configuration options\n- Remaining extendable. Extensions and modules for more use cases should be easy to add\n- Out of the box extensive logging and experiment management\n- Separating dirty / scratch code (at the script level) for quick changes and clean / polished code at the library level\n\nThis is currently in alpha release under active development, so things may break and new features\nwill be added.\n\n## Dependencies\n\nWe use [Pytorch](https://pytorch.org/) (1.7) and the following libraries\n\n- [Pytorch Lightning](https://pytorch-lightning.readthedocs.io/en/stable/)\n- [huggingface/transformers](https://huggingface.co/transformers/)\n- [Wandb](https://wandb.ai/)\n- Python 3.8\n\n## Installation\n\nYou can use slp as an external library by installing from PyPI with\n\n```\npip install slp\n```\n\nOr you can clone it from github\n\n```\ngit clone git@github.com:georgepar/slp\n```\n\nWe use [poetry](https://python-poetry.org/) for dependency management\n\nWhen you clone the repo run:\n\n```bash\npip install poetry\npoetry install\n```\n\nand a clean environment with all the dependencies will be created.\nYou can access it with `poetry shell`.\n\n**Note**: Wandb logging is enabled by default. You can either\n\n- Create an account and run `wandb login` when you clone the repo in a new machine to store the results in the online managed environment\n- Run `wandb offline` when you clone the repo to disable remote sync\n- Use one of their self-hosted solutions\n\n\n## Contributing\n\nYou are welcome to open issues / PRs with improvements and bug fixes.\n\nSince this is mostly a personal project based around workflows and practices that work for me, I don\'t guarantee I will accept every change, but I\'m always open to discussion.\n\nIf you are going to contribute, please use the pre-commit hooks under `hooks`, otherwise the PR will not go through the CI. And never, ever touch `requirements.txt` by hand, it will automatically be exported from `poetry`\n\n```bash\n\ncat <<EOT >> .git/hooks/pre-commit\n#!/usr/bin/env bash\n\nbash hooks/black-check\nbash hooks/export-requirements-txt\nbash hooks/checks\nEOT\n\nchmod +x .git/hooks/pre-commit\n```\n\n## Cite\n\nIf you use this code for your research, please include the following citation\n\n```\n@ONLINE {,\n    author = "Georgios Paraskevopoulos",\n    title  = "slp",\n    year   = "2020",\n    url    = "https://github.com/georgepar/slp"\n}\n```\n\n\n## Roadmap\n\n* Optuna integration for hyperparameter tuning\n* Add dataloaders for popular multimodal datasets\n* Add multimodal architectures\n* Add RIM, DNC and Kanerva machine implementations\n* Create cookiecutter template for new project scaffolding\n* Write unit tests\n',
    'author': 'Giorgos Paraskevopoulos',
    'author_email': 'geopar@central.ntua.gr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://georgepar.github.io/slp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
