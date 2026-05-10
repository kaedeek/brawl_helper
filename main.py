from VersaLog import *
from dotenv import load_dotenv
from discord.ext import commands

import discord
import os

from api import (
    event_rotation,
    event_gamemodes,
    player,
    club,
    ranking_players
)

load_dotenv()

logger = VersaLog(enum="detailed", tag="BASE", show_tag=True)

TOKEN = os.getenv("token")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    logger.info(f"{bot.user} で起動しました")


@bot.command()
async def events(ctx):
    data = await event_rotation()

    if not data:
        await ctx.send("取得失敗")
        return

    embed = discord.Embed(
        title="📅 Brawl Stars Events",
        color=0xffcc00
    )

    for item in data[:10]:
        event = item["event"]

        embed.add_field(
            name=f"🎮 {event['mode']}",
            value=f"🗺️ {event['map']}",
            inline=False
        )

    await ctx.send(embed=embed)


@bot.command()
async def playerinfo(ctx, tag: str):
    data = await player(tag)

    if not data:
        await ctx.send("取得失敗")
        return

    embed = discord.Embed(
        title=f"👤 {data['name']}",
        color=0x3498db
    )

    embed.add_field(
        name="🏆 Trophy",
        value=data["trophies"],
        inline=True
    )

    embed.add_field(
        name="📈 Highest",
        value=data["highestTrophies"],
        inline=True
    )

    embed.add_field(
        name="⭐ Level",
        value=data["expLevel"],
        inline=True
    )

    await ctx.send(embed=embed)


@bot.command()
async def clubinfo(ctx, tag: str):
    data = await club(tag)

    if not data:
        await ctx.send("取得失敗")
        return

    embed = discord.Embed(
        title=f"🏰 {data['name']}",
        color=0x2ecc71
    )

    embed.add_field(
        name="👥 Members",
        value=data["membersCount"],
        inline=True
    )

    embed.add_field(
        name="🏆 Trophy",
        value=data["trophies"],
        inline=True
    )

    await ctx.send(embed=embed)


@bot.command()
async def ranking(ctx):
    data = await ranking_players("jp")

    if not data:
        await ctx.send("取得失敗")
        return

    embed = discord.Embed(
        title="🏆 Japan Ranking",
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