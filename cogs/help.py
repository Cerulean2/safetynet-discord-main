import discord
from discord.ext import commands
from discord import Embed

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pages = []
        self.current_page = 0
        
    @commands.command(name='help')
    async def help_command(self, ctx):
        # Create the first page of help information
        server = ctx.guild
        icon_url = server.icon
        page1 = discord.Embed(
            title='Help Menu - General',
            description='General/Fun Commands',
            color=discord.Color.green()
        )
        page1.set_author(name=server.name,icon_url=icon_url)
        page1.set_footer(text='Bot created by Ceru#2976 | Support Server: https://discord.gg/8HtHut2BYY')
        page1.set_thumbnail(url=icon_url)      
        # Add more fields for other commands
        page1.add_field(name='!help', value='Displays this menu', inline=False)
        page1.add_field(name='!serverinfo', value='Displays server information', inline=False)
        self.pages.append(page1)

        # Create the second page of help information
        server = ctx.guild
        icon_url = server.icon
        page2 = discord.Embed(
            title='Help Menu - Moderation',
            description='Administrator and Moderator commands',
            color=discord.Color.green()
        )
        page2.set_author(name=server.name,icon_url=icon_url)
        page2.set_footer(text='Bot created by Ceru#2976 | Support Server: https://discord.gg/8HtHut2BYY')
        page2.set_thumbnail(url=icon_url)      
        # Add more fields for other commands
        page2.add_field(name='!setprefix - `Developer`', value='Changes the bot prefix', inline=False)
        page2.add_field(name='!setup - `Admin`', value='Checks the server configuration for improper or dangerous permissions', inline=False)
        page2.add_field(name='!embed - `Admin`', value='Creates an embed in the current channel', inline=False)
        page2.add_field(name='!ban/unban - `Mod`', value='Ban or unbans a target member', inline=False)
        page2.add_field(name='!kick - `Mod`', value='Kick a target member', inline=False)
        self.pages.append(page2)

        # Send the first page of the help menu
        message = await ctx.send(embed=self.pages[0])

        # Add the forward and back reactions
        await message.add_reaction('⬅️') # back arrow
        await message.add_reaction('➡️') # forward arrow
        await message.add_reaction("🗑️") # trash can

        while True:
            # Wait for the user to react
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["🗑️", "⬅️", "➡️"]

            reaction, user = await self.bot.wait_for("reaction_add", check=check)

            if str(reaction.emoji) == "🗑️":
                # Delete the help command if the user reacts with the trashcan
                await message.delete()
                break
            elif str(reaction.emoji) == "➡️":
                # Go to the next help page if the user reacts with the right arrow
                self.current_page = (self.current_page + 1) % len(self.pages)
                await message.edit(embed=self.pages[self.current_page])
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "⬅️":
                # Go to the previous help page if the user reacts with the left arrow
                self.current_page = (self.current_page - 1) % len(self.pages)
                await message.edit(embed=self.pages[self.current_page])
                await message.remove_reaction(reaction, user)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
