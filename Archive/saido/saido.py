import os
import re
import io
import aiohttp

from discord.ext import commands

from __main__ import send_cmd_help

from .utils import checks
from .utils.dataIO import dataIO


class saido:

    """Repeat messages when other users are having trouble hearing"""

    def __init__(self, bot):
        self.bot = bot
        self.settings_path = "data/saido/settings.json"
        self.settings = dataIO.load_json(self.settings_path)

    @commands.group(name="saidoignore", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def saidoignore(self, ctx):
        """Change saido cog ignore settings."""

        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @saidoignore.command(name="server", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _saidoignore_server(self, ctx):
        """Ignore/Unignore the current server"""

        server = ctx.message.server
        if server.id in self.settings['ignore_servers']:
            self.settings['ignore_servers'].remove(server.id)
            await self.bot.say("wot? Ok boss, I will no longer "
                               "ignore this server.")
        else:
            self.settings['ignore_servers'].append(server.id)
            await self.bot.say("what? Fine, I will ignore "
                               "this server.")
        dataIO.save_json(self.settings_path, self.settings)

    @saidoignore.command(name="channel", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _saidoignore_channel(self, ctx):
        """Ignore/Unignore the current channel"""

        channel = ctx.message.channel
        if channel.id in self.settings['ignore_channels']:
            self.settings['ignore_channels'].remove(channel.id)
            await self.bot.say("wut? Ok, I will no longer "
                               "ignore this channel.")
        else:
            self.settings['ignore_channels'].append(channel.id)
            await self.bot.say("wat? Alright, I will ignore "
                               "this channel.")
        dataIO.save_json(self.settings_path, self.settings)

    async def on_message(self, message):
        if message.server is None:
            return
        if message.author.bot:
            return
        if self.is_command(message):
            return
        content = message.content.lower().split()
        if len(content) != 1:
            return
        if message.server.id in self.settings['ignore_servers']:
            return
        if message.channel.id in self.settings['ignore_channels']:
            return

        pattern = re.compile(r's+i+g+h+[.]*', re.IGNORECASE)
        if pattern.fullmatch(content[0]):
            msg = "https://media1.tenor.com/images/316802abc29c277b08bae799b1fbe52c/tenor.gif \n\nsigh...\nsai...\nSAIDO CHESTO!!"
            await self.bot.send_message(message.channel, msg)

    # Credit to Twentysix26's trigger cog
    def is_command(self, msg):
        if callable(self.bot.command_prefix):
            prefixes = self.bot.command_prefix(self.bot, msg)
        else:
            prefixes = self.bot.command_prefix
        for p in prefixes:
            if msg.content.startswith(p):
                return True
        return False


def check_folders():
    folder = "data/saido"
    if not os.path.exists(folder):
        print("Creating {} folder...".format(folder))
        os.makedirs(folder)


def check_files():
    default = {'ignore_channels': [], 'ignore_servers': []}
    if not dataIO.is_valid_json("data/saido/settings.json"):
        print("Creating default saido settings.json...")
        dataIO.save_json("data/saido/settings.json", default)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(saido(bot))
