import discord
from discord.ext import commands
import aiosqlite
import asyncio
import os
from config import TOKEN

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    setattr(bot, "db", await aiosqlite.connect("main.db"))
    await asyncio.sleep(1)
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="!help | Lightning Support"))
    print("Online!")

for filename in os.listdir("cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(TOKEN)