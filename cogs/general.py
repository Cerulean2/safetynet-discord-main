import asyncio,datetime,discord
from discord.ext import commands
from discord import Embed

class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self,message):
        server = message.guild
        icon_url = server.icon
        embed = discord.Embed(
            title='Help',
            description='List of commands available:',
            color=discord.Color.red()
        )
        embed.set_author(name=server.name,icon_url=icon_url)
        embed.set_footer(text='Bot created by Ceru#2976 | Support Server: https://discord.gg/8HtHut2BYY')
        embed.set_thumbnail(url=icon_url)      
        # Add more fields for other commands
        embed.add_field(name='!help', value='Displays this menu', inline=False)
        embed.add_field(name='!serverinfo', value='Displays server information', inline=False)
        embed.add_field(name='!setprefix - `Developer`', value='Changes the bot prefix', inline=False)
        embed.add_field(name='!setup - `Admin`', value='Checks the server configuration for improper or dangerous permissions', inline=False)
        #embed.add_field(name='!toggleinv - `Admin`', value='Toggles server invites', inline=False)
        embed.add_field(name='!ban/unban - `Mod`', value='Ban or unbans a target member', inline=False)
        embed.add_field(name='!kick - `Mod`', value='Kick a target member', inline=False)

        await message.send(embed=embed)
        
    @commands.command()
    async def serverinfo(self,message):
        server = message.guild
        icon_url = server.icon
        embed = discord.Embed(
            title='',
            color=discord.Color.red()
        )
        embed.set_author(name=server.name,icon_url=icon_url)
        embed.set_thumbnail(url=icon_url)
        embed.add_field(name="Owner", value=server.owner, inline=True)
        embed.add_field(name="Category Channels", value=len(server.categories), inline=True)
        embed.add_field(name="Text Channels", value=len(server.text_channels), inline=True)
        embed.add_field(name="Voice Channels", value=len(server.voice_channels), inline=True)
        embed.add_field(name="Members", value=server.member_count, inline=True)
        embed.add_field(name="Roles", value=len(server.roles), inline=True)
        embed.set_footer(text=f'ID: {server.id} | Server Created: {server.created_at.strftime("%m/%d/%Y %I:%M %p")}')
        await message.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GeneralCog(bot))