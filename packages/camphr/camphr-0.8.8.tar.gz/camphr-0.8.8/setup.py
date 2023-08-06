# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camphr',
 'camphr.cli',
 'camphr.lang',
 'camphr.lang.juman',
 'camphr.lang.mecab',
 'camphr.lang.sentencepiece',
 'camphr.ner_labels',
 'camphr.pipelines',
 'camphr.pipelines.knp',
 'camphr.pipelines.transformers']

package_data = \
{'': ['*'],
 'camphr': ['model_config/*'],
 'camphr.cli': ['conf/train/*', 'conf/train/example/*']}

install_requires = \
['catalogue>=1.0.0,<2.0.0',
 'dataclasses>=0.6,<0.7',
 'fire>=0.2.1,<1.0',
 'hydra-core>=0.11.3,<0.12.0',
 'hydra_colorlog>=0.1.4,<0.2.0',
 'more-itertools',
 'pyahocorasick>=1.4.0,<2.0.0',
 'pytextspan>=0.5.0,<1.0',
 'pytokenizations>=0.4.8,<1.0',
 'scikit-learn>=0.22,<0.25',
 'spacy>=2.2,<3',
 'toolz>=0.10,<0.12',
 'torch>=1.0,<2.0',
 'transformers>=3.0,<3.1',
 'typing-extensions>=3.7.4']

extras_require = \
{'all': ['mojimoji>=0.0.11,<0.0.12',
         'ipadic>=1.0,<2.0',
         'fugashi>=1.0,<2.0',
         'pyknp>=0.4.2,<0.5',
         'mecab-python3>=1.0,<1.1'],
 'juman': ['mojimoji>=0.0.11,<0.0.12', 'pyknp>=0.4.2,<0.5'],
 'mecab': ['fugashi>=1.0,<2.0', 'mecab-python3>=1.0,<1.1']}

entry_points = \
{'console_scripts': ['camphr = camphr.cli.__main__:main'],
 'spacy_factories': ['juman_sentencizer = '
                     'camphr.pipelines.knp:juman_sentencizer_factory',
                     'knp = camphr.pipelines.knp:KNP.from_nlp',
                     'knp_dependency_parser = '
                     'camphr.pipelines.knp.dependency_parser:knp_dependency_parser_factory',
                     'knp_parallel_noun_chunker = '
                     'camphr.pipelines.knp.noun_chunker:knp_parallel_noun_chunker_factory',
                     'multiple_regex_ruler = '
                     'camphr.pipelines:MultipleRegexRuler.from_nlp',
                     'regex_ruler = camphr.pipelines:RegexRuler.from_nlp',
                     'transformers_model = '
                     'camphr.pipelines.transformers:TrfModel.from_nlp',
                     'transformers_ner = '
                     'camphr.pipelines.transformers:TrfForNamedEntityRecognition.from_nlp',
                     'transformers_sequece_classifier = '
                     'camphr.pipelines.transformers:TrfForSequenceClassification.from_nlp',
                     'transformers_sequence_classifier = '
                     'camphr.pipelines.transformers:TrfForSequenceClassification.from_nlp',
                     'transformers_tokenizer = '
                     'camphr.pipelines.transformers:TrfTokenizer.from_nlp'],
 'spacy_languages': ['camphr_torch = camphr.lang.torch:TorchLanguage',
                     'ja_juman = camphr.lang.juman:Japanese',
                     'ja_mecab = camphr.lang.mecab:Japanese',
                     'sentencepiece = '
                     'camphr.lang.sentencepiece:SentencePieceLang']}

setup_kwargs = {
    'name': 'camphr',
    'version': '0.8.8',
    'description': 'spaCy plugin for Transformers, Udify, Elmo, etc.',
    'long_description': '<p align="center"><img src="https://raw.githubusercontent.com/PKSHATechnology-Research/camphr/master/img/logoc.svg?sanitize=true" width="200" /></p>\n\n# Camphr - spaCy plugin for Transformers, Udify, Elmo, etc.\n\n[![Documentation Status](https://readthedocs.org/projects/camphr/badge/?version=latest)](https://camphr.readthedocs.io/en/latest/?badge=latest)\n[![Gitter](https://badges.gitter.im/camphr/community.svg)](https://gitter.im/camphr/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)\n[![PyPI version](https://badge.fury.io/py/camphr.svg)](https://badge.fury.io/py/camphr)\n![test and publish](https://github.com/PKSHATechnology-Research/camphr/workflows/test%20and%20publish/badge.svg)\n![](https://github.com/PKSHATechnology-Research/camphr/workflows/test%20extras/badge.svg)\n![](https://github.com/PKSHATechnology-Research/camphr/workflows/test%20package/badge.svg)\n\nCamphr is a *Natural Language Processing* library that helps in seamless integration for a wide variety of techniques from state-of-the-art to conventional ones.\nYou can use [Transformers](https://huggingface.co/transformers/) ,  [Udify](https://github.com/Hyperparticle/udify), [ELmo](https://allennlp.org/elmo), etc. on [spaCy](https://github.com/explosion/spaCy).\n\nCheck the [documentation](https://camphr.readthedocs.io/en/latest/) for more information.\n\n(For Japanese: https://qiita.com/tamurahey/items/53a1902625ccaac1bb2f)\n\n# Features\n\n- A [spaCy](https://github.com/explosion/spaCy) plugin - Easily integration for a wide variety of methods\n- [Transformers](https://huggingface.co/transformers/) with spaCy - Fine-tuning pretrained model with [Hydra](https://hydra.cc/). Embedding vector\n- [Udify](https://github.com/Hyperparticle/udify) - BERT based multitask model in 75 languages\n- [Elmo](https://allennlp.org/elmo) - Deep contextualized word representations\n- Rule base matching with Aho-Corasick, Regex\n- (for Japanese) KNP\n\n# License\n\nCamphr is licensed under [Apache 2.0](./LICENSE).\n\n',
    'author': 'tamuhey',
    'author_email': 'tamuhey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PKSHATechnology-Research/camphr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4',
}


setup(**setup_kwargs)
