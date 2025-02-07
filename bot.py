# Version: 1.0
import discord
import os
import sys

from dotenv import load_dotenv
from database import DatabaseManager
from discord.ext import commands
from cog import load_cogs
from logging_config import setup_logging

# Cargar las variables de entorno
load_dotenv()

"""
    Variables de entorno necesarias para el bot
"""
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MONGODB = os.getenv('MONGODB')
PREFIX = os.getenv('PREFIX', '!') # Prefijo de los comandos, si no lo encuentra, carga el '!' por defecto
LANGUAGE = os.getenv('LANGUAGE', 'es') # Idioma del bot, si no lo encuentra, carga el 'es' por defecto

"""
    Configuración de los intents necesarios para el bot
"""
intents = discord.Intents.default()
intents.emojis = True                    # Necesario para on_reaction_add
intents.guilds = True                    # Necesario para on_guild_join
intents.presences = True                 # Necesario para on_member_update
intents.reactions = True                 # Necesario para on_reaction_add
intents.typing = True                    # Necesario para on_typing
intents.voice_states = True              # Necesario para on_voice_state_update
intents.integrations = True              # Necesario para on_integration_update

# Intents Privilegiados (Requieren permisos especiales)
intents.members = True                   # Necesario para on_member_join
intents.message_content = True           # Necesario para on_message
intents.messages = True                  # Necesario para on_message

# Configuración del logger
logger = setup_logging()

class DiscordBot(commands.Bot):
    """
        Esta es la clase principal del bot, hereda de commands.Bot que es una subclase de discord.Client.
    """
    def __init__(self) -> None:
        """
            Inicializa la clase DiscordBot
        """
        super().__init__(command_prefix=PREFIX, intents=intents)
        self.database = DatabaseManager()

    async def init_db(self) -> None:
        """
            Inicializa la base de datos del bot
        """
        pass

if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: El token no se ha encontrado en el archivo .env")
        sys.exit(1)

    bot = DiscordBot()

    @bot.event
    async def on_ready():
        print(f'✅ Se ha iniciado correctamente como {bot.user}')
        await load_cogs(bot)

    bot.run(TOKEN)