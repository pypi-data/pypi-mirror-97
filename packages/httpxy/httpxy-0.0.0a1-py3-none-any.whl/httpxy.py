"""
httpxy
~~~~~
httpx with native yaml support.
"""

from typing import Any, Dict, List, Union

from httpx import *  # pylint: disable=unused-wildcard-import,wildcard-import
from yaml import dump, safe_load

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper


def _yaml(self, **load_kwargs: Any) -> Any:
    """Deserialize the content using `PyYaml` `safe_load()`."""
    return safe_load(self.content, **load_kwargs)


def _dump_yaml(content: Union[bytes, Dict, List]) -> str:
    return dump(content, Dumper=Dumper)


setattr(Response, "yaml", _yaml)

# pylint: disable=fixme
# TODO: client.request() -> logic goes here
# TODO: request() - yaml kw
# TODO: post(), put(), patch() - yaml kw
# TODO: stream? probably not

if __name__ == "__main__":
    pass
