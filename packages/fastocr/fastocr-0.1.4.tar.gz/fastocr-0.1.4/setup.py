# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastocr']

package_data = \
{'': ['*'],
 'fastocr': ['data/*',
             'i18n/*',
             'qml/*',
             'resource/icon/dark/*',
             'resource/icon/light/*']}

install_requires = \
['aiohttp', 'click', 'pyqt5', 'pyqt5-sip', 'qasync']

extras_require = \
{'dbus': ['dbus-python']}

entry_points = \
{'console_scripts': ['fastocr = fastocr.__main__:main']}

setup_kwargs = {
    'name': 'fastocr',
    'version': '0.1.4',
    'description': 'FastOCR is a desktop application for OCR API.',
    'long_description': None,
    'author': 'Bruce Zhang',
    'author_email': 'zttt183525594@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BruceZhang1993/FastOCR',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
