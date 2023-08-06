# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['httpxy']
install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'httpx>=0.17,<0.18']

setup_kwargs = {
    'name': 'httpxy',
    'version': '0.0.0a1',
    'description': 'HTTP client (httpx) with native yaml support.',
    'long_description': '[![PyPI version](https://badge.fury.io/py/blue-chip.svg)](https://badge.fury.io/py/httpxy)\n[![Coverage Status](https://coveralls.io/repos/github/Kilo59/httpxy/badge.svg?branch=master)](https://coveralls.io/github/Kilo59/httpxy?branch=master)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n\n# httpxy\nHTTP client with yaml support\n\nAdds minor convenience features to the excellent [`httpx`](https://www.python-httpx.org/) library which aims to make working with `yaml` easier and safer.\n\n## Installation\n\n```\npip install httpxy\n```\n\n## Features\n* Always use `safe_load()`. `DONE`\n* `Response` objects have a `response.yaml()` for deserializing YAML to a `dict`. `DONE`\n* Automatic serialization of objects to yaml. `TODO`\n* Automatic deserializing of yaml to python objects/classes/models. `TODO`\n* Works with multiple yaml packages. `TODO`\n\n\n## Examples\n\n### Deserialize directly from `Response` objects.\n\nEquivalent to `response.json()`.\n\n```python\nimport httpxy\nfrom pprint import pprint\n\nresponse = httpxy.get("https://mockbin.org/request", headers={"accept": "application/yaml"})\n\ndict_from_yaml = response.yaml()\n\npprint(dict_from_yaml, sort_dicts=False, depth=1)\n```\n\n```python\n    {\'startedDateTime\': \'2021-03-06T19:54:03.157Z\',\n     \'clientIPAddress\': \'99.99.999.999\',\n     \'method\': \'GET\',\n     \'url\': \'https://mockbin.org/request\',\n     \'httpVersion\': \'HTTP/1.1\',\n     \'cookies\': None,\n     \'headers\': {...},\n     \'queryString\': {},\n     \'postData\': {...},\n     \'headersSize\': 559,\n     \'bodySize\': 0}\n\n```\n\n```python\nprint(response.text)\n```\n\n```yaml\n    startedDateTime: \'2021-03-06T19:54:03.157Z\'\n    clientIPAddress: 99.99.999.999\n    method: GET\n    url: \'https://mockbin.org/request\'\n    httpVersion: HTTP/1.1\n    cookies:\n    headers:\n      host: mockbin.org\n      connection: close\n      accept-encoding: gzip\n      x-forwarded-proto: http\n      cf-visitor: \'{"scheme":"https"}\'\n      accept: application/yaml\n      user-agent: python-httpx/0.17.0\n    queryString: {}\n    postData:\n      mimeType: application/octet-stream\n      text: ""\n      params: []\n    headersSize: 559\n    bodySize: 0\n```\n',
    'author': 'Gabriel',
    'author_email': 'gabriel59kg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kilo59/httpxy',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
