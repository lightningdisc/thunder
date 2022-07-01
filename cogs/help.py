import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Help:", description="Help page for Thunder.")
        embed.add_field(name="General Commands.", value="!help (shows this command)", inline=False)
        embed.add_field(name="Lightning Support:", value="!lightning setup\n!lightning settings\n!lightning captcharole\n!lightning accountage\n!lightning antinudity\n!lightning antiprofanity\n!lightning antispam\n!lightning allowspam\n!lightning locking\n!lightning kick\n!lightning ban\n!lightning prefix\n!lightning language\n!lightning userinfo")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))