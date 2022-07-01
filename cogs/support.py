import discord
from discord.ext import commands

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def lightning(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Invalid Command!", description="This command does not exist on Lightning!", color=0xe00000)
            return await ctx.send(embed=embed)

    @lightning.command()
    async def setup(self, ctx):
        embed = discord.Embed(title="Setup Command", description="")
        embed.add_field(name="Command Info:", value="This command will setup the Captcha system in your server. This command will create a verification channel, make a role that can **ONLY** see the verification a channel, and finally a bot logs channel.", inline=False)
        embed.add_field(name="Permissions Needed:", value="Administrator", inline=False)
        embed.add_field(name="Syntax:", value="```\n?setup <on/off>\n```\nThen say *yes* or *no* to confirm the captcha.")
        await ctx.send(embed=embed)

    @lightning.command()
    async def settings(self, ctx):
        embed=discord.Embed(title="Settings Command")
        embed.add_field(name="Command Info:", value="This command will simply show you the settings of the guilds' bot settings.", inline=False)
        embed.add_field(name="Permissions Needed:", value="Administrator", inline=False)
        embed.add_field(name="Syntax", value="```\n?settings\n```")
        await ctx.send(embed=embed)

    @lightning.command()
    async def captcharole(self, ctx):
        embed = discord.Embed(title="Giveroleaftercaptcha Command")
        embed.add_field(name="Command Info:", value="This command will give a role to the member after they pass Captcha (refer to `!lightning setup` for that).", inline=False)
        embed.add_field(name="Permissions Needed:", value="Administrator", inline=False)
        embed.add_field(name="Syntax:", value="```\n?giveroleaftercaptcha <role ID/off>\n```\n(Pinging the captcha role here will not work)")
        await ctx.send(embed=embed)

    @lightning.command()
    async def accountage(self, ctx):
        embed = discord.Embed(title="Minaccountage Command")
        embed.add_field(name="Command Info:", value="The command will setup a number of hours the users account has to be registered to join the guild. The default setting for this is 24 hours.", inline=False)
        embed.add_field(name="Permissions Needed:", value="Administrator", inline=False)
        embed.add_field(name="Syntax:", value="```\n?minaccountage <number (hours)>\n```\n(It **HAS** to be hours)")
        await ctx.send(embed=embed)

    @lightning.command()
    async def antinudity(self, ctx):
        embed = discord.Embed(title="Antinudity Command")
        embed.add_field(name="Command Info:", value="This command will enable or enable or disable nsfw content in your guild.. This is enabled by default.", inline=False)
        embed.add_field(name="Permissions Needed:", value="Administrator", inline=False)
        embed.add_field(name="Syntax:", value="```\n?antinudity <true/false>\n```")
        await ctx.send(embed=embed)

    @lightning.command()
    async def antiprofanity(self, ctx):
        embed = discord.Embed(title="Antinudity Command")
        embed.add_field(name="Command Info:", value="This command will enable or disable the profanity content from your guild. This is enabled by default.", inline=False)
        embed.add_field(name="Permissions Needed:", value="Administrator", inline=False)
        embed.add_field(name="Syntax:", value="```\n?antiprofanity <true/false>\n```")
        await ctx.send(embed=embed)

    @lightning.command()
    async def antispam(self, ctx):
        embed = discord.Embed(name="Antispam Command")
        embed.add_field(name="Command Info:", value="This command will enable or disable the spam filter in your guild. This is enabled be default.", inline=False)
        embed.add_field(name="Permissions Needed:", value="Administrator", inline=False)
        embed.add_field(name="Syntax:", value="```\n?antispam <true/false>\n```")
        await ctx.send(embed=embed)

    @lightning.command()
    async def allowspam(self, ctx):
        embed = discord.Embed(title="Allowspam Command")
        embed.add_field(name="Command Info:", value="This command will ignore a text channel from the antispam setting if it is enabled.", inline=False)
        embed.add_field(name="Permissions Needed:", value="Administrator", inline=False)
        embed.add_field(name="Syntax:", value="```\n?allowspam <#channel> (remove)\n```\n(You have to use a TextChannel, and you can whitelist multiple)")
        await ctx.send(embed=embed)

    @lightning.command()
    async def locking(self, ctx):
        embed = discord.Embed(title="Lock and Unlock Command")
        embed.add_field(name="Command Info:", value="This command will lock OR unlock a channel.", inline=False)
        embed.add_field(name="Permissions Needed:", value="Administrator", inline=False)
        embed.add_field(name="Syntax:", value="```\n?lock | unlock <#channel/ID>\n```\n")
        await ctx.send(embed=embed)

    @lightning.command()
    async def kick(self, ctx):
        embed = discord.Embed(title="Kick Command")
        embed.add_field(name="Command Info:", value="This command will kick a user out of the guild.", inline=False)
        embed.add_field(name="Permissions Needed:", value="Kick Members", inline=False)
        embed.add_field(name="Syntax:", value="```\n?kick <@user/ID> (reason)\n```\n")
        await ctx.send(embed=embed)

    @lightning.command()
    async def ban(self, ctx):
        embed = discord.Embed(title="Ban Command")
        embed.add_field(name="Command Info:", value="This command will ban a user out of the guild.", inline=False)
        embed.add_field(name="Permissions Needed:", value="Ban Members", inline=False)
        embed.add_field(name="Syntax:", value="```\n?ban <@user/ID> (reason)\n```\n")
        await ctx.send(embed=embed)

    @lightning.command()
    async def prefix(self, ctx):
        embed = discord.Embed(title="Changeprefix Command")
        embed.add_field(name="Command Info:", value="This command will change the preifx for the guild.", inline=False)
        embed.add_field(name="Permissions Needed:", value="Administrator", inline=False)
        embed.add_field(name="Syntax:", value="```\n?changeprefix <prefix>\n```\n")
        await ctx.send(embed=embed)

    @lightning.command()
    async def language(self, ctx):
        embed = discord.Embed(title="Changelanguage Command")
        embed.add_field(name="Command Info:", value="This command will change the language of the bot for the guild.", inline=False)
        embed.add_field(name="Permissions Needed:", value="Administrator", inline=False)
        embed.add_field(name="Syntax:", value="```\n?changelanguage <language>\n```\n(You can choose from English or French)")
        await ctx.send(embed=embed)

    @lightning.command()
    async def userinfo(self, ctx):
        embed = discord.Embed(title="Userinfo Command")
        embed.add_field(name="Command Info:", value="This command will show the users' information.", inline=False)
        embed.add_field(name="Permissions Needed:", value="None", inline=False)
        embed.add_field(name="Syntax:", value="```\n?userinfos <@user/ID>\n```\n")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Support(bot))