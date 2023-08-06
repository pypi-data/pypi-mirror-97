# cabulAsync

async Python wrapper for [cabul](https://www.npmjs.com/package/cabul).


## Requirements

- aiohttp (>=3.6.2)

## Installation
```bash
pip install cabul
```

## Example

```py
import asyncio
from cabul import Client

client = Client()

async def main(category: str):
    result = await client.get_image(category)
    print(result)
    print(result.url)
    await client.teardown()

loop = asyncio.get_event_loop()
loop.run_until_complete(main("cabul"))
