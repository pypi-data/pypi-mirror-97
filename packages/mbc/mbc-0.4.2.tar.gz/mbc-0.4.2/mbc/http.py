import aiohttp
import asyncio
from mbc.exceptions import *


class ApiClient:
    def __init__(self, api_key: str, **kwargs):
        self.loop = kwargs.get("loop") or asyncio.get_event_loop()
        self.session = kwargs.get("session") or aiohttp.ClientSession(loop=self.loop)
        self.base_url: str = ""
        self.api_key: str = api_key

        if not self.api_key:
            raise Unauthorized("You didn't provide an api key")

    async def request(self, method: str, endpoint: str, **kwargs):
        kwargs["headers"] = {
            "Authorization": self.api_key
        }

        async with self.session.request(method, self.base_url+endpoint, **kwargs) as response:
            if 300 > response.status >= 200:
                return await response.json()

            if response.status == 404:
                raise NotFound(response)
            elif response.status == 400:
                raise BadRequest(response)
            elif response.status == 403:
                raise Forbidden(response)
            else:
                raise ServerError(response)

    async def get_bot(self, bot_id: int) -> dict:
        return await self.request("GET", f"/bots/{bot_id}")

    async def get_bots(self, limit: int = 20, skip: int = 0) -> list:
        return await self.request(
            "GET",
            f"/bots",
            params={"limit": limit, "skip": skip}
        )

    async def get_bumps(self, bot_id: int) -> list:
        return await self.request("GET", f"/bots/{bot_id}/bumps")

    async def get_bumps_count(self, bot_id: int) -> dict:
        return await self.request("GET", f"/bots/{bot_id}/bumps/count")

    async def get_comments(self, bot_id: int) -> list:
        return await self.request("GET", f"/comments/{bot_id}")

    async def get_user_reports(self, user_id: int) -> list:
        return await self.request("GET", f"/reports/{user_id}")

    async def get_reports(self) -> list:
        return await self.request("GET", f"/reports")

    async def get_user(self, user_id: int) -> dict:
        return await self.request("GET", f"/users/{user_id}")

    async def get_user_bots(self, user_id: int) -> list:
        return await self.request("GET", f"/users/{user_id}/bots")

    async def get_bot_stats(self, bot_id: int) -> list:
        return await self.request("GET", f"/bots/{bot_id}/stats")

    async def get_bot_stat(self, bot_id: int) -> dict:
        return await self.request("GET", f"/bots/{bot_id}/stat")

    async def post_bot_stat(self, bot_id: int, guilds: int, users: int, shards: int = 0):
        return await self.request(
            "POST",
            f"/bots/{bot_id}/stats",
            json={
                "guilds": guilds,
                "users": users,
                "shards": shards
            }
        )

    async def close(self):
        await self.session.close()