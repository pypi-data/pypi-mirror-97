import aiohttp

from .errors import APIError, ClientError, NotFound

BASE_URL = "http://192.145.238.5/~pasirm5/v3/sessyoin"


class HttpClient:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def get(self, endpoint: str, **kwargs):
        try:
            async with self.session.get(f"{BASE_URL}/{endpoint}") as resp:
                if resp.status == 404:
                    raise NotFound()
                if resp.status != 200:
                    raise APIError(resp.status)
                return await resp.json(content_type=None)
        except aiohttp.ClientConnectionError:
            raise ClientError()
