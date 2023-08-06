# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_trpglogger']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.13,<2.0.0', 'nonebot2>=2.0.0-alpha.9,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-trpglogger',
    'version': '0.1.5',
    'description': 'a logger for TRPG',
    'long_description': '# TRPGLogger\n\n*基于 [nonebot2](https://github.com/nonebot/nonebot2) 以及 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的 QQ 跑团记录记录器*\n\n[![License](https://img.shields.io/github/license/thereisnodice/TRPGLogger)](LICENSE)\n![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)\n![NoneBot Version](https://img.shields.io/badge/nonebot-2+-red.svg)\n![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-trpglogger.svg)\n\n用来记录跑团记录的 nonebot2 插件，与 https://logpainter.kokona.tech 配合使用\n\n*移植自 [Dice-Developer-Team/TrpgLogger](https://github.com/Dice-Developer-Team/TrpgLogger)*\n\n### 安装\n\n* 使用nb-cli（推荐）  \n\n```bash\nnb plugin install nonebot_plugin_trpglogger\n```\n\n* 使用poetry\n\n```bash\npoetry add nonebot_plugin_trpglogger\n```\n\n### 开始使用\n\n`.log on` 开始记录\n\n`.log off` 停止记录\n\n**一个群同一时间段不能存在两个记录且无法暂停！**\n\n### TO DO\n\n- [ ] 暂停记录\n- [ ] 多开记录\n\n<details>\n<summary>展开更多</summary>\n\n### 原理\n\n与 TrpgLogger 一样，使用 AWS S3 进行储存（目前是直接用溯洄的公共 bucket ）。\n\n### Bug\n\n- 无法记录机器人本身发出的消息（即无法记录掷骰）  \n **如何解决:** 等 nonebot2 更新 a11\n\n</details>\n',
    'author': 'Jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thereisnodice/TRPGLogger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
