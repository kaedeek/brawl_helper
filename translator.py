from VersaLog import *
import aiohttp
import json
import os

logger = VersaLog(enum="detailed", tag=["BASE", "TRANSLATOR"], show_tag=True)


def load_json(path: str):
    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


async def translate_and_save(
    text: str,
    file_path: str,
    target: str = "ja"
):
    cache = load_json(file_path)

    if text in cache:
        logger.info(f"Cache hit: {text}")
        return cache[text]

    url = "https://libretranslate.com/translate"

    payload = {
        "q": text,
        "source": "en",
        "target": target,
        "format": "text"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload
            ) as resp:

                data = await resp.json()

                translated = data.get(
                    "translatedText",
                    text
                )

                cache[text] = translated
                save_json(file_path, cache)

                logger.info(
                    f"Saved: {text} -> {translated}"
                )

                return translated

    except Exception as e:
        logger.error(str(e))
        return text