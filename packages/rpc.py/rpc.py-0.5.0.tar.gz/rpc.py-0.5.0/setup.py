# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rpcpy']

package_data = \
{'': ['*']}

install_requires = \
['baize>=0.1.0,<0.2.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.7.4,<4.0.0'],
 'cbor': ['cbor2>=5.2.0,<6.0.0'],
 'client': ['httpx>=0.16.0,<0.17.0'],
 'full': ['cbor2>=5.2.0,<6.0.0',
          'httpx>=0.16.0,<0.17.0',
          'msgpack>=1.0.0,<2.0.0',
          'pydantic>=1.7,<2.0'],
 'msgpack': ['msgpack>=1.0.0,<2.0.0'],
 'type': ['pydantic>=1.7,<2.0']}

setup_kwargs = {
    'name': 'rpc.py',
    'version': '0.5.0',
    'description': 'An fast and powerful RPC framework based on ASGI/WSGI.',
    'long_description': '# rpc.py\n\n[![Codecov](https://img.shields.io/codecov/c/github/abersheeran/rpc.py?style=flat-square)](https://codecov.io/gh/abersheeran/rpc.py)\n\nAn fast and powerful RPC framework based on ASGI/WSGI.\n\nBased on WSGI/ASGI, you can deploy the rpc.py server to any server and use http2 to get better performance.\n\n## Install\n\nInstall from PyPi:\n\n```bash\npip install rpc.py\n\n# need use client\npip install rpc.py[client]\n\n# need use pydantic type hint or OpenAPI docs\npip install rpc.py[type]\n\n# need use msgpack to serializer\npip install rpc.py[msgpack]\n\n# need use CBOR to serializer\npip install rpc.py[cbor]\n\n# or install all dependencies\npip install rpc.py[full]\n```\n\nInstall from github:\n\n```bash\npip install git+https://github.com/abersheeran/rpc.py@setup.py\n```\n\n## Usage\n\n### Server side:\n\n<details markdown="1">\n<summary>Use <code>ASGI</code> mode to register <code>async def</code>...</summary>\n\n```python\nfrom typing import AsyncGenerator\n\nimport uvicorn\nfrom rpcpy import RPC\nfrom rpcpy.typing import TypedDict\n\napp = RPC(mode="ASGI")\n\n\n@app.register\nasync def none() -> None:\n    return\n\n\n@app.register\nasync def sayhi(name: str) -> str:\n    return f"hi {name}"\n\n\n@app.register\nasync def yield_data(max_num: int) -> AsyncGenerator[int, None]:\n    for i in range(max_num):\n        yield i\n\n\nD = TypedDict("D", {"key": str, "other-key": str})\n\n\n@app.register\nasync def query_dict(value: str) -> D:\n    return {"key": value, "other-key": value}\n\n\nif __name__ == "__main__":\n    uvicorn.run(app, interface="asgi3", port=65432)\n```\n</details>\n\nOR\n\n<details markdown="1">\n<summary>Use <code>WSGI</code> mode to register <code>def</code>...</summary>\n\n```python\nfrom typing import Generator\n\nimport uvicorn\nfrom rpcpy import RPC\nfrom rpcpy.typing import TypedDict\n\napp = RPC()\n\n\n@app.register\ndef none() -> None:\n    return\n\n\n@app.register\ndef sayhi(name: str) -> str:\n    return f"hi {name}"\n\n\n@app.register\ndef yield_data(max_num: int) -> Generator[int, None, None]:\n    for i in range(max_num):\n        yield i\n\n\nD = TypedDict("D", {"key": str, "other-key": str})\n\n\n@app.register\ndef query_dict(value: str) -> D:\n    return {"key": value, "other-key": value}\n\n\nif __name__ == "__main__":\n    uvicorn.run(app, interface="wsgi", port=65432)\n```\n</details>\n\n### Client side:\n\nNotice: Regardless of whether the server uses the WSGI mode or the ASGI mode, the client can freely use the asynchronous or synchronous mode.\n\n<details markdown="1">\n<summary>Use <code>httpx.Client()</code> mode to register <code>def</code>...</summary>\n\n```python\nfrom typing import Generator\n\nimport httpx\nfrom rpcpy.client import Client\nfrom rpcpy.typing import TypedDict\n\napp = Client(httpx.Client(), base_url="http://127.0.0.1:65432/")\n\n\n@app.remote_call\ndef none() -> None:\n    ...\n\n\n@app.remote_call\ndef sayhi(name: str) -> str:\n    ...\n\n\n@app.remote_call\ndef yield_data(max_num: int) -> Generator[int, None, None]:\n    yield\n\n\nD = TypedDict("D", {"key": str, "other-key": str})\n\n\n@app.remote_call\ndef query_dict(value: str) -> D:\n    ...\n```\n</details>\n\nOR\n\n<details markdown="1">\n<summary>Use <code>httpx.AsyncClient()</code> mode to register <code>async def</code>...</summary>\n\n```python\nfrom typing import AsyncGenerator\n\nimport httpx\nfrom rpcpy.client import Client\nfrom rpcpy.typing import TypedDict\n\napp = Client(httpx.AsyncClient(), base_url="http://127.0.0.1:65432/")\n\n\n@app.remote_call\nasync def none() -> None:\n    ...\n\n\n@app.remote_call\nasync def sayhi(name: str) -> str:\n    ...\n\n\n@app.remote_call\nasync def yield_data(max_num: int) -> AsyncGenerator[int, None]:\n    yield\n\n\nD = TypedDict("D", {"key": str, "other-key": str})\n\n\n@app.remote_call\nasync def query_dict(value: str) -> D:\n    ...\n```\n</details>\n\n### Sub-route\n\nIf you need to deploy the rpc.py server under `example.com/sub-route/*`, you need to set `RPC(prefix="/sub-route/")` and modify the `Client(base_path=https://example.com/sub-route/)`.\n\n### Serialization\n\nCurrently supports three serializers, JSON, Pickle and Msgpack. JSON is used by default. You can override the default `JSONSerializer` with parameters.\n\n```python\nimport httpx\nfrom rpcpy import RPC\nfrom rpcpy.client import Client\nfrom rpcpy.serializers import PickleSerializer, MsgpackSerializer\n\nRPC(response_serializer=MsgpackSerializer())\n# Or\nClient(\n    ...,\n    request_serializer=PickleSerializer(),\n)\n```\n\n## Type hint and OpenAPI Doc\n\nThanks to the great work of [pydantic](https://pydantic-docs.helpmanual.io/), which makes rpc.py allow you to use type annotation to annotate the types of function parameters and response values, and perform type verification and JSON serialization . At the same time, it is allowed to generate openapi documents for human reading.\n\n### OpenAPI Documents\n\nIf you want to open the OpenAPI document, you need to initialize `RPC` like this `RPC(openapi={"title": "TITLE", "description": "DESCRIPTION", "version": "v1"})`.\n\nThen, visit the `"{prefix}openapi-docs"` of RPC and you will be able to see the automatically generated OpenAPI documentation. (If you do not set the `prefix`, the `prefix` is `"/"`)\n\n## Limitations\n\nCurrently, file upload is not supported, but you can do this by passing a `bytes` object.\n',
    'author': 'abersheeran',
    'author_email': 'me@abersheeran.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abersheeran/rpc.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
