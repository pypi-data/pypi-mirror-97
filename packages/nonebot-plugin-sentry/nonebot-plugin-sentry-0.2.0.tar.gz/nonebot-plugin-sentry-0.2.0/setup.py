# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '..'}

packages = \
['nonebot_plugin_sentry']

package_data = \
{'': ['*'], 'nonebot_plugin_sentry': ['dist/*']}

install_requires = \
['nonebot2>=2.0.0-alpha.6,<3.0.0', 'sentry-sdk>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-sentry',
    'version': '0.2.0',
    'description': 'Push your bot errors to Sentry.io',
    'long_description': '<!--\n * @Author         : yanyongyu\n * @Date           : 2020-11-23 20:23:12\n * @LastEditors    : yanyongyu\n * @LastEditTime   : 2020-11-23 22:15:54\n * @Description    : None\n * @GitHub         : https://github.com/yanyongyu\n-->\n\n<p align="center">\n  <a href="https://v2.nonebot.dev/">\n    <img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" height="100" alt="nonebot">\n  </a>\n  <a href="https://sentry.io">\n    <img src="https://sentry-brand.storage.googleapis.com/sentry-logo-black.png" height="100" alt="sentry">\n  </a>\n</p>\n\n<div align="center">\n\n# nonebot-plugin-sentry\n\n_✨ 在 Sentry.io 上进行 NoneBot 服务日志查看、错误处理 ✨_\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">\n    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-sentry">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-sentry.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">\n</p>\n\n## 使用方式\n\n填写必须配置项 `SENTRY_DSN` ，即刻开始 sentry 之旅！\n\n## 配置项\n\n配置项具体含义参考: [Sentry Docs](https://docs.sentry.io/platforms/python/configuration/options/)\n\n- `sentry_dsn: str`\n- `sentry_debug: bool = False`\n- `sentry_release: Optional[str] = None`\n- `sentry_release: Optional[str] = None`\n- `sentry_environment: Optional[str] = nonebot env`\n- `sentry_server_name: Optional[str] = None`\n- `sentry_sample_rate: float = 1.`\n- `sentry_max_breadcrumbs: int = 100`\n- `sentry_attach_stacktrace: bool = False`\n- `sentry_send_default_pii: bool = False`\n- `sentry_in_app_include: List[str] = Field(default_factory=lambda: [])`\n- `sentry_in_app_exclude: List[str] = Field(default_factory=lambda: [])`\n- `sentry_request_bodies: str = "medium"`\n- `sentry_with_locals: bool = True`\n- `sentry_ca_certs: Optional[str] = None`\n- `sentry_before_send: Optional[Callable[[Any, Any], Optional[Any]]] = None`\n- `sentry_before_breadcrumb: Optional[Callable[[Any, Any], Optional[Any]]] = None`\n- `sentry_transport: Optional[Any] = None`\n- `sentry_http_proxy: Optional[str] = None`\n- `sentry_https_proxy: Optional[str] = None`\n- `sentry_shutdown_timeout: int = 2`\n',
    'author': 'yanyongyu',
    'author_email': 'yanyongyu_1@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cscs181/QQ-GitHub-Bot/tree/master/src/plugins/nonebot_plugin_sentry',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
