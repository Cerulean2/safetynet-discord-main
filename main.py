import os,asyncio
from dotenv import load_dotenv
import discord
from discord import Embed
from discord.ext import commands 

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
client.owner_id = 856298738044895312
client.remove_command('help')
load_dotenv()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print(f'Discord version: {discord.__version__}')
    print(f'Client user name: {client.user.name}')
    print(f'Client user ID: {client.user.id}')
    print(f'Connected to {len(client.guilds)} guilds')
    print(f'Invite URL: https://discord.com/api/oauth2/authorize?client_id=1072003711603314779&permissions=17515801840&scope=bot')
    print(f'Bot created by: Ceru#2976')
    print('------')
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
    for cog in client.cogs:
        print(f'Loaded cog: {cog}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="!help"))

"""
Change the bots prefix, restricted to bot owner
"""
@client.command()
@commands.has_permissions(administrator=True)
async def setprefix(message, prefix):
    if message.author.id == client.owner_id:
        client.command_prefix = prefix
        await message.send(f'Prefix successfully changed to `{prefix}`')
    else:
        return

client.run(os.getenv("DISCORD_TOKEN"))