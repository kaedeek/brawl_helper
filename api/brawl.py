from VersaLog import *
from dotenv import load_dotenv
import os
import aiohttp

load_dotenv()

logger = VersaLog(enum="detailed", tag=["BASE", "API REQ"], show_tag=True)

APIKey = os.getenv("key")
API = "https://api.brawlstars.com/v1/"


async def request(endpoint: str):
    url = API + endpoint

    headers = {
        "Authorization": f"Bearer {APIKey}"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as req:

                if req.status == 200:
                    logger.info(f"取得成功: {endpoint}")
                    return await req.json()

                logger.error(f"{endpoint}: {req.status}")
                return None

    except Exception as e:
        logger.error(str(e))
        return None


# Events
async def event_rotation():
    return await request("events/rotation")


async def event_gamemodes():
    return await request("events/gamemodes")


# Brawlers
async def brawlers():
    return await request("brawlers")


async def brawler(id: int):
    return await request(f"brawlers/{id}")


# Players
async def player(tag: str):
    tag = tag.replace("#", "%23")
    return await request(f"players/{tag}")


async def player_battlelog(tag: str):
    tag = tag.replace("#", "%23")
    return await request(f"players/{tag}/battlelog")


# Clubs
async def club(tag: str):
    tag = tag.replace("#", "%23")
    return await request(f"clubs/{tag}")


async def club_members(tag: str):
    tag = tag.replace("#", "%23")
    return await request(f"clubs/{tag}/members")


# Rankings
async def ranking_players(country: str = "global"):
    return await request(f"rankings/{country}/players")


async def ranking_clubs(country: str = "global"):
    return await request(f"rankings/{country}/clubs")


async def ranking_brawlers(country: str, brawler_id: int):
    return await request(f"rankings/{country}/brawlers/{brawler_id}")