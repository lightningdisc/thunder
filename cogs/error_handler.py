from discord.ext import commands

class error_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        if isinstance(error, commands.errors.PrivateMessageOnly):
            await ctx.respond("This command is DM only!", ephemeral=True)

def setup(bot):
    bot.add_cog(error_handler(bot))