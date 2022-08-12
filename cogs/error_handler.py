from discord.ext import commands

class error_handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(ctx, exception):
        if isinstance(exception, commands.PrivateMessageOnly):
            await ctx.respond("This command is DM only")

    @commands.Cog.listener()
    async def on_application_command_error(ctx, exception):
        if isinstance(exception, commands.guild_only):
            await ctx.respond("This command is server only")

def setup(bot):
    bot.add_cog(error_handler(bot))