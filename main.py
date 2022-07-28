import asyncio
import platform
from functools import reduce
import aiohttp
import json

from aiohttp import ClientSession

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

DISCORD_API_INVITE_URL = "https://discordapp.com/api/invite/"


def deep_get(dictionary, *keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys, dictionary)


async def get_invite_name(session: ClientSession, invite_code: str) -> str:
    async with session.get(DISCORD_API_INVITE_URL + invite_code) as response:
        data = await response.text()
        json_data = json.loads(data)
        return deep_get(json_data, "guild", "name")


async def main():
    async with aiohttp.ClientSession() as session:
        print(await get_invite_name(session, "4jpjZkB"))


if __name__ == '__main__':
    asyncio.run(main())
