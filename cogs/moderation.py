import asyncio,datetime,discord
from discord.ext import commands
from discord import Embed

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    Bans a member

    Usage: !ban @user <dateframe:1d,1h,1m,1s> <reason>
    """
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, duration: str, *, reason: str):
        if duration:
            duration_dict = {
                'd': 86400,  # seconds in a day
                'h': 3600,  # seconds in an hour
                'm': 60  # seconds in a minute
            }
            ban_duration = 0
            for char in duration:
                if char.isdigit():
                    ban_duration = ban_duration * 10 + int(char)
                elif char.lower() in duration_dict:
                    ban_duration = ban_duration * duration_dict[char.lower()]
            await member.ban(reason=reason)
            ban_embed = discord.Embed(
                title=':tools: Banned Member',
                description=f'Banned {member.mention} for {ban_duration} seconds for `{reason}`',
                color=discord.Color.red()
                
            )
            ban_embed.set_footer(text=f'ID: {member.id} | Timestamp: {datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')
            await ctx.send(embed=ban_embed)
            await asyncio.sleep(ban_duration)
            await member.unban()
            unban_embed = discord.Embed(
                title=':tools: Unbanned Member',
                description=f'Unbanned {member.mention}',
                color=discord.Color.green()
            )
            unban_embed.set_footer(text=f'ID: {member.id} | Unban Time: {datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')
            await ctx.send(embed=unban_embed)
        else:
            await member.ban(reason=reason)
            ban_embed = discord.Embed(
                title=':tools: Ban',
                description=f'Banned {member.mention} for `{reason}`',
                color=discord.Color.red()
            )
            ban_embed.set_footer(text=f'ID: {member.id} | Timestamp: {datetime.datetime.now().strftime("%m/%d/%Y %I:%M %p")}')
            await ctx.send(embed=ban_embed)
            embed = discord.Embed(title="Bban Log", description=f"{member.mention} has been **banned** by {ctx.author.mention}\n\nReason: `{reason}`\n\Banned from: `{ctx.guild.name}`", color=0x1355ed)
            embed.add_field(name="User", value=f"{member}", inline=True)
            embed.add_field(name="UserID", value=f"{member.id}", inline=True)
            embed.add_field(name="Moderator", value=f"{ctx.author}", inline=True)
            embed.set_footer(text=f"Ban log - Banned user: {member.name}")
            embed.timestamp = datetime.datetime.utcnow()
            logchannel = ctx.guild.get_channel(1073344165666115657)        
            await logchannel.send(embed=embed)
    """
    Unbans a user, optional reason
    """
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx, member:discord.User, *, reason=None):
        server = ctx.guild
        icon_url = server.icon
        if reason == None:
            reason = f"No Reason Provided"
        await ctx.guild.unban(member, reason=reason)
        await ctx.send(f"{member.mention} has been **unbanned**", delete_after=15)
        embed = discord.Embed(title="Unban Log", description=f"{member.mention} has been **unbanned** by {ctx.author.mention}\n\nReason: `{reason}`\n\nUnbanned from: `{ctx.guild.name}`", color=0x1355ed)
        embed.add_field(name="User", value=f"{member}", inline=True)
        embed.add_field(name="UserID", value=f"{member.id}", inline=True)
        embed.add_field(name="Moderator", value=f"{ctx.author}", inline=True)
        embed.set_footer(text=f"Unban log - Banned user: {member.name}")
        embed.set_thumbnail(url=icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        logchannel = ctx.guild.get_channel(1073344165666115657)        
        await logchannel.send(embed=embed)
        await ctx.message.delete()
        print(f"Sucsessfully unbanned {member.name}")

    """
    Errror handling for ban
    """
    @ban.error
    async def on_application_command_error(self, ctx, error: discord.DiscordException):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
            title=':no_entry_sign: Missing Argument',
            color=discord.Color.red()
            )
            embed.add_field(name='Uh oh!',value='Member is a required argument that is missing.', inline=False)
            await ctx.channel.send(embed=embed)
        else:
            raise error  # Here we raise other errors to ensure they aren't ignored

    """
    Kicks a user, optional reason
    """
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} for {reason}')
        embed = discord.Embed(title="Kick Log", description=f"{member.mention} has been **kicked** by {ctx.author.mention}\n\nReason: `{reason}`\n\Kicked from: `{ctx.guild.name}`", color=0x1355ed)
        embed.add_field(name="User", value=f"{member}", inline=True)
        embed.add_field(name="UserID", value=f"{member.id}", inline=True)
        embed.add_field(name="Moderator", value=f"{ctx.author}", inline=True)
        embed.set_footer(text=f"Kick log - Kicked user: {member.name}")
        embed.timestamp = datetime.datetime.utcnow()
        logchannel = ctx.guild.get_channel(1073344165666115657)        
        await logchannel.send(embed=embed)

    """
    Errror handling for kick
    """
    @kick.error
    async def on_application_command_error(ctx, error: discord.DiscordException):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
            title=':no_entry_sign: Missing Argument',
            color=discord.Color.red()
            )
            embed.add_field(name='Uh oh!',value='Member is a required argument that is missing.', inline=False)
            await ctx.channel.send(embed=embed)
        else:
            raise error  # Here we raise other errors to ensure they aren't ignored

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))