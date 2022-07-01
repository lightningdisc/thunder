import discord 
from discord.ext import commands
from datetime import datetime
import aiosqlite

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        setattr(self.bot, "db", await aiosqlite.connect("main.db"))
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS logging (channel INTEGER, guild INTEGER)")
        await self.bot.db.commit()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild = message.guild
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM logging WHERE guild = ?", (guild.id,))
            channel = await cursor.fetchone()
            msgDelete = self.bot.get_channel(channel[0])
            embed = discord.Embed(title = f"{message.author}'s Message was Deleted", description = f"Deleted Message: {message.content}\nAuthor: {message.author.mention}", timestamp = datetime.now(), color = discord.Colour.red())
            embed.set_author(name = message.author.name, icon_url = message.author.display_avatar)
            embed.set_footer(text=str(message.author.id))
            await msgDelete.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        guild = before.guild
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM logging WHERE guild = ?", (guild.id,))
            channel = await cursor.fetchone()
            msgEdit = self.bot.get_channel(channel[0])
            embed = discord.Embed(title = f"{before.author} Edited Their Message", description = f"Before: {before.content}\nAfter: {after.content}\nAuthor: {before.author.mention}\n", timestamp = datetime.now(), color = discord.Colour.blue())
            embed.set_author(name = after.author.name, icon_url = after.author.display_avatar)
            embed.set_footer(text=str(before.author.id))
            await msgEdit.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild = before.guild
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM logging WHERE guild = ?", (guild.id,))
            channel = await cursor.fetchone()
            memUpdate = self.bot.get_channel(channel[0])
            if len(before.roles) > len(after.roles):
                role = next(role for role in before.roles if role not in after.roles)
                embed = discord.Embed(title = f"{before}'s Role has Been Removed", description = f"{role.mention} was removed from {before.mention}.",  timestamp = datetime.now(), color = discord.Colour.red())
            elif len(after.roles) > len(before.roles):
                role = next(role for role in after.roles if role not in before.roles)
                embed = discord.Embed(title = f"{before} Got a New Role", description = f"{role.mention} was added to {before.mention}.",  timestamp = datetime.now(), color = discord.Colour.green())
            elif before.nick != after.nick:
                embed = discord.Embed(title = f"{before}'s Nickname Changed", description = f"Before: {before.nick}\nAfter: {after.nick}",  timestamp = datetime.now(), color = discord.Colour.blue())
            else:
                return
            embed.set_author(name = after.name, icon_url = after.display_avatar)
            #embed.set_footer(text=str(before.author.id))
            await memUpdate.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM logging WHERE guild = ?", (guild.id,))
            channelID = await cursor.fetchone()
            chanCreate = self.bot.get_channel(channelID[0])
            embed = discord.Embed(title = f"{channel.name} was Created", description = channel.mention, timestamp = datetime.now(), color = discord.Colour.green())
            await chanCreate.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = channel.guild
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM logging WHERE guild = ?", (guild.id,))
            channelID = await cursor.fetchone()
            chanDelete = self.bot.get_channel(channelID[0])
            embed = discord.Embed(title = f"{channel.name} was Deleted", timestamp = datetime.now(), color = discord.Colour.red())
            await chanDelete.send(embed=embed)

    @commands.group()
    async def logging(self, ctx):
        return

    @logging.command()
    @commands.has_permissions(manage_guild=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM logging WHERE guild = ?", (ctx.guild.id,))
            channelData = await cursor.fetchone()
            if channelData:
                channelData = channelData[0]
                if channelData == channel.id:
                    return await ctx.send("That's the same channel bro.")
                await cursor.execute("UPDATE logging SET channel = ? WHERE guild = ?", (channel.id, ctx.guild.id,))
                await ctx.send(f"{channel.mention} is now the logging channel.")
            else:
                await cursor.execute("INSERT INTO logging VALUES (?, ?)", (channel.id, ctx.guild.id,))
                await ctx.send(f"{channel.mention} is now the logging channel.")
        await self.bot.db.commit()

def setup(bot):
    bot.add_cog(Logs(bot))