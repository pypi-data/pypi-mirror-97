# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wetterdienst',
 'wetterdienst.core',
 'wetterdienst.core.scalar',
 'wetterdienst.dwd',
 'wetterdienst.dwd.forecasts',
 'wetterdienst.dwd.forecasts.metadata',
 'wetterdienst.dwd.metadata',
 'wetterdienst.dwd.observations',
 'wetterdienst.dwd.observations.metadata',
 'wetterdienst.dwd.observations.util',
 'wetterdienst.dwd.radar',
 'wetterdienst.dwd.radar.metadata',
 'wetterdienst.metadata',
 'wetterdienst.util']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0',
 'aenum>=2.2.6,<3.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'beautifulsoup4>=4.9.1,<5.0.0',
 'cachetools>=4.1.1,<5.0.0',
 'dateparser>=1.0.0,<2.0.0',
 'deprecation>=2.1.0,<3.0.0',
 'docopt>=0.6.2,<0.7.0',
 'dogpile.cache>=1.0.2,<2.0.0',
 'lxml>=4.5.2,<5.0.0',
 'munch>=2.5.0,<3.0.0',
 'numpy>=1.19.5,<2.0.0',
 'pandas>=1.1.2,<2.0.0',
 'python-dateutil>=2.8.0,<3.0.0',
 'requests>=2.24.0,<3.0.0',
 'scipy>=1.5.2,<2.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'tqdm>=4.47.0,<5.0.0']

extras_require = \
{':extra == "ipython" or extra == "docs"': ['matplotlib>=3.3.2,<4.0.0'],
 ':python_version < "3.8"': ['importlib_metadata>=1.7.0,<2.0.0'],
 ':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8'],
 'cratedb': ['crate[sqlalchemy]>=0.25.0,<0.26.0'],
 'docs': ['sphinx>=3.2.1,<4.0.0',
          'sphinx-material>=0.0.30,<0.0.31',
          'sphinx-autodoc-typehints>=1.11.0,<2.0.0',
          'sphinxcontrib-svg2pdfconverter>=1.1.0,<2.0.0',
          'tomlkit>=0.7.0,<0.8.0',
          'ipython>=7.10.1,<8.0.0'],
 'duckdb': ['duckdb>=0.2.3,<0.3.0'],
 'excel': ['openpyxl>=3.0.5,<4.0.0'],
 'http': ['fastapi>=0.61.1,<0.62.0'],
 'http:python_version >= "3.6" and python_version < "4.0"': ['uvicorn>=0.13.3,<0.14.0'],
 'influxdb': ['influxdb>=5.3.0,<6.0.0'],
 'ipython': ['ipython>=7.10.1,<8.0.0', 'ipython-genutils>=0.2.0,<0.3.0'],
 'mysql': ['mysqlclient>=2.0.1,<3.0.0'],
 'postgresql': ['psycopg2-binary>=2.8.6,<3.0.0'],
 'radar': ['wradlib>=1.9.0,<2.0.0'],
 'sql': ['duckdb>=0.2.3,<0.3.0']}

entry_points = \
{'console_scripts': ['wddump = wetterdienst.dwd.radar.cli:wddump',
                     'wetterdienst = wetterdienst.cli:run']}

setup_kwargs = {
    'name': 'wetterdienst',
    'version': '0.15.0',
    'description': 'Open weather data for humans',
    'long_description': 'Wetterdienst - Open weather data for humans\n###########################################\n\n.. container:: align-center\n\n    .. figure:: https://raw.githubusercontent.com/earthobservations/wetterdienst/main/docs/img/temperature_ts.png\n        :alt: temperature timeseries of Hohenpeissenberg/Germany\n\n    *"Three things are (almost) infinite: the universe, human stupidity and the temperature time series of\n    Hohenpeissenberg I got with the help of wetterdienst; and I\'m not sure about the universe." - Albert Einstein*\n\n\n.. overview_start_marker\n\nOverview\n########\n\n.. image:: https://github.com/earthobservations/wetterdienst/workflows/Tests/badge.svg\n   :target: https://github.com/earthobservations/wetterdienst/actions?workflow=Tests\n.. image:: https://codecov.io/gh/earthobservations/wetterdienst/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/earthobservations/wetterdienst\n.. image:: https://readthedocs.org/projects/wetterdienst/badge/?version=latest\n   :target: https://wetterdienst.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n\n.. image:: https://img.shields.io/pypi/pyversions/wetterdienst.svg\n   :target: https://pypi.python.org/pypi/wetterdienst/\n.. image:: https://img.shields.io/pypi/v/wetterdienst.svg\n   :target: https://pypi.org/project/wetterdienst/\n.. image:: https://img.shields.io/pypi/status/wetterdienst.svg\n   :target: https://pypi.python.org/pypi/wetterdienst/\n.. image:: https://pepy.tech/badge/wetterdienst/month\n   :target: https://pepy.tech/project/wetterdienst/month\n.. image:: https://img.shields.io/github/license/earthobservations/wetterdienst\n   :target: https://github.com/earthobservations/wetterdienst/blob/main/LICENSE\n.. image:: https://zenodo.org/badge/160953150.svg\n   :target: https://zenodo.org/badge/latestdoi/160953150\n.. image:: https://img.shields.io/discord/704622099750191174.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2\n   :target: https://discord.gg/8sCb978a\n\nIntroduction\n************\n\nWelcome to Wetterdienst, your friendly weather service library for Python.\n\nWe are a group of like-minded people trying to make access to weather data in\nPython feel like a warm summer breeze, similar to other projects like\nrdwd_ for the R language, which originally drew our interest in this project.\nOur long-term goal is to provide access to multiple weather services as well as other\nrelated agencies such as river measurements. With ``wetterdienst`` we try to use modern\nPython technologies all over the place. The library is based on pandas_ across the board,\nuses Poetry_ for package administration and GitHub Actions for all things CI.\nOur users are an important part of the development as we are not currently using the\ndata we are providing and only implement what we think would be the best. Therefore\ncontributions and feedback whether it be data related or library related are very\nwelcome! Just hand in a PR or Issue if you think we should include a new feature or data\nsource.\n\n.. _rdwd: https://github.com/brry/rdwd\n.. _pandas: https://pandas.pydata.org/\n.. _Poetry: https://python-poetry.org/\n\nAcknowledgements\n****************\n\nWe want to acknowledge all environmental agencies which provide their data open and free\nof charge first and foremost for the sake of endless research possibilities.\n\nWe want to acknowledge Jetbrains_ and their `open source team`_ for providing us with\nlicenses for Pycharm Pro, which we are using for the development.\n\nWe want to acknowledge all contributors for being part of the improvements to this\nlibrary that make it better and better every day.\n\n.. _Jetbrains: https://www.jetbrains.com/\n.. _open source team: https://github.com/JetBrains\n\nCoverage\n********\n\nDWD (German Weather Service / Deutscher Wetterdienst / Germany)\n    - Historical Weather Observations\n        - Historical (last ~300 years), recent (500 days to yesterday), now (yesterday up to last hour)\n        - every minute to yearly resolution\n        - Time series of stations in Germany\n    - Mosmix - statistical optimized scalar forecasts extracted from weather models\n        - Point forecast\n        - 5400 stations worldwide\n        - Both MOSMIX-L and MOSMIX-S is supported\n        - Up to 115 parameters\n    - Radar\n        - 16 locations in Germany\n        - All of Composite, Radolan, Radvor, Sites and Radolan_CDC\n        - Radolan: calibrated radar precipitation\n        - Radvor: radar precipitation forecast\n\nTo get better insight on which data we have currently made available and under which\nlicense those are published take a look at the data_ section.\n\n.. _data: https://wetterdienst.readthedocs.io/en/latest/data/index.html\n\nFeatures\n********\n\n- API(s) for stations (metadata) and values\n- Get station(s) nearby a selected location\n- Define your request by arguments such as `parameter`, `period`, `resolution`,\n  `start date`, `end date`\n- Command line interface\n- Web-API via FastAPI\n- Run SQL queries on the results\n- Export results to databases and other data sinks\n- Public Docker image\n\nSetup\n*****\n\n``wetterdienst`` can be used by either installing it on your workstation or within a Docker\ncontainer.\n\nNative\n======\n\nVia PyPi (standard):\n\n.. code-block:: bash\n\n    pip install wetterdienst\n\nVia Github (most recent):\n\n.. code-block:: bash\n\n    pip install git+https://github.com/earthobservations/wetterdienst\n\nThere are some extras available for ``wetterdienst``. Use them like:\n\n.. code-block:: bash\n\n    pip install wetterdienst[http,sql]\n\n- docs: Install the Sphinx documentation generator.\n- ipython: Install iPython stack.\n- excel: Install openpyxl for Excel export.\n- http: Install HTTP API prerequisites.\n- sql: Install DuckDB for querying data using SQL.\n- duckdb: Install support for DuckDB.\n- influxdb: Install support for InfluxDB.\n- cratedb: Install support for CrateDB.\n- mysql: Install support for MySQL.\n- postgresql: Install support for PostgreSQL.\n\nIn order to check the installation, invoke:\n\n.. code-block:: bash\n\n    wetterdienst --help\n\n.. _run-in-docker:\n\nDocker\n======\n\nDocker images for each stable release will get pushed to GitHub Container Registry.\n\nThere are images in two variants, ``wetterdienst-standard`` and ``wetterdienst-full``.\n\n``wetterdienst-standard`` will contain a minimum set of 3rd-party packages,\nwhile ``wetterdienst-full`` will try to serve a full environment by also\nincluding packages like GDAL and wradlib.\n\nPull the Docker image:\n\n.. code-block:: bash\n\n    docker pull ghcr.io/earthobservations/wetterdienst-standard\n\nLibrary\n-------\nUse the latest stable version of ``wetterdienst``:\n\n.. code-block:: bash\n\n    $ docker run -ti ghcr.io/earthobservations/wetterdienst-standard\n    Python 3.8.5 (default, Sep 10 2020, 16:58:22)\n    [GCC 8.3.0] on linux\n\n.. code-block:: python\n\n    import wetterdienst\n    wetterdienst.__version__\n\nCommand line script\n-------------------\nThe ``wetterdienst`` command is also available:\n\n.. code-block:: bash\n\n    # Make an alias to use it conveniently from your shell.\n    alias wetterdienst=\'docker run -ti ghcr.io/earthobservations/wetterdienst-standard wetterdienst\'\n\n    wetterdienst --version\n    wetterdienst --help\n\nExample\n********\n\nAcquisition of historical data for specific stations using ``wetterdienst`` as library:\n\n.. code-block:: python\n\n    >>> from wetterdienst import Wetterdienst\n    >>> API = Wetterdienst("dwd", "observation")\n    >>> request = API(\n    ...    parameter=["climate_summary"],\n    ...    resolution="daily",\n    ...    start_date="1990-01-01",  # Timezone: UTC\n    ...    end_date="2020-01-01",  # Timezone: UTC\n    ...    tidy_data=True,  # default\n    ...    humanize_parameters=True,  # default\n    ... ).filter(station_id=[1048, 4411])\n    >>> stations = request.df  # station list\n    >>> values = request.values.all().df  # values\n\nReceiving of stations for defined parameters using the ``wetterdienst`` client:\n\n.. code-block:: bash\n\n    # Get list of all stations for daily climate summary data in JSON format\n    wetterdienst dwd observations stations --parameter=kl --resolution=daily --period=recent\n\n    # Get daily climate summary data for specific stations\n    wetterdienst dwd observations values --station=1048,4411 --parameter=kl --resolution=daily --period=recent\n\nFurther examples (code samples) can be found in the `examples`_ folder.\n\n.. _examples: https://github.com/earthobservations/wetterdienst/tree/main/example\n\n.. overview_end_marker\n\nDocumentation\n*************\n\nWe strongly recommend reading the full documentation, which will be updated continuously\nas we make progress with this library:\n\nhttps://wetterdienst.readthedocs.io/\n\nFor the whole functionality, check out the `Wetterdienst API`_ section of our\ndocumentation, which will be constantly updated. To stay up to date with the\ndevelopment, take a look at the changelog_. Also, don\'t miss out our examples_.\n\nData license\n************\n\nLicenses of the available data can be found in our documentation at the `data license`_\nsection. Licenses and usage requirements may differ so check this out before including\nthe data in your project to be sure to fulfill copyright issues beforehand.\n\n.. _data license: https://wetterdienst.readthedocs.io/en/latest/pages/data_license.html\n\n.. contribution_development_marker\n\nContribution\n************\n\nThere are different ways in which you contribute to this library:\n\n- by handing in a PR which describes the feature/issue that was solved including tests\n  for newly added features\n- by using our library and reporting bugs to us either by mail or by creating a new\n  Issue\n- by letting us know either via issue or discussion what function or data source we may\n  include into this library describing possible solutions or acquisition\n  methods/endpoints/APIs\n\nDevelopment\n***********\n\n1. Clone the library and install the environment\n\n.. code-block:: bash\n\n    git clone https://github.com/earthobservations/wetterdienst\n    cd wetterdienst\n\n    pip install . # or poetry install\n\n2. Add required libraries e.g.\n\n.. code-block:: bash\n\n    poetry add pandas\n\n3. Apply your changes\n\n4. Add tests and documentation for your changes\n\n5. Clean up and run tests\n\n.. code-block:: bash\n\n    poe format  # black code formatting\n    poe lint  # lint checking\n    poe export  # export of requirements (for Github Dependency Graph)\n    poe test  # for quicker tests run: poe test -vvvv -m "not (remote or slow)"\n\n6. Push your changes and setup PR\n\nImportant Links\n***************\n\n`Wetterdienst API`_\n\nChangelog_\n\n.. _Wetterdienst API: https://wetterdienst.readthedocs.io/en/latest/usage/api.html\n.. _Changelog: https://wetterdienst.readthedocs.io/en/latest/changelog.html\n',
    'author': 'Benjamin Gutzmann',
    'author_email': 'gutzemann@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://wetterdienst.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
