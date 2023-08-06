# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacy_syllables']

package_data = \
{'': ['*']}

install_requires = \
['pyphen>=0.10.0,<0.11.0', 'spacy>=3.0.3,<4.0.0']

setup_kwargs = {
    'name': 'spacy-syllables',
    'version': '3.0.1',
    'description': 'Multilingual syllable annotation pipeline component for spacy',
    'long_description': '![spacy syllables](https://raw.githubusercontent.com/sloev/spacy-syllables/master/header.jpg)\n\n# Spacy Syllables\n\n[![Build Status](https://travis-ci.com/sloev/spacy-syllables.svg?branch=master)](https://travis-ci.com/sloev/spacy-syllables) [![Latest Version](https://img.shields.io/pypi/v/spacy-syllables.svg)](https://pypi.python.org/pypi/spacy-syllables) [![Python Support](https://img.shields.io/pypi/pyversions/spacy-syllables.svg)](https://pypi.python.org/pypi/spacy-syllables)\n\n<a href="https://www.buymeacoffee.com/sloev" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-pink.png" alt="Buy Me A Coffee" height="51px" width="217px"></a>\n\nA [spacy 2+ pipeline component](https://spacy.io/universe/category/pipeline) for adding multilingual syllable annotation to tokens. \n\n* Uses well established [pyphen](https://github.com/Kozea/Pyphen) for the syllables.\n* Supports [a ton of languages](https://github.com/Kozea/Pyphen/tree/master/pyphen/dictionaries)\n* Ease of use thx to the awesome pipeline framework in spacy\n\n## Install\n\n```bash\n$ pip install spacy_syllables\n```\n\nwhich also installs the following dependencies:\n\n* spacy = "^2.2.3"\n* pyphen = "^0.9.5"\n\n## Usage\n\nThe [`SpacySyllables`](spacy_syllables/__init__.py) class autodetects language from the given spacy nlp instance, but you can also override the detected language by specifying the `lang` parameter during instantiation, see how [here](tests/test_all.py).\n\n### Normal usecase\n\n```python\n\nimport spacy\nfrom spacy_syllables import SpacySyllables\n\nnlp = spacy.load("en_core_web_sm")\n\nnlp.add_pipe("syllables", after="tagger")\n\nassert nlp.pipe_names == ["tok2vec", "tagger", "syllables", "parser", "ner", "attribute_ruler", "lemmatizer"]\n\ndoc = nlp("terribly long")\n\ndata = [(token.text, token._.syllables, token._.syllables_count) for token in doc]\n\nassert data == [("terribly", ["ter", "ri", "bly"], 3), ("long", ["long"], 1)]\n\n```\n\nmore examples in [tests](tests/test_all.py)\n\n## Migrating from spacy 2.x to 3.0\n\nIn spacy 2.x, spacy_syllables was originally added to the pipeline by instantiating a [`SpacySyllables`](spacy_syllables/__init__.py) object with the desired options and adding it to the pipeline: \n\n```python\nfrom spacy_syllables import SpacySyllables\n\nsyllables = SpacySyllables(nlp, "en_US")\n\nnlp.add_pipe(syllables, after="tagger")\n```\n\nIn spacy 3.0, you now add the component to the pipeline simply by adding it by name, setting custom configuration information in the `add_pipe()` parameters:\n```python\nfrom spacy_syllables import SpacySyllables\n\nnlp.add_pipe("syllables", after="tagger", config={"lang": "en_US"})\n```\n\n\n\nIn addition, the default pipeline components have changed between 2.x and 3.0; please make sure to update any asserts you have that check for these.\ne.g.:\n\nspacy 2.x:\n```python\nassert nlp.pipe_names == ["tagger", "syllables", "parser", "ner"]\n```\n\nspacy 3.0:\n```python\nassert nlp.pipe_names == ["tok2vec", "tagger", "syllables", "parser", "ner", "attribute_ruler", "lemmatizer"]\n```\n\n## Dev setup / testing\n\nwe are using\n* [poetry](https://python-poetry.org/) for the package\n* [nox](https://github.com/theacodes/nox) for the tests\n* [pyenv](https://github.com/pyenv/pyenv) for specifying python versions for nox tests\n\n### install\n\n* [install pyenv](https://github.com/pyenv/pyenv#installation)\n* [install poetry](https://python-poetry.org/docs/#installation)\n\nthen install the dev package and pyenv versions\n\n```bash\n$ poetry install\n$ poetry run nox --session install_pyenv_versions\n```\n\n### run tests\n\n```bash\n$ poetry run nox\n```\n',
    'author': 'sloev',
    'author_email': 'johannes.valbjorn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sloev/spacy-syllables',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
