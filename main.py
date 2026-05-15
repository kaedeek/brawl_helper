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
from translator import translate

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

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📘 Brawl Stars Bot Help",
        description="利用可能なコマンド一覧",
        color=0x5865F2
    )

    embed.add_field(
        name="📅 イベント",
        value="`!events`\n現在のイベント一覧を表示",
        inline=False
    )

    embed.add_field(
        name="🦸 キャラクター一覧",
        value="`!brawlerslist`",
        inline=False
    )
    
    embed.add_field(
        name="🦸 キャラクター詳細",
        value="`!brawlerinfo ID`",
        inline=False
    )
    
    embed.add_field(
        name="🔎 キャラクター検索",
        value="`!brawlersearch 名前`",
        inline=False
    )

    embed.add_field(
        name="👤 プレイヤー情報",
        value="`!playerinfo #TAG`\nプレイヤー情報を表示",
        inline=False
    )

    embed.add_field(
        name="🏰 クラブ情報",
        value="`!clubinfo #TAG`\nクラブ情報を表示",
        inline=False
    )

    embed.add_field(
        name="🏆 ランキング",
        value="`!ranking`\n日本ランキング表示",
        inline=False
    )

    embed.set_footer(
        text="Brawl Stars Discord Bot"
    )

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
        map_name = tr(t, "maps", event["map"])

        if map_name == event["map"]:
            map_name = await translate(event["map"])

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
        title="🦸 Brawlers",
        color=0x9b59b6
    )

    names = []

    for item in data["items"]:
        names.append(item["name"])

    embed.description = "\n".join(names[:30])

    await ctx.send(embed=embed)

@bot.command()
async def brawlerinfo(ctx, id: str):
    data = await brawler(id)

    if not data:
        await ctx.send(t["fetch_error"])
        return

    embed = discord.Embed(
        title=f"🦸 {data.get('name', 'Unknown')}",
        description=f"ID: {data.get('id', 'Unknown')}",
        color=0xf1c40f
    )

    rarity = data.get("rarity", {}).get(
        "name",
        "不明"
    )

    star_powers = "\n".join(
        [
            f"⭐ {sp['name']}"
            for sp in data.get("starPowers", [])
        ]
    ) or "なし"

    gadgets = "\n".join(
        [
            f"⚙️ {g['name']}"
            for g in data.get("gadgets", [])
        ]
    ) or "なし"

    hypercharge = "なし"

    if "hypercharge" in data:
        hypercharge = data["hypercharge"].get(
            "name",
            "あり"
        )

    embed.add_field(
        name="🏅 レア度",
        value=rarity,
        inline=True
    )

    embed.add_field(
        name="⭐ スターパワー",
        value=star_powers,
        inline=False
    )

    embed.add_field(
        name="⚙️ ガジェット",
        value=gadgets,
        inline=False
    )

    embed.add_field(
        name="⚡ ハイパーチャージ",
        value=hypercharge,
        inline=False
    )

    image_url = (
        data.get("imageUrl2")
        or data.get("imageUrl")
    )

    if image_url:
        embed.set_thumbnail(url=image_url)

    embed.set_footer(
        text="Brawl Stars Character Info"
    )

    await ctx.send(embed=embed)

@bot.command()
async def brawlersearch(ctx, *, name: str):
    data = await brawlers()

    if not data:
        await ctx.send(t["fetch_error"])
        return

    name = name.lower()

    for item in data["items"]:
        if item["name"].lower() == name:
            await brawlerinfo(
                ctx,
                str(item["id"])
            )
            return

    await ctx.send("見つかりませんでした")

@bot.command()
async def playerinfo(ctx, tag: str):
    data = await player(tag)

    if not data:
        await ctx.send(t["fetch_error"])
        return

    embed = discord.Embed(
        title=f"👤 {data.get('name', 'Unknown')}",
        description=f"Tag: {data.get('tag', 'Unknown')}",
        color=0x3498db
    )

    embed.add_field(
        name="🏆 トロフィー",
        value=data.get("trophies", 0),
        inline=True
    )

    embed.add_field(
        name="📈 最高トロフィー",
        value=data.get("highestTrophies", 0),
        inline=True
    )

    embed.add_field(
        name="⭐ レベル",
        value=data.get("expLevel", 0),
        inline=True
    )

    embed.add_field(
        name="⚔️ 3v3勝利",
        value=data.get("3vs3Victories", 0),
        inline=True
    )

    embed.add_field(
        name="🥇 ソロ勝利",
        value=data.get("soloVictories", 0),
        inline=True
    )

    embed.add_field(
        name="👥 デュオ勝利",
        value=data.get("duoVictories", 0),
        inline=True
    )

    club_name = "なし"
    if data.get("club"):
        club_name = data["club"].get(
            "name",
            "なし"
        )

    embed.add_field(
        name="🏰 クラブ",
        value=club_name,
        inline=False
    )

    favorite = data.get(
        "favoriteBrawler",
        {}
    ).get(
        "name",
        "なし"
    )

    embed.add_field(
        name="❤️ Favorite Brawler",
        value=favorite,
        inline=False
    )

    icon_id = data.get(
        "icon",
        {}
    ).get("id")

    if icon_id:
        embed.set_thumbnail(
            url=f"https://cdn.brawlify.com/profile-icons/regular/{icon_id}.png"
        )

    embed.set_footer(
        text="Brawl Stars Player Info"
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

    embed.add_field(name="👥 Members", value=data["membersCount"])
    embed.add_field(name="🏆 Trophy", value=data["trophies"])

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