from VersaLog import *
from dotenv import load_dotenv
from discord.ext import commands

import discord
import os

from api import (
    event_rotation,
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
async def playerinfo(ctx, tag: str):
    data = await player(tag)

    if not data:
        await ctx.send(t["fetch_error"])
        return

    embed = discord.Embed(
        title=f"👤 {data['name']}",
        color=0x3498db
    )

    embed.add_field(name="🏆 Trophy", value=data["trophies"])
    embed.add_field(name="📈 Highest", value=data["highestTrophies"])
    embed.add_field(name="⭐ Level", value=data["expLevel"])

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