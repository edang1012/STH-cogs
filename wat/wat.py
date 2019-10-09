import os
import re

from redbot.core import checks, Config, commands

BaseCog = getattr(commands, "Cog", object)


class Wat(BaseCog):

    """Repeat messages when other users are having trouble hearing"""

    default_global_settings = {
        "channels_ignored": [],
        "guilds_ignored": []
    }

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=527690525)
        self.conf.register_global(
            **self.default_global_settings
        )

    @commands.group(name="watignore", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_guild=True)
    async def watignore(self, ctx):
        """Change Wat cog ignore settings."""
        pass

    @watignore.command(name="server", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_guild=True)
    async def _watignore_server(self, ctx):
        """Ignore/Unignore the current server"""

        guild = ctx.message.guild
        guilds = await self.conf.guilds_ignored()
        if guild.id in guilds:
            guilds.remove(guild.id)
            await ctx.send("wot? Ok boss, I will no longer "
                           "ignore this server.")
        else:
            guilds.append(guild.id)
            await ctx.send("what? Fine, I will ignore "
                           "this server.")
        await self.conf.guilds_ignored.set(guilds)

    @watignore.command(name="channel", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_guild=True)
    async def _watignore_channel(self, ctx):
        """Ignore/Unignore the current channel"""

        chan = ctx.message.channel
        chans = await self.conf.channels_ignored()
        if chan.id in chans:
            chans.remove(chan.id)
            await ctx.send("wut? Ok, I will no longer "
                           "ignore this channel.")
        else:
            chans.append(chan.id)
            await ctx.send("wat? Alright, I will ignore "
                           "this channel.")
        await self.conf.channels_ignored.set(chans)

    # Come up with a new method to ignore bot commands
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        if message.author == self.bot.user:
            return
        content = message.content.lower().split()
        if len(content) != 1:
            return
        if message.guild.id in await self.conf.guilds_ignored():
            return
        if message.channel.id in await self.conf.channels_ignored():
            return
        
        pattern = 'sigh'
        if content[0] == pattern:
            #await message.channel.send("test")
            async for before in message.channel.history(limit=5, before=message):
                author = before.author
                name = author.display_name
                content = before.clean_content
                if not author.bot\
                        and not author == message.author:
                        #and not pattern.fullmatch(content):
                        #and not self.is_command(before)\
                    emoji = "\N{CHEERING MEGAPHONE}"
                    msg = "{0} said, **{1}   {2}**".format(name, emoji,
                                                           content)
                    await message.channel.send(msg)
                    break
