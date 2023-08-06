# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaqi']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyaqi',
    'version': '0.1.1',
    'description': 'Módulo para cálculo do Índice de Qualidade do Ar (IQAr).',
    'long_description': '# pyaqi\nMódulo para cálculo do IQAr - Índice de Qualidade do Ar (AQI - Air Quality Index).\n\n## Install\n\n```bash\npip install pyapi\n```\n\n## Usage\n\nA atual versão comporta somente o algoritmo brasileiro. Para saber mais\nsobre a metodologia brasileira, [consulte\naqui](https://www.gov.br/mma/pt-br/centrais-de-conteudo/mma-guia-tecnico-qualidade-do-ar-pdf).\n\nCom o pacote você pode converter a concentração média de um único poluente\npara o seu índice intermediário de qualidade (IQAI):\n\n```python\nimport aqi\nmyaqi = aqi()\nmyaqi.get_iaqi(210, "pm10_24h", algo=myaqi.aqi_brazil)\n# out: 168\n```\n\nOu obter o índice de qualidade do ar dadas as concentrações de múltiplos\npoluentes. Abaixo utilizamos o exemplo do capítulo 9 da metodologia brasileira:\n\n```python\nimport aqi\nmyaqi = aqi()\n# Calculando cada um dos poluentes\nmyaqi.get_iaqi(210, "pm10_24h", algo=myaqi.aqi_brazil)\nmyaqi.get_iaqi(135, "o3_8h", algo=myaqi.aqi_brazil)\nmyaqi.get_iaqi(220, "no2_1h", algo=myaqi.aqi_brazil)\nmyaqi.get_aqi() # por padrão usa o algo brasileiro\n# out: 168\n# Ou passando todas as concentracoes num unico dicionario\nmyaqi.get_aqi({"pm10_24h": 210}, {"o3_8h": 135}, {"no2_1h": 220}, algo=myaqi.aqi_brazil)\n# out: 168\n```',
    'author': 'Fernanda Scovino',
    'author_email': 'fscovinom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fernandascovino/iqarpy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
