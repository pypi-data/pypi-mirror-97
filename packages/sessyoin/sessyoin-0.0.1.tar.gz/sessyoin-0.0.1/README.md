# sessyoinAsync

async Python wrapper for [sessyoin](https://www.npmjs.com/package/sessyoin).


## Requirements

- aiohttp (>=3.6.2)

## Installation
```bash
pip install sessyoin
```

## Example

```py
import asyncio
from sessyoin import Client

client = Client()

async def main(category: str):
    result = await client.get_image(category)
    print(result)
    print(result.url)
    await client.teardown()

loop = asyncio.get_event_loop()
loop.run_until_complete(main("kemonomimi"))
