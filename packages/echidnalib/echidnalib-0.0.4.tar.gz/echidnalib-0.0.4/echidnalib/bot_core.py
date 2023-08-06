import os
import logging
import discord
from discord.ext import commands

#Main object used to create and run the bot
class Bot:

    def __init__(self, token, cog_directory='none'):
        #initialize logging
        self._setup_logging()

        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        intents = discord.Intents(
            guilds=True,
            members=True,
            bans=True,
            emojis=True,
            voice_states=True,
            messages=True,
            reactions=True,
        )

        #Authentication tokens
        self.token = token

        #Bot Initialization
        self.client = commands.Bot(command_prefix=self._get_config(),
                         pm_help=None, help_attrs=dict(hidden=True),
                         fetch_offline_members=False, heartbeat_timeout=150.0,
                         allowed_mentions=allowed_mentions, intents=intents)

        if cog_directory is not 'none':
            self._load_cogs(cog_directory)

    def _setup_logging(self):
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        self.handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(self.handler)

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

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandNotFound):
            await ctx.author.send('Command not found.')
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(error)
        else:
            await ctx.send(error)

    async def on_ready(self):
        print()


    def start(self):
        self.client.run(self.token)

