import discord 
from discord.ext import commands
import asyncio

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class BeerdinBot(commands.Bot, metaclass=Singleton):
    def __init__(self, prefix="!", intents=None):
        if intents is None:
            intents = discord.Intents.default()
            
            intents.messages = True         # Enable receiving message events
            intents.message_content = True  # Necessary to read message content
            intents.reactions = True        # Enable receiving reaction events
            intents.voice_states = True     # Enable receiving voice state updates
            intents.guilds = True           # Enable receiving guild (server) updates
            intents.members = True          # Enable receiving member updates


        super().__init__(
            command_prefix=prefix,
            intents=intents,
            help_command=None
        )

    async def typing(ctx, embed=None, delay:int=2):
        async with ctx.typing():
            await asyncio.sleep(delay)
        if embed:
            await ctx.send(embed=embed)
    
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("⚠️ Comando no encontrado. Usa `!help`.")
        else:
            await ctx.send(f"❌ Error: {str(error)}")