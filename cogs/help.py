import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Help:", description="Help page for Thunder.")
        embed.add_field(name="General Commands.", value=
        """
        `!help` - Shows this message
        `!starboard` - Set up the starboard
        `!afk` - Go afk
        `!logging` - set up logging
        """)
        embed.add_field(name="Tags", value=
        """
        `!!support`
        `!!bug`
        `!!hunter`
        `!!dontask`
        `!!known
        """)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))