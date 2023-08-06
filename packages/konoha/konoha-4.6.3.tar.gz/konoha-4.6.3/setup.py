# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['konoha',
 'konoha.api',
 'konoha.data',
 'konoha.integrations',
 'konoha.word_tokenizers']

package_data = \
{'': ['*']}

install_requires = \
['overrides>=3.0.0,<4.0.0']

extras_require = \
{'all': ['janome>=0.3.10,<0.4.0',
         'natto-py>=0.9.0,<0.10.0',
         'kytea>=0.1.4,<0.2.0',
         'sentencepiece>=0.1.85,<0.2.0',
         'sudachipy==0.4.9',
         'boto3>=1.11.0,<2.0.0',
         'fastapi>=0.54.1,<0.55.0',
         'uvicorn>=0.11.5,<0.12.0',
         'sudachidict-core>=20200330,<20200331',
         'nagisa>=0.2.7,<0.3.0'],
 'all_with_integrations': ['janome>=0.3.10,<0.4.0',
                           'natto-py>=0.9.0,<0.10.0',
                           'kytea>=0.1.4,<0.2.0',
                           'sentencepiece>=0.1.85,<0.2.0',
                           'sudachipy==0.4.9',
                           'boto3>=1.11.0,<2.0.0',
                           'allennlp>=1.3.0,<2.0.0',
                           'fastapi>=0.54.1,<0.55.0',
                           'uvicorn>=0.11.5,<0.12.0',
                           'sudachidict-core>=20200330,<20200331',
                           'nagisa>=0.2.7,<0.3.0'],
 'allennlp': ['allennlp>=1.3.0,<2.0.0'],
 'docs': ['sphinx>=3.1.1,<4.0.0', 'sphinx_rtd_theme>=0.4.3,<0.5.0'],
 'janome': ['janome>=0.3.10,<0.4.0'],
 'kytea': ['kytea>=0.1.4,<0.2.0'],
 'mecab': ['natto-py>=0.9.0,<0.10.0'],
 'nagisa': ['nagisa>=0.2.7,<0.3.0'],
 'remote': ['boto3>=1.11.0,<2.0.0'],
 'sentencepiece': ['sentencepiece>=0.1.85,<0.2.0'],
 'server': ['fastapi>=0.54.1,<0.55.0', 'uvicorn>=0.11.5,<0.12.0'],
 'sudachi': ['sudachipy==0.4.9', 'sudachidict-core>=20200330,<20200331']}

setup_kwargs = {
    'name': 'konoha',
    'version': '4.6.3',
    'description': 'A tiny sentence/word tokenizer for Japanese text written in Python',
    'long_description': '# 🌿 Konoha: Simple wrapper of Japanese Tokenizers\n\n[![GitHub stars](https://img.shields.io/github/stars/himkt/konoha?style=social)](https://github.com/himkt/konoha/stargazers)\n\n[![Downloads](https://pepy.tech/badge/konoha)](https://pepy.tech/project/konoha)\n[![Downloads](https://pepy.tech/badge/konoha/month)](https://pepy.tech/project/konoha/month)\n[![Downloads](https://pepy.tech/badge/konoha/week)](https://pepy.tech/project/konoha/week)\n\n[![Build Status](https://github.com/himkt/konoha/workflows/Python%20package/badge.svg?style=flat-square)](https://github.com/himkt/konoha/actions)\n[![Documentation Status](https://readthedocs.org/projects/konoha/badge/?version=latest)](https://konoha.readthedocs.io/en/latest/?badge=latest)\n![Python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue?logo=python)\n[![PyPI](https://img.shields.io/pypi/v/konoha.svg)](https://pypi.python.org/pypi/konoha)\n[![GitHub Issues](https://img.shields.io/github/issues/himkt/konoha.svg?cacheSeconds=60&color=yellow)](https://github.com/himkt/konoha/issues)\n[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/himkt/konoha.svg?cacheSeconds=60&color=yellow)](https://github.com/himkt/konoha/issues)\n\n`Konoha` is a Python library for providing easy-to-use integrated interface of various Japanese tokenziers,\nwhich enables you to switch a tokenizer and boost your pre-processing.\n\n## Supported tokenizers\n\n<a href="https://github.com/buruzaemon/natto-py"><img src="https://img.shields.io/badge/MeCab-natto--py-ff69b4"></a>\n<a href="https://github.com/chezou/Mykytea-python"><img src="https://img.shields.io/badge/KyTea-Mykytea--python-ff69b4"></a>\n<a href="https://github.com/mocobeta/janome"><img src="https://img.shields.io/badge/Janome-janome-ff69b4"></a>\n<a href="https://github.com/WorksApplications/SudachiPy"><img src="https://img.shields.io/badge/Sudachi-sudachipy-ff69b4"></a>\n<a href="https://github.com/google/sentencepiece"><img src="https://img.shields.io/badge/Sentencepiece-sentencepiece-ff69b4"></a>\n<a href="https://github.com/taishi-i/nagisa"><img src="https://img.shields.io/badge/nagisa-nagisa-ff69b4"></a>\n\nAlso, `konoha` provides rule-based tokenizers (whitespace, character) and a rule-based sentence splitter.\n\n\n## Quick Start with Docker\n\nSimply run followings on your computer:\n\n```baseh\ndocker run --rm -p 8000:8000 -t himkt/konoha  # from DockerHub\n```\n\nOr you can build image on your machine:\n\n```bash\ngit clone https://github.com/himkt/konoha  # download konoha\ncd konoha && docker-compose up --build  # build and launch contaier\n```\n\nTokenization is done by posting a json object to `localhost:8000/api/tokenize`.\nYou can also batch tokenize by passing `texts: ["１つ目の入力", "２つ目の入力"]` to the server.\n\n(API documentation is available on `localhost:8000/redoc`, you can check it using your web browser)\n\nSend a request using `curl` on you terminal.\n\n```json\n$ curl localhost:8000/api/tokenize -X POST -H "Content-Type: application/json" \\\n    -d \'{"tokenizer": "mecab", "text": "これはペンです"}\'\n\n{\n  "tokens": [\n    [\n      {\n        "surface": "これ",\n        "part_of_speech": "名詞"\n      },\n      {\n        "surface": "は",\n        "part_of_speech": "助詞"\n      },\n      {\n        "surface": "ペン",\n        "part_of_speech": "名詞"\n      },\n      {\n        "surface": "です",\n        "part_of_speech": "助動詞"\n      }\n    ]\n  ]\n}\n```\n\n\n## Installation\n\n\nI recommend you to install konoha by `pip install \'konoha[all]\'` or `pip install \'konoha[all_with_integrations]\'`.\n(`all_with_integrations` will install `AllenNLP`)\n\n- Install konoha with a specific tokenizer: `pip install \'konoha[(tokenizer_name)]`.\n- Install konoha with a specific tokenizer and AllenNLP integration: `pip install \'konoha[(tokenizer_name),allennlp]`.\n- Install konoha with a specific tokenzier and remote file support: `pip install \'konoha[(tokenizer_name),remote]\'`\n\n** Attention!! **\n\nCurrently, installing konoha with all tokenizers on Python3.8 fails.\nThis failure happens since we can\'t install nagisa on Python3.8. (https://github.com/taishi-i/nagisa/issues/24)\nThis problem is caused by DyNet dependency problem. (https://github.com/clab/dynet/issues/1616)\nDyNet doesn\'t provide wheel for Python3.8 and building DyNet from source doesn\'t work due to the dependency issue of DyNet.\n\nIf you want to install konoha with a tokenizer, please install konoha with a specific tokenizer\n(e.g. `konoha[mecab]`, `konoha[sudachi]`, ...etc) or install tokenizers individually.\n\n\n## Example\n\n### Word level tokenization\n\n```python\nfrom konoha import WordTokenizer\n\nsentence = \'自然言語処理を勉強しています\'\n\ntokenizer = WordTokenizer(\'MeCab\')\nprint(tokenizer.tokenize(sentence))\n# => [自然, 言語, 処理, を, 勉強, し, て, い, ます]\n\ntokenizer = WordTokenizer(\'Sentencepiece\', model_path="data/model.spm")\nprint(tokenizer.tokenize(sentence))\n# => [▁, 自然, 言語, 処理, を, 勉強, し, ています]\n```\n\nFor more detail, please see the `example/` directory.\n\n### Remote files\n\nKonoha supports dictionary and model on cloud storage (currently supports Amazon S3).\nIt requires installing konoha with the `remote` option, see [Installation](#installation).\n\n```python\n# download user dictionary from S3\nword_tokenizer = WordTokenizer("mecab", user_dictionary_path="s3://abc/xxx.dic")\nprint(word_tokenizer.tokenize(sentence))\n\n# download system dictionary from S3\nword_tokenizer = WordTokenizer("mecab", system_dictionary_path="s3://abc/yyy")\nprint(word_tokenizer.tokenize(sentence))\n\n# download model file from S3\nword_tokenizer = WordTokenizer("sentencepiece", model_path="s3://abc/zzz.model")\nprint(word_tokenizer.tokenize(sentence))\n```\n\n### Sentence level tokenization\n\n```python\nfrom konoha import SentenceTokenizer\n\nsentence = "私は猫だ。名前なんてものはない。だが，「かわいい。それで十分だろう」。"\n\ntokenizer = SentenceTokenizer()\nprint(tokenizer.tokenize(sentence))\n# => [\'私は猫だ。\', \'名前なんてものはない。\', \'だが，「かわいい。それで十分だろう」。\']\n```\n\n### AllenNLP integration\n\nKonoha provides AllenNLP integration, it enables users to specify konoha tokenizer in a Jsonnet config file.\nBy running `allennlp train` with `--include-package konoha`, you can train a model using konoha tokenizer!\n\nFor example, konoha tokenizer is specified in `xxx.jsonnet` like following:\n\n```jsonnet\n{\n  "dataset_reader": {\n    "lazy": false,\n    "type": "text_classification_json",\n    "tokenizer": {\n      "type": "konoha",  // <-- konoha here!!!\n      "tokenizer_name": "janome",\n    },\n    "token_indexers": {\n      "tokens": {\n        "type": "single_id",\n        "lowercase_tokens": true,\n      },\n    },\n  },\n  ...\n  "model": {\n  ...\n  },\n  "trainer": {\n  ...\n  }\n}\n```\n\nAfter finishing other sections (e.g. model config, trainer config, ...etc), `allennlp train config/xxx.jsonnet --include-package konoha --serialization-dir yyy` works!\n(remember to include konoha by `--include-package konoha`)\n\nFor more detail, please refer [my blog article](https://qiita.com/klis/items/f1d29cb431d1bf879898) (in Japanese, sorry).\n\n## Test\n\n```\npython -m pytest\n```\n\n## Article\n\n- Introducing Konoha (in Japanese): [トークナイザをいい感じに切り替えるライブラリ konoha を作った](https://qiita.com/klis/items/bb9ffa4d9c886af0f531)\n- Implementing AllenNLP integration (in Japanese): [日本語解析ツール Konoha に AllenNLP 連携機能を実装した](https://qiita.com/klis/items/f1d29cb431d1bf879898)\n\n## Acknowledgement\n\nSentencepiece model used in test is provided by @yoheikikuta. Thanks!\n',
    'author': 'himkt',
    'author_email': 'himkt@klis.tsukuba.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
