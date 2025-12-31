import aiohttp

class LubeLoggerAPI:
    def __init__(self, base_url, username=None, password=None):
        self._base_url = base_url.rstrip("/")
        self._session = aiohttp.ClientSession()

        # Only create BasicAuth if BOTH username and password are provided
        if username and password:
            self._auth = aiohttp.BasicAuth(username, password)
        else:
            self._auth = None

    async def _get(self, path):
        url = f"{self._base_url}{path}"

        kwargs = {}
        if self._auth:
            kwargs["auth"] = self._auth

        async with self._session.get(url, **kwargs) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def get_vehicles(self):
        return await self._get("/api/vehicles")

    async def close(self):
        await self._session.close()
