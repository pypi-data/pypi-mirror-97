[![PyPI version](https://badge.fury.io/py/blue-chip.svg)](https://badge.fury.io/py/httpxy)
[![Coverage Status](https://coveralls.io/repos/github/Kilo59/httpxy/badge.svg?branch=master)](https://coveralls.io/github/Kilo59/httpxy?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


# httpxy
HTTP client with yaml support

Adds minor convenience features to the excellent [`httpx`](https://www.python-httpx.org/) library which aims to make working with `yaml` easier and safer.

## Installation

```
pip install httpxy
```

## Features
* Always use `safe_load()`. `DONE`
* `Response` objects have a `response.yaml()` for deserializing YAML to a `dict`. `DONE`
* Automatic serialization of objects to yaml. `TODO`
* Automatic deserializing of yaml to python objects/classes/models. `TODO`
* Works with multiple yaml packages. `TODO`


## Examples

### Deserialize directly from `Response` objects.

Equivalent to `response.json()`.

```python
import httpxy
from pprint import pprint

response = httpxy.get("https://mockbin.org/request", headers={"accept": "application/yaml"})

dict_from_yaml = response.yaml()

pprint(dict_from_yaml, sort_dicts=False, depth=1)
```

```python
    {'startedDateTime': '2021-03-06T19:54:03.157Z',
     'clientIPAddress': '99.99.999.999',
     'method': 'GET',
     'url': 'https://mockbin.org/request',
     'httpVersion': 'HTTP/1.1',
     'cookies': None,
     'headers': {...},
     'queryString': {},
     'postData': {...},
     'headersSize': 559,
     'bodySize': 0}

```

```python
print(response.text)
```

```yaml
    startedDateTime: '2021-03-06T19:54:03.157Z'
    clientIPAddress: 99.99.999.999
    method: GET
    url: 'https://mockbin.org/request'
    httpVersion: HTTP/1.1
    cookies:
    headers:
      host: mockbin.org
      connection: close
      accept-encoding: gzip
      x-forwarded-proto: http
      cf-visitor: '{"scheme":"https"}'
      accept: application/yaml
      user-agent: python-httpx/0.17.0
    queryString: {}
    postData:
      mimeType: application/octet-stream
      text: ""
      params: []
    headersSize: 559
    bodySize: 0
```
