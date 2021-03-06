import discord
import os
import re
import pickle
import random
import numpy as np

# BE CAREFULE 'Path' and 'path' ARE DIFFERENT
from pathlib import Path
import os.path
from os import path

from redbot.core import checks, Config, commands


class weebcircle(commands.Cog):
    """This bot was made to be used for weebcircle things."""
    
    default_guild_settings = {
        "settings": {}
    }

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=964952632)
        self.conf.register_guild(
            **self.default_guild_settings
            )
        self.list = []
        self.old =  []
        self.test = []
        self.dir = '/home/pi/Bot_Archive/weebcircle/'

        
    @commands.guild_only()
    @commands.command()
    async def start(self, ctx):
        
        # clear list for next circle
        self.list = []
        
        # create director for channel if doesn't exist
        weebfile = self.dir + '{}/'.format(ctx.message.channel)
        Path(weebfile).mkdir(parents=True, exist_ok=True)
        
        # create file if doesn't exist
        weebfile += 'weeb_list.data'
        with open(weebfile, 'wb') as f:
            pickle.dump(self.list,f)
        
        # create embed welcome message, no real code here, just formatting
        embed = discord.Embed(
            title = 'Welcome to the Weeb Circle',
            description = """The purpose of this circle is to get others in the group to watch anime they haven't seen before.""",
            color = discord.Color.red()
        )
        footer = """Warning: running this command clears the list, so don't use this command again to view the instructions. Use .weebhelp"""
        embed.set_footer(text=footer)
        embed.add_field(name='**Instructions:**', 
                        value=("To start the circle, please follow the procedure listed below:\n\n"

                        "1.  **\".optin <count>\"**:\nUse this command to opt into the circle. " 
                                                    "Specify the number of cours you want to watch with a number or keywords such as: *easy, med, hard*. " 
                                                    "\nIf you want to opt out after opting in, simply use the command **\".optout\"**.\n\n"

                        "2.  **\".randomize\"**:     \nUse this command to create a randomized list for the members to recommend "
                                                    "anime.\n\n"

                        "3.  **\".rec <anime>\"**:   \nUse this command to recommend an anime to your assigned member. \nIf you want "
                                                    "to see who is your assigned member use the command **\".list\"**.\n\n"

                        "4.  **\".watch\"**:         \nUse this command to display the final list of what each member is watching.\n\n" 
                               
                        "5.  **\".weebhelp\"**:      \nUse this command to view the instructions again in case you forget them. " 
                                                    "\n\n"), 
                        inline=False
        )
        embed.set_thumbnail(url='https://pbs.twimg.com/profile_images/1148502291692965889/rdZ5NNWh_400x400.png')
        await ctx.send(embed=embed)
        
    @commands.guild_only()
    @commands.command()
    async def weebhelp(self, ctx):
        
        # create embed welcome message, no real code here, just formatting
        embed = discord.Embed(
            title = 'Weebcircle Help Menu',
            description = """View the instructions again in case you forgot them. """,
            color = discord.Color.red()
        )
        footer = """Why are you looking down here, baka..."""
        embed.set_footer(text=footer)
        embed.add_field(name='**Instructions:**', 
                        value=("To start the circle, please follow the procedure listed below:\n\n"

                        "1.  **\".optin <count>\"**:\nUse this command to opt into the circle. " 
                                                    "Specify the number of cours you want to watch with a number or keywords such as: *easy, med, hard*. " 
                                                    "\nIf you want to opt out after opting in, simply use the command **\".optout\"**.\n\n"

                        "2.  **\".randomize\"**:     \nUse this command to create a randomized list for the members to recommend "
                                                    "anime.\n\n"

                        "3.  **\".rec <anime>\"**:   \nUse this command to recommend an anime to your assigned member. \nIf you want "
                                                    "to see who is your assigned member use the command **\".list\"**.\n\n"

                        "4.  **\".watch\"**:         \nUse this command to display the final list of what each member is watching. " 
                                                    "\n\n"), 
                        inline=False
        )
        embed.set_thumbnail(url='https://pbs.twimg.com/profile_images/1148502291692965889/rdZ5NNWh_400x400.png')
        await ctx.send(embed=embed)
        
        
    @commands.guild_only()
    @commands.command()
    async def optin(self, ctx, arg1):
        """Usage: Enter the number of cours you would like to watch\n
        Input any number of cours or specify with the keywords below:
        1 cour:   1, Easy, Wolf, Okami
        2 cours:  2, Med, Medium, Tiger
        3 cours:  3, Hard, Demon, Oni, Akuma
        3+ cours: Expert, Dragon, Ryu"""
        
        weebfile = self.dir + str(ctx.message.channel) + '/weeb_list.data'
        #check if .start was run by looking at the directory
        if not path.exists(weebfile):
            msg = 'You cant optin without starting the circle. Use **.start** to start the circle.'
            
        else:
            # open list from file to ensure most up to date version
            with open(weebfile, 'rb') as f:
                self.list = pickle.load(f)

            msg = 'none'

            # convert input argument to a number if valid
            if arg1.isnumeric():
                    pass

            # check the keywords    
            elif (arg1.lower() == 'easy') or (arg1.lower() == 'wolf') or (arg1.lower() == 'okami'):
                arg1 = '1'

            elif (arg1.lower() == 'med') or (arg1.lower() == 'medium') or (arg1.lower() == 'tiger') or (arg1.lower() == 'tora'):
                arg1 = '2'

            elif (arg1.lower() == 'hard') or (arg1.lower() == 'demon') or (arg1.lower() == 'oni') or (arg1.lower() == 'akuma'):
                arg1 = '3'

            elif (arg1.lower() == 'expert') or (arg1.lower() == 'dragon') or (arg1.lower() == 'ryu'):
                arg1 = '3+'

            elif (arg1.lower() == 'god') or (arg1.lower() == 'kami'):
                arg1 = 'f'

            else:
               arg1 = '0'

            # check if author is in list already
            for member in self.list:
                if member[0] == ctx.author.mention:

                    # already in the list, no changes
                    if member[1] == arg1:
                        msg = "You are already in the list baka"

                    elif arg1 == '0':
                        msg = "Thats not a valid number of cours, baka..."

                    elif arg1 == 'f':
                        msg = "Just pick something from here: https://en.wikipedia.org/wiki/List_of_anime_series_by_episode_count \nEnjoy ya damn masochist..."

                    # in the list, but different cour count
                    else:
                        # update the list with new cour count
                        member[1] = arg1
                        #with open('/home/pi/Bot_Archive/weeb_list.data', 'wb') as f:
                        with open(weebfile, 'wb') as f:
                            pickle.dump(self.list,f)
                        msg = "{} was already in the list, but now they want to watch {} cour(s).".format(ctx.author.mention,arg1)

            # member wasn't in list cause msg is still 'none'
            # add them to the list if input was valid
            if msg == 'none':
                if arg1 == '0':
                    msg = "Thats not a valid number of cours, baka..."

                elif arg1 == 'f':
                    msg = "Just pick something from here: https://en.wikipedia.org/wiki/List_of_anime_series_by_episode_count \nEnjoy ya damn masochist..."

                else:
                    # update list with new member
                    self.list.append([ctx.author.mention, arg1])
                    #with open('/home/pi/Bot_Archive/weeb_list.data', 'wb') as f:
                    with open(weebfile, 'wb') as f:
                        pickle.dump(self.list,f)
                    msg = "{} has been added to the list and wants at most {} cour(s).".format(ctx.author.mention,arg1)

        await ctx.send(msg)
        
    
    # TODO: update to not allow optout if not already in the list
    @commands.guild_only()
    @commands.command()
    async def optout(self, ctx):
        weebfile = self.dir + str(ctx.message.channel) + '/weeb_list.data'
        #check if .start was run by looking at the directory
        if not path.exists(weebfile):
            msg = 'You cant optout without starting the circle. Use **.start** to start the circle.'
            
        else:
            # open list from file to ensure most up to date version
            #with open('/home/pi/Bot_Archive/weeb_list.data', 'rb') as f:
            with open(weebfile, 'rb') as f:
                self.list = pickle.load(f)

            # go through list to find author and remove
            for member in self.list:
                if ctx.author.mention == member[0]:
                    self.list.remove(member)

            # update the list
            #with open('/home/pi/Bot_Archive/weeb_list.data', 'wb') as f:
            with open(weebfile, 'wb') as f:
                pickle.dump(self.list,f)

            msg = "{} has been removed from the list.".format(ctx.author.mention)
            
        await ctx.send(msg)
                
            
    # TODO: add a check to the oldlist so people dont get matched
    # two lists in a row
    @commands.guild_only()
    @commands.command()
    async def randomize(self, ctx):  
        weebfile = self.dir + str(ctx.message.channel) + '/weeb_list.data'
        #check if .start was run by looking at the directory
        if not path.exists(weebfile):
            msg = 'You cant randomize without starting the circle. Use **.start** to start the circle.'
            
        else:
            # open list from file to ensure most up to date version
            #with open('/home/pi/Bot_Archive/weeb_list.data', 'rb') as f:
            with open(weebfile, 'rb') as f:
                self.list = pickle.load(f)

            if not self.list:
                msg = "You can't randomize an empty list baka..."

            # check if the list has only one member based on col count
            elif len(self.list) == 1:
                msg = "You can't randomize a list with only 1 member baka..."

            # check if the rec command was run based on row count
            elif len(self.list[0]) > 3:
                msg = "You can't randomize again cause you already ran **.rec**..."

            else:
                # check to see if rand was done before, delete old partner
                for member in self.list:
                    if len(member) > 2:
                        member.pop(2)
                        
                # create numpy arrays for random function
                rand_array = np.array(self.list)
                old_array = np.array(self.list)

                # keep randomizing list until no one recommends themself
                while (rand_array[:,0] == old_array[:,0]).any():
                    np.random.shuffle(rand_array)

                # convert numpy array back to lists since its just easier
                #self.rand = rand_list.tolist()
                rand_list = rand_array.tolist()
                self.list = old_array.tolist()

                # add randomized partner to member, partner is who watches your recommended show
                for member,rand in zip(self.list,rand_list):
                    member.extend([rand[0]])

                # update the list
                #with open('/home/pi/Bot_Archive/weeb_list.data', 'wb') as f:
                with open(weebfile, 'wb') as f:
                    pickle.dump(self.list,f)

                # debug text printing
                #msg = "Not Rand:\n"
                #for member in self.list:
                #    msg += "{} wants to watch ".format(member[0])
                #    msg += "{} cour(s)\n".format(member[1])

                #msg += "\n\n Rand:\n"
                #for member in rand_list:
                #    msg += "{} wants to watch ".format(member[0])
                #    msg += "{} cour(s)\n".format(member[1])
                
                embed = discord.Embed(
                        title = 'Weebcircle List',
                        description = """Below is the list of all members who opted in and who they are recommending.""",
                        color = discord.Color.red()
                    )
                embed.set_thumbnail(url='https://pbs.twimg.com/profile_images/1148502291692965889/rdZ5NNWh_400x400.png')
                embed_field = ""
                for member in self.list:
                    embed_field += "{}, recommend {} an anime that is at most {} cour(s)\n".format(member[2], member[0], member[1])
                embed.add_field(name='__**Weebcircle:**__', value=embed_field, inline=False)
                await ctx.send(embed=embed)
                
                msg = "The list has been randomized, use **\".list\"** to see this list again"
        
        await ctx.send(msg)
        
        
    @commands.guild_only()    
    @commands.command()
    async def list(self, ctx):        
        weebfile = self.dir + str(ctx.message.channel) + '/weeb_list.data'
        #check if .start was run by looking at the directory
        if not path.exists(weebfile):
            msg = 'Use **.start** to start the circle.'
            await ctx.send(msg)
            
        else:            
            # open list from file to ensure most up to date version
            with open(weebfile, 'rb') as f:
                self.list = pickle.load(f) 

            if not self.list:
                msg = "The list is empty..."
                await ctx.send(msg)
                
            elif len(self.list[0]) < 3:
                msg = "You need to run **.randomize** before you can see a list..."
                await ctx.send(msg) 
            else:
                embed = discord.Embed(
                            title = 'Weebcircle List',
                            description = """Below is the list of all members who opted in and who they are recommending.""",
                            color = discord.Color.red()
                        )
                embed.set_thumbnail(url='https://pbs.twimg.com/profile_images/1148502291692965889/rdZ5NNWh_400x400.png')
                embed_field = ""
                for member in self.list:
                    embed_field += "{}, recommend {} an anime that is at most {} cour(s)\n".format(member[2], member[0], member[1])
                embed.add_field(name='__**Weebcircle:**__', value=embed_field, inline=False)
                await ctx.send(embed=embed)    
            
            
    @commands.guild_only()
    @commands.command()
    async def rec(self, ctx, *, arg):
        """Usage: Recommend an anime using this command"""
        
        weebfile = self.dir + str(ctx.message.channel) + '/weeb_list.data'
        #check if .start was run by looking at the directory
        if not path.exists(weebfile):
            msg = 'You cant rec without starting the circle. Use **.start** to start the circle.'
            
        else:
            # open list from file to ensure most up to date version
            #with open('/home/pi/Bot_Archive/weeb_list.data', 'rb') as f:
            with open(weebfile, 'rb') as f:
                self.list = pickle.load(f)

            if not self.list:
                msg = "You can't recommend to an empty list, baka..."

            # check list to see if only 1 member based on col count
            elif len(self.list) == 1:
                msg = "You can't recommend to yourself, baka..."

            # check if .randomize has run based on row count
            elif len(self.list[0]) < 3:
                msg = "You can't recommend without a partner, run the **.randomize** command first."

            else:
                # check if author is in list
                if not any(ctx.author.mention in list for list in self.list):
                    msg = "You can't recommend unless you are in the list, baka..."

                # look for author in list
                for member in self.list:
                    if member[2] == ctx.author.mention:

                        # check if author has already recommended
                        # could break cause hard coding index, but will add length checks
                        # to ensure commands can only work in a certain order
                        if len(member) >= 4:
                            member[3] = arg

                        else:
                            member.extend([arg])

                        # update the list
                        #with open('/home/pi/Bot_Archive/weeb_list.data', 'wb') as f:
                        with open(weebfile, 'wb') as f:
                            pickle.dump(self.list,f)

                        msg = "{} recommended {} to {}".format(ctx.author.mention, arg, member[0])
                
        await ctx.send(msg)

        
    @commands.guild_only()
    @commands.command()
    async def watch(self, ctx):
        weebfile = self.dir + str(ctx.message.channel) + '/weeb_list.data'
        weebfile_old = self.dir + str(ctx.message.channel) + '/weeb_list_old.data'
        
        #check if .start was run by looking at the directory
        if not path.exists(weebfile):
            msg = 'You cant watch without starting the circle. Use **.start** to start the circle.'
            await ctx.send(msg)
        
        elif not self.list:
            msg = 'You cant watch an empty list, baka...'
            await ctx.send(msg)
            
        else:
            msg = "none"

            for member in self.list:
                if len(member) < 4:
                    msg = "{} needs to recommend something using **.rec**...".format(member[2])
                    await ctx.send(msg)

            if msg == "none":                
                embed = discord.Embed(
                        title = 'Weebcircle Watch',
                        description = """Below is the list of all members who opted in and what anime they were recommended.""",
                        color = discord.Color.red()
                    )
                embed.set_thumbnail(url='https://pbs.twimg.com/profile_images/1148502291692965889/rdZ5NNWh_400x400.png')
                embed_field = ""
                for member in self.list:
                    embed_field += "{} watches *'{}'* (rec'd by {})\n".format(member[0], member[3], member[2])
                embed.add_field(name='__**Weebcircle:**__', value=embed_field, inline=False)
                await ctx.send(embed=embed)
                
                # save list to a file to track the old list
                with open(weebfile_old, 'wb') as f:
                    pickle.dump(self.list,f)
                    
        
    # DEBUG COMMANDS BELOW:    
    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def debugoldlist(self, ctx):
        # debug command to check if the oldlist was saved, nothing important
        weebfile_old = self.dir + str(ctx.message.channel) + '/weeb_list_old.data'
        
        #check if .start was run by looking at the directory
        if not path.exists(weebfile_old):
            msg = 'You cant use this command without starting the circle. Use **.start** to start the circle.'
            
        else:
            # open list from file to ensure most up to date version
            with open(weebfile_old, 'rb') as f:
                self.old = pickle.load(f)
                
            msg = "This is the oldlist: (format is: member, cour count, who recs this member, anime to watch)\n"

            for member in self.old:
                msg += "{}\n".format(member)
            
        await ctx.send(msg)
        
        
    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def debuglist(self, ctx):
        # debug command to ensure list is properly populated
        
        weebfile = self.dir + str(ctx.message.channel) + '/weeb_list.data'
        #check if .start was run by looking at the directory
        if not path.exists(weebfile):
            msg = 'Use **.start** to start the circle.'
            
        else:
            # open list from file to ensure most up to date version
            with open(weebfile, 'rb') as f:
                self.list = pickle.load(f)

            msg = "Current members: (format is: member, cour count, who recs this member, anime to watch)\n"

            for member in self.list:
                msg += "{}\n".format(member)

        await ctx.send(msg)
        
    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def clear(self, ctx):
        weebfile = self.dir + str(ctx.message.channel) + '/weeb_list.data'
        #check if .start was run by looking at the directory
        if not path.exists(weebfile):
            msg = 'Use **.start** to start the circle.'
            
        else:
            # debug command, to clear the list

            # set list to empty list
            self.list = []

            # write empty list to file
            #with open('/home/pi/Bot_Archive/weeb_list.data', 'wb') as f:
            with open(weebfile, 'wb') as f:
                pickle.dump(self.list,f)

            msg = "The list has been cleared"
        await ctx.send(msg)

    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def clearold(self, ctx):
        weebfile_old = self.dir + str(ctx.message.channel) + '/weeb_list_old.data'
        #check if .start was run by looking at the directory
        if not path.exists(weebfile_old):
            msg = 'Use **.start** to start the circle.'
            
        else:
            # debug command, to clear the list

            # set list to empty list
            self.old = []

            # write empty list to file
            #with open('/home/pi/Bot_Archive/weeb_list.data', 'wb') as f:
            with open(weebfile_old, 'wb') as f:
                pickle.dump(self.old,f)

            msg = "The old list has been cleared"
        await ctx.send(msg)
        
    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def debugadd(self, ctx, arg1, arg2, arg3, arg4):
        
        self.test.append([arg1, arg2, arg3, arg4])
        msg = "TEST COMMAND Current members: (format is: member, cour count, who recs this member, anime to watch)\n"
        for member in self.test:
            msg += "{}\n".format(member)
        await ctx.send(msg)
        
    @commands.guild_only()
    @checks.admin_or_permissions(manage_guild=True)
    @commands.command()
    async def debugload(self, ctx):
        weebfile = self.dir + str(ctx.message.channel) + '/weeb_list.data'
        #check if .start was run by looking at the directory
        if not path.exists(weebfile):
            msg = 'Use **.start** to start the circle.'
            
        self.list = self.test

        #with open('/home/pi/Bot_Archive/weeb_list.data', 'wb') as f:
        with open(weebfile, 'wb') as f:
            pickle.dump(self.list,f)
            
        msg = "TEST COMMAND Current members: (format is: member, cour count, who recs this member, anime to watch)\n"
        for member in self.test:
            msg += "{}\n".format(member)
        await ctx.send(msg)
