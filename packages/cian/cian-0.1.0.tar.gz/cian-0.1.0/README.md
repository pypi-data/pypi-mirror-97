# Cian
[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/OlegYurchik/aiocian/blob/master/LICENSE)
[![built with Python3](https://img.shields.io/badge/built%20with-Python3-red.svg)](https://www.python.org/)
## Description
Unofficial library for interaction with [Cian](https://cian.ru)

Contents
=================
* [Release Notes](#release-notes)
  * [0.0.1](#version-0-0-1)
  * [0.1.0](#version-0-1-0)
* [Getting Started](#getting-started)
  * [Installation from pip](#installation-from-pip)
  * [Installation from GitHub](#installation-from-github)
  * [Quick Start](#quick-start)
## Release Notes
### Version 0.0.1
* Created library
* Add simple search
### Version 0.1.0
* Rename library - from `aiocian` to `cian`
* Restructured library - make library closer with Cian API
* Edit constants - now constants is `enum.Enum` instance
* Delete heavy logic creation request data
* Delete creation `Result` object - now return `dict` object
* Add empty tests
## Getting Started
### Installation from pip
```bash
pip install cian
```
### Installation from GitHub
```bash
git clone https://github.com/OlegYurchik/cian.git
cd cian
```
and
```
pip install .
```
or
```bash
python setup.py install
```
### Quick Start
After installation, you can use the library in your code. 

Sync example

```python
from cian import CianClient, constants


def main(cian_client):
    for offer in cian_client.search(
            region=constants.Region.SPB,
            ad_type=constants.AdType.FLAT_SALE,
    ):
        print(result["fullUrl"])


if __name__ == "__main__":
    cian_client = CianClient()
    main(cian_client)
```

Async example:

```python
import asyncio

from cian import CianClient, constants


async def main(cian_client):
    async for offer in cian_client.search(
            region=constants.Region.SPB,
            ad_type=constants.AdType.FLAT_SALE,
    ):
        print(result["fullUrl"])


if __name__ == "__main__":
    cian_client = CianClient()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(cian_client))
    loop.close()
```