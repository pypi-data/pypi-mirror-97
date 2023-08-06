# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hyperglass',
 'hyperglass.api',
 'hyperglass.api.examples',
 'hyperglass.cache',
 'hyperglass.cli',
 'hyperglass.compat',
 'hyperglass.configuration',
 'hyperglass.execution',
 'hyperglass.execution.drivers',
 'hyperglass.external',
 'hyperglass.models',
 'hyperglass.models.api',
 'hyperglass.models.commands',
 'hyperglass.models.config',
 'hyperglass.models.parsing',
 'hyperglass.parsing',
 'hyperglass.util']

package_data = \
{'': ['*'],
 'hyperglass': ['examples/*',
                'images/*',
                'ui/*',
                'ui/components/*',
                'ui/components/card/*',
                'ui/components/countdown/*',
                'ui/components/footer/*',
                'ui/components/form/*',
                'ui/components/greeting/*',
                'ui/components/header/*',
                'ui/components/help/*',
                'ui/components/label/*',
                'ui/components/layout/*',
                'ui/components/markdown/*',
                'ui/components/output/*',
                'ui/components/path/*',
                'ui/components/results/*',
                'ui/components/select/*',
                'ui/components/submit/*',
                'ui/components/table/*',
                'ui/components/util/*',
                'ui/context/*',
                'ui/hooks/*',
                'ui/pages/*',
                'ui/public/*',
                'ui/types/*',
                'ui/util/*']}

install_requires = \
['Pillow>=7.0.0,<8.0.0',
 'PyJWT>=1.7.1,<2.0.0',
 'PyYAML>=5.3,<6.0',
 'aiofiles>=0.5.0,<0.6.0',
 'aredis>=1.1.7,<2.0.0',
 'click>=7.0,<8.0',
 'cryptography==3.0.0',
 'distro>=1.5.0,<2.0.0',
 'fastapi>=0.59,<0.60',
 'favicons>=0.0.9,<0.0.10',
 'gunicorn>=20.0.4,<21.0.0',
 'httpx>=0.11,<0.12',
 'inquirer>=2.6.3,<3.0.0',
 'loguru>=0.4.0,<0.5.0',
 'netmiko>=3.3.2,<4.0.0',
 'paramiko>=2.7.1,<3.0.0',
 'psutil>=5.7.2,<6.0.0',
 'py-cpuinfo>=7.0.0,<8.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'redis>=3.5.3,<4.0.0',
 'scrapli[asyncssh]>=2020.9.26,<2021.0.0',
 'uvicorn>=0.11,<0.12',
 'uvloop>=0.14.0,<0.15.0',
 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['hyperglass = hyperglass.console:CLI']}

setup_kwargs = {
    'name': 'hyperglass',
    'version': '1.0.0b80',
    'description': 'hyperglass is the modern network looking glass that tries to make the internet better.',
    'long_description': '<div align="center">\n  <br/>\n  <img src="https://res.cloudinary.com/hyperglass/image/upload/v1593916013/logo-light.svg" width=300></img>\n  <br/>\n  <h3>The network looking glass that tries to make the internet better.</h3>\n  <br/>  \n  A looking glass is implemented by network operators as a way of providing customers, peers, or the general public with a way to easily view elements of, or run tests from the provider\'s network.\n</div>\n\n<hr/>\n\n<div align="center">\n\n[**Documentation**](https://hyperglass.io)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[**Screenshots**](https://hyperglass.io/screenshots)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[**Live Demo**](https://demo.hyperglass.io/)\n\n[![PyPI](https://img.shields.io/pypi/v/hyperglass?style=for-the-badge)](https://pypi.org/project/hyperglass/)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/hyperglass?color=%2340798C&style=for-the-badge)\n\n[![GitHub Contributors](https://img.shields.io/github/contributors/checktheroads/hyperglass?color=40798C&style=for-the-badge)](https://github.com/checktheroads/hyperglass)\n[![Gitter](https://img.shields.io/gitter/room/checktheroads/hyperglass?color=ff5e5b&style=for-the-badge)](https://gitter.im/hyperglass)\n[![Telegram](https://img.shields.io/badge/chat-telegram-blue?style=for-the-badge&color=blue&logo=telegram)](https://t.me/hyperglasslg)\n\n[![Frontend Tests](https://img.shields.io/github/workflow/status/checktheroads/hyperglass/Frontend%20Testing?label=Frontend%20Tests&style=for-the-badge)](https://github.com/checktheroads/hyperglass/actions?query=workflow%3A%Frontend+Testing%22)\n[![Backend Tests](https://img.shields.io/github/workflow/status/checktheroads/hyperglass/Backend%20Testing?label=Backend%20Tests&style=for-the-badge)](https://github.com/checktheroads/hyperglass/actions?query=workflow%3A%Backend+Testing%22)\n[![Installer Tests](https://img.shields.io/github/workflow/status/checktheroads/hyperglass/Installer%20Testing?label=Installer%20Tests&style=for-the-badge)](https://github.com/checktheroads/hyperglass/actions?query=workflow%3A%Installer+Testing%22)\n\n<br/>\n\nhyperglass is intended to make implementing a looking glass too easy not to do, with the lofty goal of improving the internet community at large by making looking glasses more common across autonomous systems of any size.\n\n<br/>\n\n⚠️ **v1.0.0** *is currently in beta. While everything should work, some things might not. Documentation and the live demo are not yet complete. For a fully working and documented version of hyperglass, **please go to the [v0 branch](https://github.com/checktheroads/hyperglass/tree/v0)**.*\n\n</div>\n\n### [Changelog](https://github.com/checktheroads/hyperglass/blob/v1.0.0/CHANGELOG.md)\n\n## Features\n\n- BGP Route, BGP Community, BGP AS Path, Ping, & Traceroute\n- Full IPv6 support\n- Customizable everything: features, theme, UI/API text, error messages, commands\n- Built in support for:\n    - Arista EOS\n    - BIRD\n    - Cisco IOS-XR\n    - Cisco IOS/IOS-XE\n    - Cisco NX-OS\n    - FRRouting\n    - Huawei\n    - Juniper JunOS\n    - Mikrotik\n    - Nokia SR OS\n    - TNSR\n    - VyOS\n- Configurable support for any other [supported platform](https://hyperglass.io/docs/platforms)\n- Optionally access devices via an SSH proxy/jump server\n- VRF support\n- Access List/prefix-list style query control to whitelist or blacklist query targets on a per-VRF basis\n- REST API with automatic, configurable OpenAPI documentation\n- Modern, responsive UI built on [ReactJS](https://reactjs.org/), with [NextJS](https://nextjs.org/) & [Chakra UI](https://chakra-ui.com/), written in [TypeScript](https://www.typescriptlang.org/)\n- Query multiple devices simultaneously\n- Browser-based DNS-over-HTTPS resolution of FQDN queries\n\n*To request support for a specific platform, please [submit a Github Issue](https://github.com/checktheroads/hyperglass/issues/new) with the **enhancement** label.*\n\n### [Get Started →](https://hyperglass.io/)\n\n## Community\n\n- [Telegram](https://t.me/hyperglasslg)\n- [Gitter](https://gitter.im/hyperglass)\n- [Twitter](https://twitter.com/checktheroads)\n- [Keybase](https://keybase.io/team/hyperglass)\n\nAny users, potential users, or contributors of hyperglass are welcome to join and discuss usage, feature requests, bugs, and other things.\n\n**hyperglass is developed with the express intention of being free to the networking community**.\n\n*However, the hyperglass demo does cost [@checktheroads](https://github.com/checktheroads) $60/year for the [hyperglass.io](https://hyperglass.io) domain. If you\'re feeling particularly helpful and want to help offset that cost, small donations are welcome.*\n\n[![Donate](https://img.shields.io/badge/Donate-blue.svg?logo=paypal&style=for-the-badge)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZQFH3BB2B5M3E&source=url)\n\n## Acknowledgements\n\nhyperglass is built entirely on open-source software. Here are some of the awesome libraries used, check them out too!\n\n- [FastAPI](https://fastapi.tiangolo.com/)\n- [Netmiko](https://github.com/ktbyers/netmiko)\n- [Scrapli](https://github.com/carlmontanari/scrapli)\n- [Pydantic](https://pydantic-docs.helpmanual.io/)\n- [Chakra UI](https://chakra-ui.com/)\n\n[![GitHub](https://img.shields.io/github/license/checktheroads/hyperglass?color=330036&style=for-the-badge)](https://github.com/checktheroads/hyperglass/blob/v1.0.0/LICENSE)\n',
    'author': 'Matt Love',
    'author_email': 'matt@hyperglass.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hyperglass.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
