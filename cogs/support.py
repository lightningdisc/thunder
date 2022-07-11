import discord
from discord.ext import commands

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "!!support":
            embed = discord.Embed(title="How can we help you?", description=
            """
            How can we help you? *I need help* is not a valid question. Please state specifically with what you need help with.
            """)
            await message.channel.send(embed=embed)
            return
        if message.content == "!!bug":
            embed = discord.Embed(title="Error", description="So you found an bug in Lightning? Please follow the format below to report it:")
            embed.add_field(name="How to Report:", value=
            """
            - What is the error?
            - What is it breaking?
            - What is the severity of this error?
            - How can we reproduce this error?

            (Please note that you will get the Bug Hunter role based on certain conditions.)

            **Do NOT share the bug with anyone else BESIDES the Lightning Team and the Administrators.**
            """)
            await message.channel.send(embed=embed)
            return
        if message.content == "!!hunter":
            embed = discord.Embed(title="Bug Hunter", description=
            """
            The bug hunter role is for the peole who find bugs in our bot to make the bot better.
            """)
            embed.add_field(name="How to get Bug Hunter:", value=
            """
            - Bug must have a moderate to high severity. 
            - Must be in the bot.
            - Must be a new bug, not a one that is already known.
            - Must be able to reproduce it for us or show us how to reproduce the bug.

            (Please note that this role will **NOT** give you any special permissions.)

            **If you abuse this in ways such as attemping to get clout/attention from the developers or bragging about the role **WILL** be removed.**
            """)
            await message.channel.send(embed=embed)
            return
        if message.content == "!!dontask":
            embed = discord.Embed(title="Don't ask to ask to ask", description="Just ask.")
            await message.channel.send(embed=embed)
            return
        if message.content == "!!known":
            embed = discord.Embed(title="Known Bugs.", description="This bug is already known, no need to report it again.")
            await message.channel.send(embed=embed)
            return
            

def setup(bot):
    bot.add_cog(Support(bot))