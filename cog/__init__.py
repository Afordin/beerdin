import os

async def load_cogs(bot):
    """
        Cargar los cogs a excepcion de __init__.py
    """

    cogs_folder = os.path.join(os.path.dirname(__file__), 'cogs')
    for filename in os.listdir(cogs_folder):
        if filename.endswith(".py") and filename != "__init__.py":
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"✅ Cargado correctamente cog: {cog_name}")
            except Exception as e:
                print(f"❌ Fallo al cargar {cog_name}: {e}")
