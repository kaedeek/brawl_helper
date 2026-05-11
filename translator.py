from VersaLog import *
import aiohttp
import json

logger = VersaLog(
    enum="detailed",
    tag=["TRANSLATOR"],
    show_tag=True
)

MAP_FILE = "locales/maps_ja.json"


def load_cache():
    try:
        with open(MAP_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_cache(cache: dict):
    with open(MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(
            cache,
            f,
            ensure_ascii=False,
            indent=4
        )


CACHE = load_cache()


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
                save_cache(CACHE)

                logger.info(
                    f"Saved: {text} -> {translated}"
                )

                return translated

    except Exception as e:
        logger.error(str(e))
        return text