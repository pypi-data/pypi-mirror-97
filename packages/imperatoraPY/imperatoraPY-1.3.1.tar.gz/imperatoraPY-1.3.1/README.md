# imperatoraPY - Imperator API wrapper written in Python

[![widget](https://inv.wtf/widget/myerfire)](https://myer.wtf/discord)

Maintained by [Myer (also known as myerfire, MyerFire)](https://github.com/myerfire)

- [YouTube](https://myer.wtf/youtube)
- [Twitter](https://myer.wtf/twitter)
- myer#0001 on Discord

This library is a fully featured async wrapper for the [Imperator API](https://docs.imperator.network/api). 

## Installation

`imperatoraPY` is available from the official pYpI package index.

`python -m pip install -U imperatoraPY`

## Documentation

- There are relevant docstrings on the functions of the main wrapper class.
- Object attribute documentation may (?) be worked on but the code
  in [objects.py](https://github.com/MyerFire/imperatoraPY/blob/master/imperatoraPY/objects.py) is easily readable.

## Quick Start

```python
from imperatoraPY import Imperator
import asyncio

API_KEY = "hahagetbaited"
# if it isn't obvious enough, replace this string 
# with your API key obtained by going onto the Imperator server and running /api

async def main():
    imperator = await Imperator(API_KEY)
    player = imperator.fetch.player(name="myerfire")
    print(player.nation)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
```