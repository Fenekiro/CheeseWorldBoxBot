import asyncio
import discord

from app.config.config import config

token = config.data.discord.bot_token
bot = discord.Bot(discord_intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("OK")


bot.load_extension("app.discord_api.cogs.games")
bot.load_extension("app.discord_api.cogs.players")
bot.load_extension("app.discord_api.cogs.wars")
bot.load_extension("app.discord_api.cogs.researches")


bot.run(token)
