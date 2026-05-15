from VersaLog import *
from dotenv import load_dotenv
from discord.ext import commands

import discord
import os

from api import (
    event_rotation,
    brawler,
    brawlers,
    player,
    club,
    ranking_players
)

from i18n import get_text, tr
from translator import translate_and_save

load_dotenv()

logger = VersaLog(
    enum="detailed",
    tag="BASE",
    show_tag=True
)

TOKEN = os.getenv("token")

LANG = "ja"
t = get_text(LANG)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


@bot.event
async def on_ready():
    logger.info(f"{bot.user} で起動しました")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "❌ コマンドが見つかりません。\n`!help` を確認してください。"
        )
        return

    raise error


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📘 Brawl Stars Bot Help",
        description="利用可能なコマンド一覧",
        color=0x5865F2
    )

    commands_list = [
        ("📅 イベント", "`!events`\n現在のイベント一覧"),
        ("👤 プレイヤー情報", "`!playerinfo TAG`\n例: `!playerinfo ABC123`"),
        ("🦸 所持キャラクター", "`!roster TAG`\n例: `!roster ABC123`"),
        ("🦸 キャラ一覧", "`!brawlerslist`"),
        ("🦸 キャラ詳細", "`!brawlerinfo ID`\n例: `!brawlerinfo 16000000`"),
        ("🔎 キャラ検索", "`!brawlersearch 名前`\n例: `!brawlersearch Shelly`"),
        ("🏰 クラブ情報", "`!clubinfo TAG`"),
        ("🏆 ランキング", "`!ranking`")
    ]

    for name, value in commands_list:
        embed.add_field(
            name=name,
            value=value,
            inline=False
        )

    embed.set_footer(text="Brawl Stars Discord Bot")
    await ctx.send(embed=embed)


@bot.command()
async def events(ctx):
    data = await event_rotation()

    if not data:
        await ctx.send(t["fetch_error"])
        return

    embed = discord.Embed(
        title=t["events_title"],
        color=0xffcc00
    )

    for item in data[:10]:
        event = item["event"]

        mode = tr(t, "modes", event["mode"])

        map_name = await translate_and_save(
            event["map"],
            "locales/maps_ja.json"
        )

        embed.add_field(
            name=f"🎮 {mode}",
            value=f"🗺️ {map_name}",
            inline=False
        )

    await ctx.send(embed=embed)


@bot.command()
async def brawlerslist(ctx):
    data = await brawlers()

    if not data:
        await ctx.send(t["fetch_error"])
        return

    embed = discord.Embed(
        title="🦸 キャラクター一覧",
        color=0x9b59b6
    )

    names = []

    for item in data["items"]:
        name_ja = await translate_and_save(
            item["name"],
            "locales/brawlers_ja.json"
        )
        names.append(name_ja)

    embed.description = "\n".join(names[:30])
    await ctx.send(embed=embed)


@bot.command()
async def brawlerinfo(ctx, id: str):
    data = await brawler(id)

    if not data:
        await ctx.send(t["fetch_error"])
        return

    name_ja = await translate_and_save(
        data.get("name", "Unknown"),
        "locales/brawlers_ja.json"
    )

    embed = discord.Embed(
        title=f"🦸 {name_ja}",
        description=f"ID: {data.get('id', 'Unknown')}",
        color=0xf1c40f
    )

    rarity = data.get("rarity", {}).get("name", "不明")

    star_powers = []
    for sp in data.get("starPowers", []):
        sp_name = await translate_and_save(
            sp["name"],
            "locales/brawlers_ja.json"
        )
        star_powers.append(f"⭐ {sp_name}")

    gadgets = []
    for g in data.get("gadgets", []):
        g_name = await translate_and_save(
            g["name"],
            "locales/brawlers_ja.json"
        )
        gadgets.append(f"⚙️ {g_name}")

    embed.add_field(
        name="🏅 レア度",
        value=rarity,
        inline=True
    )

    embed.add_field(
        name="⭐ スターパワー",
        value="\n".join(star_powers) or "なし",
        inline=False
    )

    embed.add_field(
        name="⚙️ ガジェット",
        value="\n".join(gadgets) or "なし",
        inline=False
    )

    image_url = data.get("imageUrl2") or data.get("imageUrl")
    if image_url:
        embed.set_thumbnail(url=image_url)

    await ctx.send(embed=embed)


@bot.command()
async def brawlersearch(ctx, *, name: str):
    data = await brawlers()

    if not data:
        await ctx.send(t["fetch_error"])
        return

    for item in data["items"]:
        if item["name"].lower() == name.lower():
            await brawlerinfo(ctx, str(item["id"]))
            return

    await ctx.send("見つかりませんでした")


@bot.command()
async def playerinfo(ctx, tag: str):
    data = await player(tag)

    if not data:
        await ctx.send(t["fetch_error"])
        return

    favorite = data.get(
        "favoriteBrawler",
        {}
    ).get("name", "なし")

    if favorite != "なし":
        favorite = await translate_and_save(
            favorite,
            "locales/brawlers_ja.json"
        )

    embed = discord.Embed(
        title=f"👤 {data.get('name', 'Unknown')}",
        description=f"Tag: {data.get('tag', 'Unknown')}",
        color=0x3498db
    )

    embed.add_field(name="🏆 トロフィー", value=data.get("trophies", 0))
    embed.add_field(name="📈 最高", value=data.get("highestTrophies", 0))
    embed.add_field(name="⭐ レベル", value=data.get("expLevel", 0))
    embed.add_field(name="⚔️ 3v3", value=data.get("3vs3Victories", 0))
    embed.add_field(name="🥇 ソロ", value=data.get("soloVictories", 0))
    embed.add_field(name="👥 デュオ", value=data.get("duoVictories", 0))
    embed.add_field(name="❤️ Favorite", value=favorite, inline=False)

    icon_id = data.get("icon", {}).get("id")
    if icon_id:
        embed.set_thumbnail(
            url=f"https://cdn.brawlify.com/profile-icons/regular/{icon_id}.png"
        )

    await ctx.send(embed=embed)


@bot.command()
async def roster(ctx, tag: str):
    data = await player(tag)

    if not data:
        await ctx.send(t["fetch_error"])
        return

    embed = discord.Embed(
        title=f"🦸 {data['name']} の所持キャラクター一覧",
        color=0x9b59b6
    )

    brawlers_data = sorted(
        data.get("brawlers", []),
        key=lambda x: x["trophies"],
        reverse=True
    )

    for b in brawlers_data[:10]:
        name_ja = await translate_and_save(
            b["name"],
            "locales/brawlers_ja.json"
        )

        embed.add_field(
            name=f"{name_ja} (ランク {b['rank']})",
            value=(
                f"🏆 現在: {b['trophies']}\n"
                f"📈 最高: {b['highestTrophies']}\n"
                f"⚡ パワー: {b['power']}"
            ),
            inline=False
        )

    top = brawlers_data[0]
    embed.set_thumbnail(
        url=f"https://cdn.brawlify.com/brawlers/borders/{top['id']}.png"
    )

    embed.set_footer(
        text=f"全 {len(brawlers_data)} キャラクター"
    )

    await ctx.send(embed=embed)


@bot.command()
async def clubinfo(ctx, tag: str):
    data = await club(tag)

    if not data:
        await ctx.send(t["fetch_error"])
        return

    embed = discord.Embed(
        title=f"🏰 {data['name']}",
        color=0x2ecc71
    )

    embed.add_field(name="👥 メンバー", value=data["membersCount"])
    embed.add_field(name="🏆 トロフィー", value=data["trophies"])

    await ctx.send(embed=embed)


@bot.command()
async def ranking(ctx):
    data = await ranking_players("jp")

    if not data:
        await ctx.send(t["fetch_error"])
        return

    embed = discord.Embed(
        title=t["ranking_title"],
        color=0xe74c3c
    )

    for user in data["items"][:10]:
        embed.add_field(
            name=f"{user['rank']}. {user['name']}",
            value=f"🏆 {user['trophies']}",
            inline=False
        )

    await ctx.send(embed=embed)


bot.run(TOKEN)