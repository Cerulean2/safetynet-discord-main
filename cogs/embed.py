import asyncio,datetime,discord
from discord.ext import commands
from discord import Embed

class EmbedGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def embed(self, ctx, title: str, color: str, *, message: str):
        # Convert the hexadecimal color code to an integer
        color = int(color[1:], 16)

        # Create an instance of the Embed class
        embed = discord.Embed(
            title=title,
            description=message,
            color=color
        )

        # Send the embed to the channel
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EmbedGenerator(bot))