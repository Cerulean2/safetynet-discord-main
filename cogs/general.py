import asyncio,datetime,discord
from discord.ext import commands
from discord import Embed

class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    """
    Displays basic server information
    """
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