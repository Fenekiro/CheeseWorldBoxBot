import asyncio

import discord

token = "MTM5MjI4OTE4MDk3Njk0MzE3NA.G5YIuO.5mIKtrID9DwONdXfEDrphnFkMZvrgx9_brc5pw"
bot = discord.Bot(discord_intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("OK")


bot.load_extension("app.discord_api.cogs.games")
bot.load_extension("app.discord_api.cogs.players")
bot.load_extension("app.discord_api.cogs.wars")
bot.load_extension("app.discord_api.cogs.researches")


bot.run(token)
