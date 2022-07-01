import discord
from discord.ext import commands
import aiosqlite

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        setattr(self.bot, "db", await aiosqlite.connect("main.db"))
        await self.bot.wait_until_ready()
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS starSetup (starLimit INTEGER, channel INTEGER, guild INTEGER)")
        await self.bot.db.commit()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji
        guild = self.bot.get_guild(payload.guild_id)
        channel = await guild.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if emoji.name == "⭐":
            async with self.bot.db.cursor() as cursor:
                await cursor.execute("SELECT starLimit, channel FROM starSetup WHERE guild = ?", (guild.id,))
                data = await cursor.fetchone()
                if data:
                    starData = data[0]
                    channelData = await guild.fetch_channel(data[1])
                    for reaction in message.reactions:
                        if reaction.emoji == "⭐":
                            if reaction.count >= starData:
                                embed = discord.Embed(title="New Starboard message:", description=f"{message.content}")
                                try:
                                    embed.set_image(url=message.attachments[0].url)
                                except:
                                    pass
                                embed.set_author(name="Message Link:", url=message.jump_url, icon_url=message.author.avatar.url)
                                embed.set_footer(text=f"Message ID: {message.id} | Author: {message.author.name}")
                                await channelData.send(embed=embed)

    @commands.group()
    async def starboard(ctx):
        return

    @starboard.command()
    @commands.has_permissions(manage_guild=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT channel FROM starSetup WHERE guild = ?", (ctx.guild.id,))
            channelData = await cursor.fetchone()
            if channelData:
                channelData = channelData[0]
                if channelData == channel.id:
                    return await ctx.send("That's the same channel bro.")
                await cursor.execute("UPDATE starSetup SET channel = ? WHERE guild = ?", (channel.id, ctx.guild.id,))
                await ctx.send(f"{channel.mention} is now the starboard channel.")
            else:
                await cursor.execute("INSERT INTO starSetup VALUES (?, ?, ?)", (5, channel.id, ctx.guild.id,))
                await ctx.send(f"{channel.mention} is now the starboard channel.")
        await self.bot.db.commit()

    @starboard.command()
    @commands.has_permissions(manage_guild=True)
    async def stars(self, ctx, star: int):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT starLimit FROM starSetup WHERE guild = ?", (ctx.guild.id,))
            starData = await cursor.fetchone()
            if starData:
                starData = starData[0]
                if starData == star:
                    return await ctx.send("That's already the star limit bro.")
                await cursor.execute("UPDATE starSetup SET starLimit = ? WHERE guild = ?", (star, ctx.guild.id,))
                await ctx.send(f"**{star}** is now the star limit.")
            else:
                await cursor.execute("INSERT INTO starSetup VALUES (?, ?, ?)", (star, 0, ctx.guild.id,))
                await ctx.send(f"**{star}** is now the star limit.")
        await self.bot.db.commit()

def setup(bot):
    bot.add_cog(Starboard(bot))