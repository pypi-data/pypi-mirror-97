# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['human_readable']

package_data = \
{'': ['*'],
 'human_readable': ['locale/de_DE/LC_MESSAGES/human_readable.mo',
                    'locale/en_ABBR/LC_MESSAGES/human_readable.mo',
                    'locale/es_ES/LC_MESSAGES/human_readable.mo',
                    'locale/fa_IR/LC_MESSAGES/human_readable.mo',
                    'locale/fi_FI/LC_MESSAGES/human_readable.mo',
                    'locale/fr_FR/LC_MESSAGES/human_readable.mo',
                    'locale/id_ID/LC_MESSAGES/human_readable.mo',
                    'locale/it_IT/LC_MESSAGES/human_readable.mo',
                    'locale/ja_JP/LC_MESSAGES/human_readable.mo',
                    'locale/ko_KR/LC_MESSAGES/human_readable.mo',
                    'locale/nl_NL/LC_MESSAGES/human_readable.mo',
                    'locale/pl_PL/LC_MESSAGES/human_readable.mo',
                    'locale/pt_BR/LC_MESSAGES/human_readable.mo',
                    'locale/pt_PT/LC_MESSAGES/human_readable.mo',
                    'locale/ru_RU/LC_MESSAGES/human_readable.mo',
                    'locale/sk_SK/LC_MESSAGES/human_readable.mo',
                    'locale/tr_TR/LC_MESSAGES/human_readable.mo',
                    'locale/uk_UA/LC_MESSAGES/human_readable.mo',
                    'locale/vi_VI/LC_MESSAGES/human_readable.mo',
                    'locale/zh_CN/LC_MESSAGES/human_readable.mo',
                    'locale/zh_TW/LC_MESSAGES/human_readable.mo']}

setup_kwargs = {
    'name': 'human-readable',
    'version': '0.3.0',
    'description': 'Human Readable',
    'long_description': 'Human Readable\n==============\n\n|Status| |PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |Status| image:: https://badgen.net/badge/status/beta/orange\n   :target: https://badgen.net/badge/status/beta/orange\n   :alt: Project Status\n.. |PyPI| image:: https://img.shields.io/pypi/v/human-readable.svg\n   :target: https://pypi.org/project/human-readable/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/human-readable\n   :target: https://pypi.org/project/human-readable\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/human-readable\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/human-readable/latest.svg?label=Read%20the%20Docs\n   :target: https://human-readable.readthedocs.io/\n   :alt: Read the documentation at https://human-readable.readthedocs.io/\n.. |Tests| image:: https://github.com/staticdev/human-readable/workflows/Tests/badge.svg\n   :target: https://github.com/staticdev/human-readable/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/staticdev/human-readable/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/staticdev/human-readable\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* File size humanization.\n* List humanization.\n* Numbers humanization.\n* Time and dates humanization.\n* Internacionalization (i18n) to 20+ locales:\n\n  * Abbreviated English (en_ABBR)\n  * Brazilian Portuguese (pt_BR)\n  * Dutch (nl_NL)\n  * Finnish (fi_FI)\n  * French (fr_FR)\n  * German (de_DE)\n  * Indonesian (id_ID)\n  * Italian (it_IT)\n  * Japanese (ja_JP)\n  * Korean (ko_KR)\n  * Persian (fa_IR)\n  * Polish (pl_PL)\n  * Portugal Portuguese (pt_PT)\n  * Russian (ru_RU)\n  * Simplified Chinese (zh_CN)\n  * Slovak (sk_SK)\n  * Spanish (es_ES)\n  * Taiwan Chinese (zh_TW)\n  * Turkish (tr_TR)\n  * Ukrainian (uk_UA)\n  * Vietnamese (vi_VI)\n\n\nRequirements\n------------\n\n* It works in Python 3.7+.\n\n\nInstallation\n------------\n\nYou can install *Human Readable* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install human-readable\n\n\n.. basic-usage\n\nBasic usage\n-----------\n\nImport the lib with:\n\n.. code-block:: python\n\n   import human_readable\n\n\nDate and time humanization examples:\n\n.. code-block:: python\n\n   human_readable.time_of_day(17)\n   "afternoon"\n\n   import datetime as dt\n   human_readable.timing(dt.time(6, 59, 0))\n   "one minute to seven hours"\n\n   human_readable.timing(dt.time(21, 0, 40), formal=False)\n   "nine in the evening"\n\n   human_readable.time_delta(dt.timedelta(days=65))\n   "2 months"\n\n   human_readable.date_time(dt.datetime.now() - dt.timedelta(minutes=2))\n   "2 minutes ago"\n\n   human_readable.day(dt.date.today() - dt.timedelta(days=1))\n   "yesterday"\n\n   human_readable.date(dt.date(2019, 7, 2))\n   "Jul 02 2019"\n\n   human_readable.year(dt.date.today() + dt.timedelta(days=365))\n   "next year"\n\n\nPrecise time delta examples:\n\n.. code-block:: python\n\n   import datetime as dt\n   delta = dt.timedelta(seconds=3633, days=2, microseconds=123000)\n   human_readable.precise_delta(delta)\n   "2 days, 1 hour and 33.12 seconds"\n\n   human_readable.precise_delta(delta, minimum_unit="microseconds")\n   "2 days, 1 hour, 33 seconds and 123 milliseconds"\n\n   human_readable.precise_delta(delta, suppress=["days"], format="%0.4f")\n   "49 hours and 33.1230 seconds"\n\n\nFile size humanization examples:\n\n.. code-block:: python\n\n   human_readable.file_size(1000000)\n   "1.0 MB"\n\n   human_readable.file_size(1000000, binary=True)\n   "976.6 KiB"\n\n   human_readable.file_size(1000000, gnu=True)\n   "976.6K"\n\n\nLists humanization examples:\n\n.. code-block:: python\n\n   human_readable.listing(["Alpha", "Bravo"], ",")\n   "Alpha, Bravo"\n\n   human_readable.listing(["Alpha", "Bravo", "Charlie"], ";", "or")\n   "Alpha; Bravo or Charlie"\n\n\nNumbers humanization examples:\n\n.. code-block:: python\n\n   human_readable.int_comma(12345)\n   "12,345"\n\n   human_readable.int_word(123455913)\n   "123.5 million"\n\n   human_readable.int_word(12345591313)\n   "12.3 billion"\n\n   human_readable.ap_number(4)\n   "four"\n\n   human_readable.ap_number(41)\n   "41"\n\n\nFloating point number humanization examples:\n\n.. code-block:: python\n\n   human_readable.fractional(1.5)\n   "1 1/2"\n\n   human_readable.fractional(0.3)\n   "3/10"\n\n\nScientific notation examples:\n\n.. code-block:: python\n\n   human_readable.scientific_notation(1000)\n   "1.00 x 10³"\n\n   human_readable.scientific_notation(5781651000, precision=4)\n   "5.7817 x 10⁹"\n\n.. end-basic-usage\n\nComplete instructions can be found at `human-readable.readthedocs.io`_.\n\n\nLocalization\n------------\n\nHow to change locale at runtime:\n\n.. code-block:: python\n\n   import datetime as dt\n   human_readable.date_time(dt.timedelta(seconds=3))\n   \'3 seconds ago\'\n\n   _t = human_readable.i18n.activate("ru_RU")\n   human_readable.date_time(dt.timedelta(seconds=3))\n   \'3 секунды назад\'\n\n   human_readable.i18n.deactivate()\n   human_readable.date_time(dt.timedelta(seconds=3))\n   \'3 seconds ago\'\n\n\nYou can pass additional parameter `path` to `activate` to specify a path to search\nlocales in.\n\n.. code-block:: python\n\n   human_readable.i18n.activate("xx_XX")\n   ...\n   FileNotFoundError: [Errno 2] No translation file found for domain: \'human_readable\'\n   human_readable.i18n.activate("pt_BR", path="path/to/my/portuguese/translation/")\n   <gettext.GNUTranslations instance ...>\n\nYou can see how to add a new locale on the `Contributor Guide`_.\n\nA special locale, `en_ABBR`, renderes abbreviated versions of output:\n\n.. code-block:: python\n\n    human_readable.date_time(datetime.timedelta(seconds=3))\n    3 seconds ago\n\n    human_readable.int_word(12345591313)\n    12.3 billion\n\n    human_readable.date_time(datetime.timedelta(seconds=86400*476))\n    1 year, 3 months ago\n\n    human_readable.i18n.activate(\'en_ABBR\')\n    human_readable.date_time(datetime.timedelta(seconds=3))\n    3s\n\n    human_readable.int_word(12345591313)\n    12.3 B\n\n    human_readable.date_time(datetime.timedelta(seconds=86400*476))\n    1y 3M\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*Human Readable* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis lib is based on original humanize_ with some added features such as listing, improved naming, documentation, functional tests, type-annotations, bug fixes and better localization.\n\nThis project was generated from `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _humanize: https://github.com/jmoiron/humanize\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/staticdev/human-readable/issues\n.. _pip: https://pip.pypa.io/\n.. _human-readable.readthedocs.io: https://human-readable.readthedocs.io\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n',
    'author': "Thiago Carvalho D'Ávila",
    'author_email': 'thiagocavila@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/staticdev/human-readable',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
