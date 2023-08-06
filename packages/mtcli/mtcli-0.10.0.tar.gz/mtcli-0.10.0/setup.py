# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mtcli', 'mtcli.indicator']

package_data = \
{'': ['*']}

install_requires = \
['PyMQL5>=1.2.1,<2.0.0', 'click>=7.1.2,<8.0.0', 'python-dotenv>=0.10.3,<0.11.0']

entry_points = \
{'console_scripts': ['atr = mtcli.cli:atr',
                     'bars = mtcli.cli:bars',
                     'buy = mtcli.cli:buy',
                     'cancel = mtcli.cli:cancel',
                     'ema = mtcli.cli:ema',
                     'fib = mtcli.cli:fib',
                     'mt = mtcli.cli:cli',
                     'order = mtcli.cli:orders',
                     'position = mtcli.cli:positions',
                     'sell = mtcli.cli:sell',
                     'sma = mtcli.cli:sma']}

setup_kwargs = {
    'name': 'mtcli',
    'version': '0.10.0',
    'description': 'Ferramenta de linha de comando para leitura de graficos do MetaTrader 5 para deficientes visuais',
    'long_description': '# mtcli  \n  \nFerramenta de linha de comando para leitura de gráficos do MetaTrader 5 para deficientes visuais.  \n  \n[PyPI](https://pypi.python.org/pypi/mtcli)  \n[Documentação](https://vfranca.github.io/mtcli)  \n  \n------------\n\n## Pré-requisitos  \n\n* [MetaTrader5](https://www.metatrader5.com/pt) - Plataforma de trading.  \n* [Python](https://www.python.org/downloads/windows) - Interpretador de comandos disponível no prompt de comando.  \n\n\n## Instalação  \n\n1. Instale o Python. Obtenha o instalador em https://www.python.org/downloads/windows. Durante a instalação marque a opção para ficar disponível no path do Windows.\n\n2. No prompt de comando execute:\n```\n> pip install mtcli\n```\n3. Instale o MetaTrader 5. De preferência obtenha o instalador no site da sua corretora, caso contrário o instalador está disponível para download no site oficial do MetaTrader.  \n4. Baixe no link abaixo o arquivo contendo os arquivos de trabalho do mtcli:  \nhttps://drive.google.com/file/d/1olFEKJnnunBI1SDoW7QoMT9p6_yRQyhp/view?usp=sharing  \n5. Descompacte o arquivo mtcli-workspace.zip e renomeie para um nome da sua preferência. Essa pasta deverá ser usada para executar os atalhos de comandos do mtcli. Além disso nela estarão os expert advisors que deverão ser anexados ao s gráficos do MetaTrader 5 e o arquivo .env com variáveis de configuração.  \n6. Copie o arquivo .env para c:\\.env e altere a variável CSV_PATH com o caminho da pasta de arquivos do MetaTrader 5.  \n7. Anexe um dos  expert advisors ao gráfico do MetaTrader 5.  \n\nPronto! O mtcli está pronto para ser usado.  \n\n\n## Comandos  \n  \n* [mt bars](https://github.com/vfranca/mtcli/blob/master/docs/chart.md) - Exibe as barras do gráfico.  \n* [mt sma](https://github.com/vfranca/mtcli/blob/master/docs/chart.md) - Exibe a média móvel simples.  \n* [mt ema](https://github.com/vfranca/mtcli/blob/master/docs/chart.md) - Exibe a média móvel exponencial.  \n* [mt atr](https://github.com/vfranca/mtcli/blob/master/docs/chart.md) - Exibe average true range.  \n* [mt fib](https://github.com/vfranca/mtcli/blob/master/docs/chart.md) - Exibe retrações e projeções de fibonacci.  \n\n------------\n  \n  ## Agradecimentos  \n  \nAgradecimentos:  \nAo @MaiconBaggio desenvolvedor do PyMQL5 que faz uma comunicação com o MetaTrader5 e fornecedor do primeiro EA exportador das cotações.  \nAo Claudio Garini que transferiu a geração das cotações para um indicador.  \n\n\n------------\n  \n## Licenciamento  \n\nEste aplicativo está licenciado sob os termos da [GPL](../LICENSE).  \n',
    'author': 'Valmir Franca',
    'author_email': 'vfranca3@gmail.com',
    'maintainer': 'Valmir Franca',
    'maintainer_email': 'vfranca3@gmail.com',
    'url': 'https://github.com/vfranca/mtcli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
