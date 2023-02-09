import asyncio,datetime,discord
from discord.ext import commands
from discord import Embed

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self,message):
        server = message.guild
        icon_url = server.icon
            
        await message.channel.send(f':gear: Checking permissions for **{server.name}**...')

        mention_roles = []
        admin_roles = []
        moderation_roles = []
        disabled_history_channels = []
        open_channels = []
            
        for role in server.roles:
            if role.permissions.mention_everyone:
                mention_roles.append(role)
            if role.permissions.administrator:
                admin_roles.append(role)
            if role.permissions.kick_members or role.permissions.ban_members or role.permissions.manage_messages or role.permissions.move_members or role.permissions.mute_members or role.permissions.deafen_members or role.permissions.manage_nicknames:
                moderation_roles.append(role)

        embed = Embed(title='', color=0xffa500)
        embed.set_author(name=server.name,icon_url=icon_url)
        embed.set_footer(text='Bot created by Ceru#2976 | Support Server: https://discord.gg/8HtHut2BYY')
        embed.set_thumbnail(url=icon_url)      

        if not mention_roles:
            embed.add_field(name=':white_check_mark: Roles with `mention @everyone` permissions', value='None found.')
        else:
            roles = ' '.join([f'<@&{r.id}>' if r.name != "@everyone" else "@everyone" for r in mention_roles])
            embed.add_field(name=':octagonal_sign:  Roles with `mention @everyone` permissions', value=roles)

        if not admin_roles:
            embed.add_field(name=':white_check_mark: Roles with `Administrator`', value='None found.')
        else:
            roles = ' '.join([f'<@&{r.id}>' for r in admin_roles])
            embed.add_field(name=':octagonal_sign:  Roles with `Administrator`', value=roles)

        if not moderation_roles:
            embed.add_field(name=':white_check_mark: Roles with `Moderator` privileges', value='None found.')
        else:
            mods = ''
            for role in moderation_roles:
                mod_privileges = []
                if role.permissions.kick_members:
                    mod_privileges.append('`Kick Members`')
                if role.permissions.ban_members:
                    mod_privileges.append('`Ban Members`')
                if role.permissions.manage_messages:
                    mod_privileges.append('`Manage Messages`')
                if role.permissions.move_members:
                    mod_privileges.append('`Move Members`')
                if role.permissions.mute_members:
                    mod_privileges.append('`Mute Members`')
                if role.permissions.deafen_members:
                    mod_privileges.append('`Deafen Members`')
                if role.permissions.manage_nicknames:
                    mod_privileges.append('`Manage Nicknames`')
                mods += f'<@&{role.id}> - {", ".join(mod_privileges)}\n'
            embed.add_field(name=':warning: Roles with `Moderator` privileges', value=mods, inline=False)

        for channel in server.channels:
            if not channel.permissions_for(server.default_role).read_message_history:
                disabled_history_channels.append(channel)
            if channel.permissions_for(server.default_role).send_messages and (channel.name.lower() == 'announcements' or channel.name.lower() == 'rules' or channel.name.lower() == 'welcome'):
                open_channels.append(channel)

        if not disabled_history_channels:
            embed.add_field(name=':white_check_mark: Channels with read history disabled', value='None found.')
        else:
            channels = ' '.join([f'<#{c.id}>' for c in disabled_history_channels])
            embed.add_field(name=':mag_right: Channels with read history disabled', value=channels)

        if not open_channels:
            embed.add_field(name=':white_check_mark: Possible `Admin` channels with `send messages` enabled', value='None found.')
        else:
            channels = ' '.join([f'<#{c.id}>' for c in open_channels])
            embed.add_field(name=':mag_right: Possible `Admin` channels with `send messages` enabled', value=channels)

        await message.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AdminCog(bot))