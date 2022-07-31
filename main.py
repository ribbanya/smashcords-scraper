import asyncio
import os
import platform
import re
from functools import reduce
from typing import Union, List

import aiohttp
import json

from aiohttp import ClientSession

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

DISCORD_API_INVITE_URL = "https://discordapp.com/api/invite/"

INVITE_RE = re.compile(r"(?:(?:https?\:\/\/)?discord\.gg\/)?([\da-zA-Z]+)")


def deep_get(dictionary, *keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys, dictionary)


async def get_guild_from_invite(session: ClientSession, invite_code: str) -> dict:
    async with session.get(DISCORD_API_INVITE_URL + invite_code) as response:
        data = await response.text()
        json_data = json.loads(data)

        return {
            "id": deep_get(json_data, "guild", "id"),
            "name": deep_get(json_data, "guild", "name")
        }


async def parse_smashcords(session: ClientSession, acc: dict, path: Union[str, bytes, os.PathLike]):
    root: List[dict]
    with open(path, "r") as f:
        root = json.load(f)
    for category in root:
        category_name = category.get("name")
        category_type = category.get("type")

        for server in category.get("Servers", []):
            server_name = server.get("name")
            invite_url = server.get("destination")
            invite_code = None if not invite_url else INVITE_RE.match(invite_url).group(1)
            guild = {}
            # guild = await get_guild_from_invite(session, invite_code)
            # await asyncio.sleep(1)
            result = {
                "smashcords_category": category_name,
                "smashcords_name": server_name,
                "invite_code": invite_code,
            }
            result.update(guild)
            print(result)


async def main():
    async with aiohttp.ClientSession() as session:
        await parse_smashcords(session, {}, r"data/smashcords.json")


if __name__ == '__main__':
    asyncio.run(main())
