# Version: 1.0

import discord
import os
import logging
import asyncpg
import sys

from dotenv import load_dotenv
from database import DatabaseManager
from discord.ext import commands
from cog import load_cogs

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


class LoggingFormatter(logging.Formatter):
    """
        Clase para dar formato a los logs del bot
    """
    # Colores
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    
    # Formatos
    reset = "\x1b[0m"
    bold = "\x1b[1m"
    
    # Colores para los logs
    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        """
            Formatea el log
        """
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)

# Configuración del logger
logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# Manejadores de logs
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())

# Manejador de logs en archivo
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Añadir los manejadores al logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

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