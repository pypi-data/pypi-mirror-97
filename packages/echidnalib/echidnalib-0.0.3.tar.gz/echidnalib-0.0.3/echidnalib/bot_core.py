import os
import discord
from discord.ext import commands

#Main object used to create and run the bot
class Bot:

    def __init__(self, token, cog_directory='none'):
        #Authentication tokens
        self.token = token

        #Bot Initialization
        self.client = commands.Bot(command_prefix=self._get_config())

        if cog_directory is not 'none':
            self._load_cogs(cog_directory)

    #Used to fetch the prefix set in the server, or the default prefix if not defined
    def _get_config(self):
        #To be implemented
        return '!'

    def _load_cog(self,cog):
        self.client.load_extension(cog)
        pass

    def _load_cogs(self,cogdir):
        cogs = []

        for file in os.listdir(cogdir):
            print(file)
            if file.startswith('cog_') or file.endswith('.py'):
                cogs.append('cogs.' + file[:-3])
                self._load_cog('cogs.' + file[:-3])


    def start(self):
        self.client.run(self.token)

