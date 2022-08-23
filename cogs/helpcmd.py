import discord
from discord.ext import commands

class helpcmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="help")
    async def help_cmd(self, ctx):
        embed = discord.Embed(title="Help", description="See below for help commands.")
        embed.set_footer(text="Brought to you by Thunder")
        embed.add_field(
            name="modmail",
            value="`setup` (BOT ADMINS ONLY)\n`openticket`\n`sendmessage`\n`adminrespond` (BOT ADMINS ONLY)\n"
        )
        embed.add_field(
            name="tags",
            value="`settag`\n`viewtag`\n`listall`\n`remove`"
        )
        embed.add_field(
            name="misc",
            value="`docs`\n`ping`"
        )
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(helpcmd(bot))