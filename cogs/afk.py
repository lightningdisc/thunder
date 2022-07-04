import discord
from discord.ext import commands
import aiosqlite

class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online!")
        setattr(self.bot, "db", await aiosqlite.connect("main.db"))
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS afk (user INTEGER, guild INTEGER, reason TEXT)")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT reason FROM afk WHERE user = ? AND guild = ?", (message.author.id, message.guild.id,))
            data = await cursor.fetchone()
            if data:
                await message.channel.send(f"{message.author.mention}: Welcome back from your AFK dude!")
                await cursor.execute("DELETE FROM afk WHERE user = ? AND guild = ?", (message.author.id, message.guild.id,))
            if message.mentions:
                for mention in message.mentions:
                    await cursor.execute("SELECT reason FROM afk WHERE user = ? AND guild = ?", (mention.id, message.guild.id,))
                    data2 = await cursor.fetchone()
                    if data2 and mention.id != message.author.id:
                        await message.channel.send(f"{mention.name} is afk! Reason: `{data2[0]}`")
        await self.bot.db.commit()

    @commands.command()
    async def afk(self, ctx, *, reason=None):
        if reason == None:
            reason = "No reason provided."
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT reason FROM afk WHERE user = ? AND guild = ?", (ctx.author.id, ctx.guild.id,))
            data = await cursor.fetchone()
            if data:
                if data[0] == reason:
                    return await ctx.send("You are already afk fwith the same reason bro.")
                await cursor.execute("UPDATE afk SET reason = ? WHERE user = ? AND guild = ?", (reason, ctx.author.id, ctx.guild.id,))
            else:
                await cursor.execute("INSERT INTO afk (user, guild, reason) VALUES (?, ?, ?)", (ctx.author.id, ctx.guild.id, reason,))
                await ctx.reply(f"You are now afk for `{reason}`!")
        await self.bot.db.commit()

def setup(bot):
    bot.add_cog(Afk(bot))