import discord 
from discord.ext import commands
import asyncio
def setup_bot(prefix="!", intents=None):
    """Configura y devuelve una instancia del bot."""
    if intents is None:
      intents = discord.Intents.default()
    intents.message_content = True  # Necesario para leer mensajes
    intents.guilds = True  # Información de servidores
    intents.members = True  # Para acceder a miembros

    bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)
    return bot

async def typing(ctx, embed=None,time:int=2):
    async with ctx.typing():
        await asyncio.sleep(time)

    if embed:
        await ctx.send(embed=embed)
