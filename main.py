import discord
import asyncio
from discord.ext import commands
#from discord.commands import option
import pymongo
from pymongo import MongoClient
import json

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

cluster = MongoClient(
    "mongodb+srv://exbyte:1234@cluster0.aw1f22q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = cluster["KronosTwikit"]
collection = db["KronosTwikit"]
reply_collection = db["KronosTwikitReplies"]
watch_collection = db["KronosTwikitWatch"]
secondary_collection = db["KronosTwikitSecondary"]
secondary_reply_collection = db["KronosTwikitSecondaryReplies"]
power_state_collection = db["KronosTwikitPowerState"]

with open("config.json", "r") as f:
    config = json.load(f)
    TOKEN = config["token"]

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)
intents = intents.default()

@bot.event
async def on_ready():
    # add help command as status
    await bot.change_presence(activity=discord.Game(name="/help"))
    print(f"Logged in as {bot.user}")

@bot.slash_command()
async def set_account(ctx, email, password, username):
    await ctx.defer()
    """
    Change the account details for the twitter bot
    """
    data = {
        "main_bot_email": email,
        "main_bot_password": password,
        "main_bot_username": username
    }
    collection.update_one(
        {"_id": 0},
        {"$set": data},
        upsert=True
    )
    """
    
    more logic here
    
    """
    await ctx.respond("Account details updated successfully!")

@bot.slash_command()
async def get_account(ctx):
    await ctx.defer()
    """
    Get the account details for the twitter bot
    """
    data = collection.find_one({"_id": 0})
    if data is None:
        await ctx.send("No account details found!")
        return
    embed = discord.Embed(
        title="Account Details",
        description=f"Email: {data['main_bot_email']}\nPassword: {data['main_bot_password']}\nUsername: {data['main_bot_username']}"
    )
    await ctx.respond(embed=embed)

@bot.slash_command()
async def start_bot(ctx):
    await ctx.defer()
    """
    Start the twitter bot
    """
    power_state = "on"
    power_state_collection.update_one(
        {"_id": 0},
        {"$set": {"power_state": power_state}},
        upsert=True
    )
    await ctx.respond("Twitter bot will start shortly!")

@bot.slash_command()
async def stop_bot(ctx):
    await ctx.defer()
    """
    Stop the twitter bot
    """
    power_state = "off"
    power_state_collection.update_one(
        {"_id": 0},
        {"$set": {"power_state": power_state}},
        upsert=True
    )
    await ctx.respond("Bot stopped successfully!")

@bot.slash_command()
async def help(ctx):
    """
    Shows the list of commands
    """
    await ctx.defer()
    embed = discord.Embed(
        title="Commands")
    embed.add_field(name="/set_account", value="Change the account details for the twitter bot", inline=False)
    embed.add_field(name="/get_account", value="Get the account details for the twitter bot", inline=False)
    embed.add_field(name="/start_bot", value="Start the twitter bot", inline=False)
    embed.add_field(name="/stop_bot", value="Stop the twitter bot", inline=False)
    embed.add_field(name="/add_replies", value="Loads the form for adding replies", inline=False)
    embed.add_field(name="/get_replies", value="Get the list of replies", inline=False)
    embed.add_field(name="/watch_accounts", value="Loads the form for watching accounts", inline=False)
    embed.add_field(name="/get_watch_accounts", value="Get the list of accounts to watch", inline=False)
    embed.add_field(name="/add_secondary_account", value="Add details for bots that will interact with the main bot", inline=False)
    embed.add_field(name="/get_secondary_accounts", value="Get the details for the secondary accounts", inline=False)
    embed.add_field(name="/remove_secondary_account", value="Remove the details for a secondary account", inline=False)
    embed.add_field(name="/add_secondary_replies", value="Loads the form for adding replies for secondary accounts", inline=False)
    embed.add_field(name="/get_secondary_replies", value="Get the list of replies for secondary accounts", inline=False)
    await ctx.respond(embed=embed)

class FormModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Reply list", placeholder="Enter the list of replies separated by semicolons (;)", style=discord.InputTextStyle.long))
    
    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Form Submitted",
            description="Your form has been submitted successfully!"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # process the form data and save it to the database
        data = self.children[0].value
        replies = data.split(";")
        # save the list of replies to the database
        reply_collection.update_one(
            {"_id": 0},
            {"$set": {"replies": replies}},
            upsert=True
        )
        
    async def on_timeout(self):
        embed = discord.Embed(
            title="Form Timed Out",
            description="You didn't fill out the form in time!"
        )
        await self.message.edit(embed=embed, view=None)

@bot.slash_command()
async def add_replies(ctx):
    """Loads the form for adding replies"""
    modal = FormModal(title="Add Replies")
    await ctx.send_modal(modal)

@bot.slash_command()
async def get_replies(ctx):
    """Get the list of replies"""
    await ctx.defer()
    data = reply_collection.find_one({})
    if data is None:
        await ctx.send("No replies found!")
        return
    replies = data["replies"]
    embed = discord.Embed(
        title="Replies",
        description="\n".join(replies)
    )
    await ctx.respond(embed=embed)

class WatchFormModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Enter the accounts to watch", placeholder="Enter the list of accounts to watch separated by semicolons (;)", style=discord.InputTextStyle.long))
        
    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Form Submitted",
            description="Your form has been submitted successfully!"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # process the form data and save it to the database
        data = self.children[0].value
        accounts = data.split(";")
        # save the list of accounts to watch to the database
        watch_collection.update_one(
            {"_id": 0},
            {"$set": {"watch_accounts": accounts}},
            upsert=True
        )
    
    async def on_timeout(self):
        embed = discord.Embed(
            title="Form Timed Out",
            description="You didn't fill out the form in time!"
        )
        await self.message.edit(embed=embed, view=None)
    
@bot.slash_command()
async def watch_accounts(ctx):
    """Loads the form for watching accounts"""
    modal = WatchFormModal(title="Watch Accounts")
    await ctx.send_modal(modal)

@bot.slash_command()
async def get_watch_accounts(ctx):
    """Get the list of accounts to watch"""
    await ctx.defer()
    data = watch_collection.find_one({"_id": 0})
    if data is None:
        await ctx.send("No accounts found!")
        return
    accounts = data["watch_accounts"]
    embed = discord.Embed(
        title="Accounts to Watch",
        description="\n".join(accounts)
    )
    await ctx.respond(embed=embed)


@bot.slash_command()
async def add_secondary_account(ctx, email, password, username):
    await ctx.defer()
    """
    Add details for bots that will interact with the main bot
    """
    data = {
        "secondary_bot_email": email,
        "secondary_bot_password": password,
        "secondary_bot_username": username
    }
    secondary_collection.insert_one(data)
    
    await ctx.respond("Secondary account details added successfully!")

@bot.slash_command()
async def get_secondary_accounts(ctx):
    await ctx.defer()
    """
    Get the details for the secondary accounts
    """
    data = secondary_collection.find({})
    if data is None:
        await ctx.send("No secondary account details found!")
        return
    embed = discord.Embed(
        title="Secondary Account Details"
    )
    for account in data:
        embed.add_field(
            name=account["secondary_bot_username"],
            value=f"Email: {account['secondary_bot_email']}\nPassword: {account['secondary_bot_password']}"
        )
    await ctx.respond(embed=embed)

@bot.slash_command()
async def remove_secondary_account(ctx, username):
    await ctx.defer()
    """
    Remove the details for a secondary account
    """
    secondary_collection.delete_one({"secondary_bot_username": username})
    await ctx.respond("Secondary account details removed successfully!")

class SecondaryFormModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Reply list", placeholder="Enter the list of replies separated by semicolons (;)", style=discord.InputTextStyle.long))
    
    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Form Submitted",
            description="Your form has been submitted successfully!"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # process the form data and save it to the database
        data = self.children[0].value
        replies = data.split(";")
        # save the list of replies to the database
        secondary_reply_collection.update_one(
            {"_id": 0},
            {"$set": {"replies": replies}},
            upsert=True
        )
        
    async def on_timeout(self):
        embed = discord.Embed(
            title="Form Timed Out",
            description="You didn't fill out the form in time!"
        )
        await self.message.edit(embed=embed, view=None)

@bot.slash_command()
async def add_secondary_replies(ctx):
    """Loads the form for adding replies for secondary accounts"""
    modal = SecondaryFormModal(title="Add Secondary Replies")
    await ctx.send_modal(modal)

@bot.slash_command()
async def get_secondary_replies(ctx):
    """Get the list of replies for secondary accounts"""
    await ctx.defer()
    data = secondary_reply_collection.find_one({})
    if data is None:
        await ctx.send("No replies found!")
        return
    replies = data["replies"]
    embed = discord.Embed(
        title="Replies",
        description="\n".join(replies)
    )
    await ctx.respond(embed=embed)


bot.run(TOKEN)