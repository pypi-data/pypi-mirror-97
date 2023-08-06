# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['culqi', 'culqi.resources', 'culqi.schemas', 'culqi.utils']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2.0,<4.0.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'culqi-api-python',
    'version': '1.0.0',
    'description': 'Biblioteca de Culqi en Python',
    'long_description': '![Community project](https://raw.githubusercontent.com/softbutterfly/culqi-api-python/master/resources/softbutterfly-open-source-community-project.png)\n\n![PyPI - Supported versions](https://img.shields.io/pypi/pyversions/culqi-api-python)\n![PyPI - Package version](https://img.shields.io/pypi/v/culqi-api-python)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/culqi-api-python)\n![PyPI - MIT License](https://img.shields.io/pypi/l/culqi-api-python)\n\n[![Build Status](https://www.travis-ci.org/softbutterfly/culqi-api-python.svg?branch=develop)](https://www.travis-ci.org/softbutterfly/culqi-api-python)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/8ac045251e9745eea3b89c2896b1f777)](https://www.codacy.com/gh/softbutterfly/culqi-api-python/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=softbutterfly/culqi-api-python&amp;utm_campaign=Badge_Grade)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/8ac045251e9745eea3b89c2896b1f777)](https://www.codacy.com/gh/softbutterfly/culqi-api-python/dashboard?utm_source=github.com&utm_medium=referral&utm_content=softbutterfly/culqi-api-python&utm_campaign=Badge_Coverage)\n[![codecov](https://codecov.io/gh/softbutterfly/culqi-api-python/branch/master/graph/badge.svg?token=pbqXUUOu1F)](https://codecov.io/gh/softbutterfly/culqi-api-python)\n[![Requirements Status](https://requires.io/github/softbutterfly/culqi-api-python/requirements.svg?branch=master)](https://requires.io/github/softbutterfly/culqi-api-python/requirements/?branch=master)\n\n# Culqi API Python\n\nBiblioteca de CULQI para el lenguaje Python, pagos simples en tu sitio web.\n\n## Requisitos\n\n- Python 3.6, 3.7, 3.8, 3.9\n- Credenciales de comercio en [Culqi](https://culqi.com).\n\n## Instalación\n\n```bash\npip install culqi-api-python\n```\n\n![Sample](https://raw.githubusercontent.com/softbutterfly/culqi-api-python/master/resources/carbon.png)\n\nCada metodo retona un diccionario con la estructura\n\n```python\n{\n      "status": status_code,\n      "data": data\n}\n```\n\nEl `status_code` es el estatus HTTP numérico devuelto por la solicitud HTTP que se\nrealiza al API de Culqi, y `data` contiene el cuerpo de la respuesta obtenida.\n\n## Documentación\n\n- [Referencia de API](https://www.culqi.com/api/)\n- [Ejemplos](https://github.com/softbutterfly/culqi-api-python/wiki)\n- [Wiki](https://github.com/softbutterfly/culqi-api-python/wiki)\n\n## Changelog\n\nTodos los cambios en las versiones de esta biblioteca están listados en\nel [historial de cambios](CHANGELOG.md).\n\n## Desarrollo\n\nRevisa nuestra [guia de contribución](CONTRIBUTING.md)\n\n## Contribuidores\n\nMira la lista de contribuidores [aquí](https://github.com/softbutterfly/culqi-api-python/graphs/contributors).\n\n## Historia...\n\nLa libreria de Culqi para Python inicio su desarrollo en enero del 2017, d ela mano de [@william-muro-culqi](https://github.com/william-muro-culqi) y [@marti1125](https://github.com/marti1125), posteriorme [@brayancruces](https://github.com/brayancruces), [@KhanMaytok](https://github.com/KhanMaytok) y [@oskargicast](https://github.com/oskargicast) complementaron el trabajo incial y mantiuvieron la libreria estable hasta mediados de 2019. En enero del 2020 [@zodiacfireworks](https://github.com/zodiacfireworks) hace una refactorizacion completa de la libreria, estos cambios son aprobados y mejorados por [@joelibaceta](https://github.com/joelibaceta). Con estos cambios se publicaron las versiones 1.0.0, 1.0.1, 1.0.2 y 1.0.3 de la libreria. [@zodiacfireworks](https://github.com/zodiacfireworks) envió más cambios para corregir algunos errores de empaquetamiento, lamentablemente, tras mas de un año de haber sido enviados, no se publicaron a traves del canal oficial, por este motivo es que en [@SoftButterfly](https://github.com/softbutterfly) hemos tomado la iniciativa publicar esta libreria, compatible con la original, con los cambios que no llegaron a publicarse y otras mejoras que se pueden ver en el [historial de cambios](https://github.com/softbutterfly/culqi-api-python/blob/master/CHANGELOG.md). Con el fin de respetar el trabajo de quienes participaron del desarrollo de esta libreria en el repositorio focial de Culqi, el historial original de contribuciones se ha mantenido en este repositorio.\n',
    'author': 'SoftButterfly Development Team',
    'author_email': 'dev@softbutterfly.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/softbutterfly/culqi-api-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
