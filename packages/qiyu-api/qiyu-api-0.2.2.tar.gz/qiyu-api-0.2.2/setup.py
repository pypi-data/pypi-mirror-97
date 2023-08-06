# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qiyu_api',
 'qiyu_api.ali_sms_api',
 'qiyu_api.apns_sdk_py',
 'qiyu_api.dtk_api',
 'qiyu_api.mob_api',
 'qiyu_api.py_apple_signin',
 'qiyu_api.tbk_api',
 'qiyu_api.ztk_api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4',
 'cryptography>=3.0,<4.0',
 'dataclasses-json>=0.5,<0.6',
 'pydantic>=1.7,<2',
 'pydes>=2,<3',
 'pyjwt>=2.0,<3',
 'requests>=2.25,<3',
 'structlog>=21,<22']

setup_kwargs = {
    'name': 'qiyu-api',
    'version': '0.2.2',
    'description': '奇遇科技 Python API 合集',
    'long_description': '# QiYu-API\n\n[![Black Format Check](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/black-format.yml/badge.svg)](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/black-format.yml)\n[![CodeQL](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/codeql-analysis.yml)\n[![Poetry Publish](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/poetry_pypi.yml/badge.svg)](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/poetry_pypi.yml)\n[![Pylama Lint](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/pylama-lint.yml/badge.svg)](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/pylama-lint.yml)\n[![pytest](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/pytest.yml/badge.svg)](https://github.com/QiYuTechDev/qiyu-api/actions/workflows/pytest.yml)\n\n![PyPI - Version](https://img.shields.io/pypi/v/qiyu-api)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qiyu-api)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/qiyu-api)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/qiyu-api)\n![GitHub repo size](https://img.shields.io/github/repo-size/qiyutechdev/qiyu-api)\n![Lines of code](https://img.shields.io/tokei/lines/github/qiyutechdev/qiyu-api)\n\n奇遇科技 Python API 集合\n\n## 当前已经合并\n\n* ali_sms_api (阿里云短信)\n* apns_sdk_py (Apple APNs 推送)\n* dtk_api     (大淘客接口)\n* mob_api     (掌淘科技接口)\n* py_apple_signin (Apple Sign in 接口)\n* tbk_api (淘宝客标准化的类型)\n* ztk_api (折淘客接口)\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://oss.qiyutech.tech/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
