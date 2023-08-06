# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['structlog_sentry']

package_data = \
{'': ['*']}

install_requires = \
['sentry-sdk']

setup_kwargs = {
    'name': 'structlog-sentry',
    'version': '1.4.0',
    'description': 'Sentry integration for structlog',
    'long_description': '# structlog-sentry\n\n| What          | Where                                         |\n| ------------- | --------------------------------------------- |\n| Documentation | <https://github.com/kiwicom/structlog-sentry> |\n| Maintainer    | @kiwicom/platform                             |\n\nBased on <https://gist.github.com/hynek/a1f3f92d57071ebc5b91>\n\n## Installation\n\nInstall the package with [pip](https://pip.pypa.io/):\n\n```\npip install structlog-sentry\n```\n\n## Usage\n\nThis module is intended to be used with `structlog` like this:\n\n```python\nimport sentry_sdk\nimport structlog\nfrom structlog_sentry import SentryProcessor\n\n\nsentry_sdk.init()  # pass dsn in argument or via SENTRY_DSN env variable\n\nstructlog.configure(\n    processors=[\n        structlog.stdlib.add_logger_name,  # optional, but before SentryProcessor()\n        structlog.stdlib.add_log_level,  # required before SentryProcessor()\n        SentryProcessor(level=logging.ERROR),\n    ],\n    logger_factory=...,\n    wrapper_class=...,\n)\n\n\nlog = structlog.get_logger()\n```\n\nDo not forget to add the `structlog.stdlib.add_log_level` and optionally the\n`structlog.stdlib.add_logger_name` processors before `SentryProcessor`. The\n`SentryProcessor` class takes the following arguments:\n\n- `level` - events of this or higher levels will be reported to Sentry,\n  default is `WARNING`\n- `active` - default is `True`, setting to `False` disables the processor\n\nNow exceptions are automatically captured by Sentry with `log.error()`:\n\n```python\ntry:\n    1/0\nexcept ZeroDivisionError:\n    log.error()\n\ntry:\n    resp = requests.get(f"https://api.example.com/users/{user_id}/")\n    resp.raise_for_status()\nexcept RequestException:\n    log.error("request error", user_id=user_id)\n```\n\nThis won\'t automatically collect `sys.exc_info()` along with the message, if you want\nto enable this behavior, just pass `exc_info=True`.\n\nWhen you want to use structlog\'s built-in\n[`format_exc_info`](http://www.structlog.org/en/stable/api.html#structlog.processors.format_exc_info)\nprocessor, make that the `SentryProcessor` comes *before* `format_exc_info`!\nOtherwise, the `SentryProcessor` won\'t have an `exc_info` to work with, because\nit\'s removed from the event by `format_exc_info`.\n\nLogging calls with no `sys.exc_info()` are also automatically captured by Sentry:\n\n```python\nlog.info("info message", scope="accounts")\nlog.warning("warning message", scope="invoices")\nlog.error("error message", scope="products")\n```\n\nIf you do not want to forward logs into Sentry, just pass the `sentry_skip=True`\noptional argument to logger methods, like this:\n\n```python\nlog.error(sentry_skip=True)\n```\n\n### Sentry Tags\n\nYou can set some or all of key/value pairs of structlog `event_dict` as sentry `tags`:\n\n```python\nstructlog.configure(\n    processors=[\n        structlog.stdlib.add_logger_name,\n        structlog.stdlib.add_log_level,\n        SentryProcessor(level=logging.ERROR, tag_keys=["city", "timezone"]),\n    ],...\n)\n\nlog.error("error message", city="Tehran", timezone="UTC+3:30", movie_title="Some title")\n```\n\nthis will report the error and the sentry event will have **city** and **timezone** tags.\nIf you want to have all event data as tags, create the `SentryProcessor` with `tag_keys="__all__"`.\n\n```python\nstructlog.configure(\n    processors=[\n        structlog.stdlib.add_logger_name,\n        structlog.stdlib.add_log_level,\n        SentryProcessor(level=logging.ERROR, tag_keys="__all__"),\n    ],...\n)\n```\n\n### Skip Extra\n\nBy default `SentryProcessor` will send `event_dict` key/value pairs as extra info to the sentry.\nSometimes you may want to skip this, specially when sending the `event_dict` as sentry tags:\n\n```python\nstructlog.configure(\n    processors=[\n        structlog.stdlib.add_logger_name,\n        structlog.stdlib.add_log_level,\n        SentryProcessor(level=logging.ERROR, as_extra=False, tag_keys="__all__"),\n    ],...\n)\n```\n\n### Ignore specific loggers\n\nIf you want to ignore specific loggers from being processed by the `SentryProcessor` just pass\na list of loggers when instantiating the processor:\n\n```python\nstructlog.configure(\n    processors=[\n        structlog.stdlib.add_logger_name,\n        structlog.stdlib.add_log_level,\n        SentryProcessor(level=logging.ERROR, ignore_loggers=["some.logger"]),\n    ],...\n)\n```\n\n### Logging as JSON\n\nIf you want to configure `structlog` to format the output as **JSON**\n(maybe for [elk-stack](https://www.elastic.co/elk-stack)) you have to use `SentryJsonProcessor` to prevent\nduplication of an event reported to sentry.\n\n```python\nfrom structlog_sentry import SentryJsonProcessor\n\nstructlog.configure(\n    processors=[\n        structlog.stdlib.add_logger_name,  # required before SentryJsonProcessor()\n        structlog.stdlib.add_log_level,\n        SentryJsonProcessor(level=logging.ERROR, tag_keys="__all__"),\n        structlog.processors.JSONRenderer()\n    ],...\n)\n```\n\nThis processor tells sentry to *ignore* the logger and captures the events manually.\n\n## Testing\n\nTo run all tests:\n\n```\ntox\n```\n\n## Contributing\n\nCreate a merge request and tag @kiwicom/platform  for review.\n',
    'author': 'Kiwi.com platform',
    'author_email': 'platform@kiwi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kiwicom/structlog-sentry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
