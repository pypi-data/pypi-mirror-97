import os
import discord
from discord.ext import commands

#Main object used to create and run the bot
class Bot:

    def __init__(self, token):
        #Authentication tokens
        self.token = token

        #Bot Initialization
        self.client = commands.Bot(command_prefix=self._get_config())

        self._load_cogs()

    #Used to fetch the prefix set in the server, or the default prefix if not defined
    def _get_config(self):
        #To be implemented
        return '!'

    def _load_cog(self,cog):
        self.client.load_extension(cog)
        pass

    def _load_cogs(self):
        here = os.path.dirname(__file__)
        cogdir = os.path.join(here,'modules\\cogs')
        cogs = []

        for file in os.listdir(cogdir):
            print(file)
            if file.startswith('cog_') or file.endswith('.py'):
                cogs.append('modules.cogs.' + file[:-3])
                self._load_cog('modules.cogs.' + file[:-3])


    def start(self):
        self.client.run(self.TOKEN)

