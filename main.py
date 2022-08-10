import discord
import motor.motor_asyncio
import os
from dotenv import load_env

load_env()
token = os.getenv('BOT_TOKEN')
mongo_string = os.getenv('MONGO_CONNECT_STRING')
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_string)

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

@bot.slash_command(description="Pong!")
async def ping(ctx):
    await ctx.respond("Pong!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(token)