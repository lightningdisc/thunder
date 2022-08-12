import discord
from discord.ext import commands
from main import guild_id
import asyncio
from discord.ui import View, Button, Modal, InputText
import os
import random
from datetime import datetime
from config import db_collection

class modmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    modmailCmds = discord.SlashCommandGroup(name="modmail", description="Thunder's Modmail Commands")

    @modmailCmds.command(name="setup", description="Sets up Modmail")
    @commands.guild_only()
    @discord.option(name="logchannel", description="channel to send transcripts, if left empty, one will be created.", required=False, default=None)
    async def mmsetup(self, ctx, logchannel: discord.TextChannel):
        if ctx.guild.id != int(guild_id):
            print(ctx.guild.id)
            print(guild_id)
            return await ctx.respond("You cannot run that command!")
        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond("You do not have the correct permissions!")
        if logchannel is None:
            guild = ctx.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False)
            }
            mmCategory = await guild.create_category(name="modmail", overwrites=overwrites)
            mmChannel = await guild.create_text_channel(name="modmail-logs", category=mmCategory, overwrites=overwrites)
            db_collection.insert_one({"_id": ctx.guild.id})
            db_collection.update_one({"_id": ctx.guild.id}, {"$set": {"mmChannel": mmChannel.id}}, upsert=True)
            db_collection.update_one({"_id": ctx.guild.id}, {"$set": {"mmCategory": mmCategory.id}}, upsert=True)
            await ctx.respond("Channels made!")
            await asyncio.sleep(1)
            embed = discord.Embed(title="Modmail Logs", description="Logs will be recorded here!")
            embed.set_footer(text="Brought to you by Thunder")
            await mmChannel.send(embed=embed)
            return

        elif logchannel is not None:
            mmChannel = logchannel
            mmCategory = mmChannel.category
            print(mmCategory)
            db_collection.insert_one({"_id": ctx.guild.id})
            db_collection.update_one({"_id": ctx.guild.id}, {"$set": {"mmChannel": mmChannel.id}}, upsert=True)
            db_collection.update_one({"_id": ctx.guild.id}, {"$set": {"mmCategory": mmCategory.id}}, upsert=True)
            await ctx.respond("This channel must be under a cateogory")
            await ctx.respond("Channels made!")
            await asyncio.sleep(1)
            embed = discord.Embed(title="Modmail Logs", description="Logs will be recorded here!")
            embed.set_footer(text="Brought to you by Thunder")
            await mmChannel.send(embed=embed)

    @modmailCmds.command(name="openticket", description="Opens a ticket with Thunder")
    @discord.option(name="reason", description="Reason for opening a ticket.", required=False, default=None)
    @commands.dm_only()
    async def open_ticket(self, ctx, reason):
        await ctx.defer()
        guild = self.bot.get_guild(int(guild_id))
        data = db_collection.find({"_id": int(guild_id)})

        overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False)
            }
            
        async for fields in data:
            category = fields["mmCategory"]
            channel = fields["mmChannel"]
        category = self.bot.get_channel(category)
        channel = self.bot.get_channel(channel)

        randID = random.randint(1000, 9999)
        ticketChannel = await category.create_text_channel(name=f"ticket {randID}", overwrites=overwrites)
        ticketChannelTarget = self.bot.get_channel(ticketChannel.id)
        db_collection.insert_one({"_id": ctx.author.id, "ticketID": ticketChannel.id})

        async def btn_callback(interaction):
            
            deleteEmbed = discord.Embed(title="Ticket Closed!", description="Your ticket has been closed. We hope your issue was resolved.")
            deleteEmbed.set_footer(text="Brought to you by Thunder")
            await dmChannel.send(embed=deleteEmbed)
            await interaction.response.send_message("Ticket Closed! this channel will be deleted momentarily.")
            await asyncio.sleep(1.75)

            logEmbed = discord.Embed(title=f"Ticket {randID} closed.", description=f"**Reason For Opening:** {reason}")
            logEmbed.set_footer(text="Brought to you by Thunder")
            logEmbed.timestamp = datetime.now()

            fileName = "log.txt"
            with open(fileName, "w") as file:
                async for msg in ticketChannelTarget.history(limit=None):
                    file.write(f"""{msg.created_at} - 
    {msg.author.display_name}: 
    {msg.clean_content}\n\n""")
            file = discord.File(fileName)
            await channel.send(embed=logEmbed, file=file)
            os.remove(fileName)

            await ticketChannelTarget.delete()  
            db_collection.delete_one({"_id": ctx.author.id})
            
            deleteEmbed = discord.Embed(title="Ticket Closed!", description="Your ticket has been closed. We hope your issue was resolved.")
            deleteEmbed.set_footer(text="Brought to you by Thunder")
            await dmChannel.send(embed=deleteEmbed)

            await interaction.response.send_message("Ticket Closed! this channel will be deleted momentarily.")
            await asyncio.sleep(1.75)

            logEmbed = discord.Embed(title=f"Ticket {randID} closed.", description=f"**Reason For Opening:** {reason}")
            logEmbed.set_footer(text="Brought to you by Thunder")
            logEmbed.timestamp = datetime.now()

            fileName = "log.txt"
            with open(fileName, "w") as file:
                async for msg in ticketChannelTarget.history(limit=None):
                    file.write(f"""{msg.created_at} - 
    {msg.author.display_name}: 
    {msg.clean_content}\n\n""")
            file = discord.File(fileName)
            await channel.send(embed=logEmbed, file=file)
            os.remove(fileName)

            await ticketChannelTarget.delete()  
            db_collection.delete_one({"_id": ctx.author.id})   
                    
        close_btn = Button(label="Close", style=discord.ButtonStyle.red)
        view = View()
        view.add_item(close_btn)
        close_btn.callback = btn_callback

        dmChannel = await ctx.author.create_dm()
        dmEmbed = discord.Embed(title="Your Ticket Has Been Opened!", description="Please wait for a response from the dev team to help with your issue.")
        dmEmbed.set_footer(text="Brought to you by Thunder")
        await dmChannel.send(embed=dmEmbed)

        ticketEmbed = discord.Embed(title=f"{ctx.author} has opened a ticket!", description=f"A user has opened a ticket with reason: {reason}")
        ticketEmbed.set_footer(text="Brought to you by Thunder")
        await ticketChannelTarget.send(embed=ticketEmbed, view=view) 

        await ctx.respond("Ticket Created!")

    @modmailCmds.command(name="sendmessage", description="Send a message to the staff.")
    @discord.option(name="anonymous", description="toggle whether the message is anonymous. True by default.", required=False, default=True)
    @commands.dm_only()
    async def ticket_send(self, ctx, message, anonymous):
        data = db_collection.find({"_id": ctx.author.id})
        async for user in data:
            if user["_id"] == ctx.author.id:
                ticket = self.bot.get_channel(user["ticketID"])
                if not bool(anonymous) or "n" in anonymous:
                    await ticket.send(f"From {ctx.author}: {message}")
                elif anonymous or "y" in anonymous:
                    await ticket.send(f"From Anonymous: {message}")
                await ctx.respond("Message Sent!", ephemeral=True)
                return
        try:
            if user["_id"] != ctx.author.id:
                return await ctx.respond("You do not have an open ticket!", ephemeral=True)
        except:
            return await ctx.respond("You do not have an open ticket!", ephemeral=True)

    @modmailCmds.command(name="adminrespond", description="Sends a message back to the user. BOT ADMINS ONLY")
    async def adminrespond(self, ctx, message):
        guild = self.bot.get_guild(int(guild_id))
        if ctx.author not in guild.members:
            return await ctx.respond("This command can only be used by bot admins!")  
        elif ctx.author in guild.members:
            ticketData = db_collection.find({"ticketID": ctx.channel.id})
            async for users in ticketData:
                user = self.bot.get_user(users["_id"])
            embed = discord.Embed(title=f"{ctx.author} sends a message:", description=message)
            embed.set_footer(text="Brought to you by Thunder")
            try:
                await user.send(embed=embed)
            except:
                return await ctx.respond("This is not a ticket channel, please use this command in an opened ticket!", ephemeral=True)
            await ctx.respond(f"{ctx.author} sent: {message}")            

def setup(bot):
    bot.add_cog(modmail(bot))