from cProfile import label
import discord
from discord.ext import commands
from discord.ui import Modal, InputText
from config import tags_collection as tagCol

class test_modal(Modal):
    def __init__(self) -> None:
        super().__init__(title="Tag Setter")
        self.add_item(InputText(label="Name", placeholder="Name"))
        self.add_item(InputText(label="Description", style=discord.InputTextStyle.long, placeholder="Description"))

    async def callback(self, interaction:discord.Interaction):
        try:
            await tagCol.update_one({"_id": interaction.guild_id}, {"$set": {self.children[0].value: self.children[1].value}}, upsert=True)
        except:
            return await interaction.response.send_message("That tag exists!")
        embed = discord.Embed(title=f"Tag {self.children[0].value} set!", description=f"Type /tags {self.children[0].value} to view!")
        embed.set_footer(text="Brought to you by Thunder")
        await interaction.response.send_message(embed=embed)

class tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    tagCmd = discord.SlashCommandGroup(name="tags", description="tags commands")

    @tagCmd.command(description="sets a tag or updates an existing one")
    async def settag(self, interaction:discord.Interaction):
        modal = test_modal()
        await interaction.response.send_modal(modal)

    @tagCmd.command(description="view a specified tag")
    async def viewtag(self, ctx, tagname):
        data = tagCol.find({"_id": ctx.guild.id})
        async for tags in data:
            for key in tags.keys():
                if tagname == key.lower():
                    return await ctx.respond(tags[key])
        else:
            return await ctx.respond("Tag not found")

    @tagCmd.command(description="view all tag names")
    async def listall(self, ctx):
        data = tagCol.find({"_id": ctx.guild.id})
        tagstr = ""
        async for tags in data:
            for key in tags.keys():
                if key == "_id":
                    continue
                tagstr += f"{key}\n"
        embed = discord.Embed(title="Tag List", description=tagstr)
        embed.set_footer(text="Brought to you by Thunder")
        await ctx.respond(embed=embed)

    @tagCmd.command(description="remove a tag")
    async def remove(self, ctx, tag):
        data = tagCol.find({"_id": ctx.guild.id})
        async for tags in data:
            for keys in tags.keys():
                if keys.lower() == tag:
                    val = tags[keys]
                    tagCol.update_one({"_id": ctx.guild.id}, {"$unset": {keys: val}})
                    return await ctx.respond(f"Tag {tag} removed!")
        else:
            return await ctx.respond("Tag not found")

def setup(bot):
    bot.add_cog(tags(bot))