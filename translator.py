from VersaLog import *
import aiohttp

logger = VersaLog(enum="detailed", tag=["BASE", "TRANSLATOR"], show_tag=True)

CACHE = {}


async def translate(text: str, target="ja"):
    if text in CACHE:
        logger.info(f"Cache hit: {text}")
        return CACHE[text]

    url = "https://libretranslate.com/translate"

    payload = {
        "q": text,
        "source": "en",
        "target": target,
        "format": "text"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                data = await resp.json()

                translated = data.get(
                    "translatedText",
                    text
                )

                CACHE[text] = translated

                logger.info(
                    f"Translated: {text} -> {translated}"
                )

                return translated

    except Exception as e:
        logger.error(str(e))
        return text