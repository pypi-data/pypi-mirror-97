# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests',
 'xepmts',
 'xepmts.api',
 'xepmts.api.server',
 'xepmts.api.server.sc',
 'xepmts.api.server.v1',
 'xepmts.api.server.v2',
 'xepmts.web_client',
 'xepmts.web_client.src',
 'xepmts.web_client.src.apps',
 'xepmts.web_client.src.apps.api_client_gui',
 'xepmts.web_client.src.apps.gains_viewer',
 'xepmts.web_client.src.apps.heatmap_viewer',
 'xepmts.web_client.src.apps.home',
 'xepmts.web_client.src.apps.pandas_profiling',
 'xepmts.web_client.src.apps.perspective_viewer',
 'xepmts.web_client.src.apps.pmt_datasheets',
 'xepmts.web_client.src.apps.resource_plots',
 'xepmts.web_client.src.apps.trend_viewer',
 'xepmts.web_client.src.assets',
 'xepmts.web_client.src.shared',
 'xepmts.web_client.src.shared.modifications']

package_data = \
{'': ['*'],
 'xepmts.api': ['endpoints/*'],
 'xepmts.web_client': ['requirements/*'],
 'xepmts.web_client.src': ['config/*']}

install_requires = \
['bokeh==2.2.3',
 'click',
 'eve-panel==0.3.12',
 'invoke>=1.5.0,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'xeauth==0.1.2']

extras_require = \
{'dask': ['dask[dataframe]>=2021.2.0,<2022.0.0'],
 'full': ['eve-jwt>=0.1.9,<0.2.0',
          'flask_swagger_ui>=3.36.0,<4.0.0',
          'prometheus_flask_exporter>=0.18.1,<0.19.0',
          'dask[dataframe]>=2021.2.0,<2022.0.0',
          'hvplot>=0.7.0,<0.8.0',
          'awesome-panel-extensions>=20210124.1,<20210125.0',
          'ipywidgets_bokeh>=1.0.2,<2.0.0',
          'ipywidgets>=7.6.3,<8.0.0'],
 'plotting': ['hvplot>=0.7.0,<0.8.0'],
 'server': ['eve-jwt>=0.1.9,<0.2.0',
            'flask_swagger_ui>=3.36.0,<4.0.0',
            'prometheus_flask_exporter>=0.18.1,<0.19.0'],
 'webclient': ['awesome-panel-extensions>=20210124.1,<20210125.0']}

entry_points = \
{'console_scripts': ['xepmts = xepmts.cli:main']}

setup_kwargs = {
    'name': 'xepmts',
    'version': '0.4.13',
    'description': 'Python client for accessing the XENON experiment PMT data.',
    'long_description': '======\nxepmts\n======\n\n\n.. image:: https://img.shields.io/pypi/v/xepmts.svg\n        :target: https://pypi.python.org/pypi/xepmts\n\n.. image:: https://img.shields.io/travis/jmosbacher/xepmts.svg\n        :target: https://travis-ci.com/jmosbacher/xepmts\n\n.. image:: https://readthedocs.org/projects/xepmts/badge/?version=latest\n        :target: https://xepmts.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\nBasic Usage\n-----------\n\n.. code-block:: python\n\n    import xepmts\n\n    # If you are using a notebook:\n    xepmts.notebook()\n\n    db = xepmts.default_client()\n    db.set_token(\'YOUR-API-TOKEN\')\n\n    # set the number of items to pull per page\n    db.tpc.installs.items_per_page = 25\n    \n    # get the next page \n    page = db.tpc.installs.next_page()\n\n    # iterate over pages:\n    for page in db.tpc.installs.pages():\n        df = page.df\n        # do something with data\n\n    # select only top array\n    top_array = db.tpc.installs.filter(array="top")\n\n    # iterate over top array pages\n    for page in top_array.pages():\n        df = page.df\n        # do something with data\n\n    query = dict(pmt_index=4)\n    # get the first page of results for this query as a list of dictionaries\n    docs = db.tpc.installs.find(query, max_results=25, page_number=1)\n\n    # same as find, but returns a dataframe \n    df = db.tpc.installs.find_df(query)\n\n\n    # insert documents into the database\n    docs = [{"pmt_index": 1, "position_x": 0, "position_y": 0}]\n    db.tpc.installs.insert_documents(docs)\n    \n* Free software: MIT\n* Documentation: https://xepmts.readthedocs.io/\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Yossi Mosbacher',
    'author_email': 'joe.mosbacher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmosbacher/xepmts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1',
}


setup(**setup_kwargs)
