import discord
import os
import re

from redbot.core import checks, Config, commands

BaseCog = getattr(commands, "Cog", object)


class sthreact(BaseCog):

    """All STH reaction commands conveniently located in one file!"""

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

    @commands.group(name="sthreact_ignore", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_guild=True)
    async def sthreact_ignore(self, ctx):
        """Change Oh my cog ignore settings."""
        pass

    @sthreact_ignore.command(name="server", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_guild=True)
    async def _sthreact_ignore_server(self, ctx):
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

    @sthreact_ignore.command(name="channel", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_guild=True)
    async def _sthreact_ignore_channel(self, ctx):
        """Ignore/Unignore the current channel"""

        chan = ctx.message.channel
        chans = await self.conf.channels_ignored()
        if chan.id in chans:
            chans.remove(chan.id)
            await ctx.send("nani? Ok, I will no longer "
                           "ignore this channel.")
        else:
            chans.append(chan.id)
            await ctx.send("nani? Alright, I will ignore "
                           "this channel.")
        await self.conf.channels_ignored.set(chans)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        if message.author == self.bot.user:
            return
        #content = message.content.lower().split()
        content = message.content.lower()
        if len(content) < 2:
            return
        if message.guild.id in await self.conf.guilds_ignored():
            return
        if message.channel.id in await self.conf.channels_ignored():
            return

        
        pattern0 = "test"
        pattern1 = re.compile(r'(sigh)+[.]*', re.IGNORECASE)
        pattern2 = re.compile(r'(oh my)', re.IGNORECASE)
        pattern3 = re.compile(r'(keikaku)', re.IGNORECASE)
        pattern4 = re.compile(r'\A(\.\.\.)+[.]*', re.IGNORECASE)
        pattern5 = re.compile(r'(sorry not sorry)', re.IGNORECASE)
        pattern5_1 = re.compile(r'(sorrynotsorry)', re.IGNORECASE)
        pattern5_2 = re.compile(r'(gomenasike)', re.IGNORECASE)
        
        if re.search(pattern0, content):
            msg = "it works!!! shishou"
            await message.channel.send(msg)
            
            content_split = content.split()
            if "embed" in content_split[1]:
                embed = discord.Embed(
                    title = 'Title',
                    description = 'This is a description',
                    color = discord.Color.blue()
                )
                embed.set_footer(text='This is a footer')
                embed.set_image(url='https://pbs.twimg.com/profile_images/1148502291692965889/rdZ5NNWh_400x400.png')
                embed.set_thumbnail(url='https://pbs.twimg.com/profile_images/1148502291692965889/rdZ5NNWh_400x400.png')
                embed.add_field(name='Field Name', value='Field Value', inline=False)
                await message.channel.send(embed=embed)

        if re.search(pattern1, content):
            embed = discord.Embed(
                description = 'sigh...\nsai...\nSAIDO CHESTO!!',
                color = discord.Color.red()
            )
            embed.set_image(url='https://media1.tenor.com/images/316802abc29c277b08bae799b1fbe52c/tenor.gif')
            await message.channel.send(embed=embed)
            
        if re.search(pattern2, content):
            embed = discord.Embed(
                description = 'oh my...\nomae...\nOMAE WA MOU SHINDEIRU!!!',
                color = discord.Color.red()
            )
            embed.set_image(url='https://i.makeagif.com/media/2-21-2015/RDVwim.gif')
            await message.channel.send(embed=embed)
            
        if re.search(pattern3, content):
            msg = "TL's Note: Keikaku means plan."
            await message.channel.send(msg)

        if re.search(pattern4, content):
            embed = discord.Embed(
                color = discord.Color.red()
            )
            embed.set_image(url='https://cdn.discordapp.com/attachments/464597387504123905/631584595627868180/bakuman-ep-14-5.png')
            await message.channel.send(embed=embed)
            
        if re.search(pattern5, content) or re.search(pattern5_1, content) or re.search(pattern5_2, content):
            embed = discord.Embed(
                color = discord.Color.red()
            )
            embed.set_image(url='https://i.pinimg.com/236x/81/95/4c/81954cf575ffa7bd8b573efc848c92c0.jpg')
            await message.channel.send(embed=embed)
