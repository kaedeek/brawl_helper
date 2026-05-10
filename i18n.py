from locales.ja import TEXT as JA
from locales.en import TEXT as EN


LANGUAGES = {
    "ja": JA,
    "en": EN
}


def get_text(lang="ja"):
    return LANGUAGES.get(lang, JA)


def tr(texts: dict, category: str, key: str):
    return texts.get(category, {}).get(key, key)

def missing(texts: dict, category: str, key: str):
    return key not in texts.get(category, {})