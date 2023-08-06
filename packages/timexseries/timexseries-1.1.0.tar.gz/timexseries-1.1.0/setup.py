# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['timexseries',
 'timexseries.data_prediction',
 'timexseries.data_prediction.models',
 'timexseries.data_visualization']

package_data = \
{'': ['*'],
 'timexseries.data_prediction.models': ['default_prediction_parameters/*'],
 'timexseries.data_visualization': ['locales/*',
                                    'locales/en/LC_MESSAGES/*',
                                    'locales/it/LC_MESSAGES/*']}

install_requires = \
['colorhash>=1.0.3,<2.0.0',
 'dash-bootstrap-components>=0.11.3,<0.12.0',
 'dash>=1.19.0,<2.0.0',
 'dateparser>=1.0.0,<2.0.0',
 'fbprophet>=0.7.1,<0.8.0',
 'gunicorn>=20.0.4,<21.0.0',
 'networkx>=2.5,<3.0',
 'scipy>=1.6.0,<2.0.0',
 'sklearn>=0.0,<0.1',
 'statsmodels>=0.12.2,<0.13.0',
 'torch>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'timexseries',
    'version': '1.1.0',
    'description': 'TIMEX is a framework for time-series-forecasting-as-a-service.',
    'long_description': '# TIMEX\nTIMEX (referred in code as `timexseries`) is a framework for time-series-forecasting-as-a-service.\n\nIts main goal is to provide a simple and generic tool to build websites and, more in general,\nplatforms, able to provide the forecasting of time-series in the "as-a-service" manner.\n\nThis means that users should interact with the service as less as possible.\n\nAn example of the capabilities of TIMEX can be found at [covid-timex.it](https://covid-timex.it)  \nThat website is built using the [Dash](https://dash.plotly.com/), on which the visualization\npart of TIMEX is built. A deep explanation is available in the \n[dedicated repository](https://github.com/AlexMV12/covid-timex.it).\n\n## Installation\nThe main two dependencies of TIMEX are [Facebook Prophet](https://github.com/facebook/prophet)\nand [PyTorch](https://pytorch.org/). \nIf you prefer, you can install them beforehand, maybe because you want to choose the CUDA/CPU\nversion of Torch.\n\nHowever, installation is as simple as running:\n\n`pip install timexseries`\n\n## Get started\nPlease, refer to the Examples folder. You will find some Jupyter Notebook which illustrate\nthe main characteristics of TIMEX. A Notebook explaining the covid-timex.it website is present,\nalong with the source code of the site, [here](https://github.com/AlexMV12/covid-timex.it).\n\n## Documentation\nThe full documentation is available at [here](https://alexmv12.github.io/TIMEX/timexseries/index.html).\n\n## Contacts\nIf you have questions, suggestions or problems, feel free to open an Issue.\nYou can contact us at:\n\n- alessandro.falcetta@polimi.it\n- manuel.roveri@polimi.it\n\n',
    'author': 'Alessandro Falcetta',
    'author_email': 'alessandro.falcetta@polimi.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://alexmv12.github.io/TIMEX/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
