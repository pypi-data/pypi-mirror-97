# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['models', 'tomba']

package_data = \
{'': ['*'],
 'models': ['pt_core_news_sm_addresses/*',
            'pt_core_news_sm_addresses/entity_ruler/*',
            'pt_core_news_sm_addresses/vocab/*']}

install_requires = \
['jupyter>=1.0.0,<2.0.0',
 'pandas>=1.2.1,<2.0.0',
 'setuptools>=53.0.0,<54.0.0',
 'spacy>=3.0.0',
 'wheel>=0.36.2,<0.37.0']

setup_kwargs = {
    'name': 'tomba',
    'version': '0.1.1a1',
    'description': 'Identifique localizações brasileiras em um texto 🏘',
    'long_description': '# tomba\n\n[![Built with spaCy](https://img.shields.io/badge/made%20with%20❤%20and-spaCy-09a3d5.svg)](https://spacy.io) [![CI](https://github.com/DadosAbertosDeFeira/tomba/actions/workflows/ci.yml/badge.svg)](https://github.com/DadosAbertosDeFeira/tomba/actions/workflows/ci.yml)\n\nIdentifique endereços, bairros e outras localizações brasileiras em um texto. 🏘\n\nNão sabe o que é o [Tomba](https://pt.wikipedia.org/wiki/Tomba_(Feira_de_Santana))?\n\n---\n\nEssa biblioteca é experimental e está no seu estágio inicial de desenvolvimento.\n\nObjetivo:\n\n```python\nimport tomba\n\n\ntomba.get_locations(\n    "Contratação de empresa de engenharia para executar obras "\n    "de pavimentação localizados no CEP 44100-000, no bairro Tomba."\n)\n```\n\nSaída:\n\n```\n[\n    {"type": "zipcode", "start": 92, "end": 123},\n    {"type": "neighborhood", "start": 113, "end": 118}\n]\n```\n\n## Desenvolvimento\n\nUtilizamos o [poetry](https://python-poetry.org/) para empacotamento e gerenciamento das dependências.\n\nPara instalar as dependências, execute `poetry install`.\n\nPara configurar o [spacy](https://spacy.io) em português, execute:\n\n```\npoetry run python -m spacy download pt_core_news_sm\n```\n\nPara rodar os testes:\n\n```\npoetry run pytest\n```\n\nPara gerar um novo modelo:\n\n```\npoetry run python tomba/models.py\n```\n',
    'author': 'Dados Abertos de Feira',
    'author_email': 'dadosabertosdefeira+gh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
