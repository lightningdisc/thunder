import discord
import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('BOT_TOKEN')
mongo_string = os.getenv('MONGO_CONNECT_STRING')
guild_id = os.getenv('COMMS_GUILD_ID')
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(mongo_string)

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

for files in os.listdir("./cogs"):
    if files.endswith(".py"):
        cogName = files[:-3]
        bot.load_extension(f"cogs.{cogName}")
        print(f"{cogName} initialized!")

@bot.slash_command(description="Pong!")
async def ping(ctx):
    await ctx.respond("Pong!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(token)