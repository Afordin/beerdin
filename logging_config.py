import logging
from patterns import Singleton

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


class Logger(metaclass=Singleton):
    """
        Clase para manejar los logs del bot
    """
    def __init__(self):
        # Configuración del logger
        self.logger = logging.getLogger("beerdin")
        self.logger.setLevel(logging.INFO)

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
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

        return self.logger

    def get_logger(self):
        return self.logger
    

def setup_logging():
    """
        Configura el logger del bot
    """
    return Logger().get_logger() # Return the logger instance
