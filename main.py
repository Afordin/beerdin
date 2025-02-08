from utils.bot_utils import setup_bot,typing
from decouple import config
import discord
from collections import Counter
from datetime import datetime, timedelta, timezone
from collections import Counter
# venv\Scripts\activate

DISCORD_TOKEN = input("Ingresa tu token de Discord: ").strip()
bot = setup_bot()
voice_context = {}
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
   
@bot.command(name="help",aliases=["h","ayuda"])
async def helper(ctx):
    embed_help=discord.Embed(title="**Helper**", color=0xff0000)
    embed_help.add_field(name="**Test**", value="**Prueba ok**", inline=True)
    await typing(ctx,embed=embed_help,time=1)

@bot.command(name="mensajes")
async def analizar_mensajes(ctx, tipo: str = None, valor: str = None):
    """Analiza los mensajes del canal actual según la opción elegida."""
    now = datetime.now(timezone.utc)
    today = now.date()
    last_30_days = now - timedelta(days=30)

    mensajes_por_mes = Counter()
    mensajes_por_dia = Counter()
    mensajes_por_usuario = Counter()

    async for message in ctx.channel.history(limit=5000, after=last_30_days):
        fecha = message.created_at
        mensajes_por_mes[(fecha.year, fecha.month)] += 1
        mensajes_por_dia[fecha.date()] += 1
        mensajes_por_usuario[message.author.name] += 1

    # **Mensajes por mes**
    if tipo == "mes":
        if valor:  # Formato "YYYY-MM"
            try:
                year, month = map(int, valor.split('-'))  # Convertimos a enteros para coincidir con las claves
                result = mensajes_por_mes.get((year, month), 0)
                await ctx.send(f"📆 Mensajes en {year}-{str(month).zfill(2)}: **{result}**")
            except ValueError:
                await ctx.send("Formato inválido. Usa `YYYY-MM`, por ejemplo `!mensajes mes 2024-01`")
        else:
            result = mensajes_por_mes.get((now.year, now.month), 0)
            await ctx.send(f"📆 Mensajes en {now.year}-{str(now.month).zfill(2)}: **{result}**")

    # **Mensajes por día**
    elif tipo == "día":
        dias = int(valor) if valor and valor.isdigit() else 1
        result = "\n".join([f"{date}: {count}" for date, count in mensajes_por_dia.items() if date >= today - timedelta(days=dias)])
        await ctx.send(f"📊 Mensajes de los últimos {dias} días:\n{result}" if result else "No hay mensajes en el período solicitado.")

    # **Mensajes por usuario**
    elif tipo == "usuario":
        if valor:  # Si se especifica un usuario
            usuario, dias = (valor.split()[0], int(valor.split()[1])) if len(valor.split()) == 2 and valor.split()[1].isdigit() else (valor, 30)
            mensajes_usuario = mensajes_por_usuario.get(usuario, 0)
            await ctx.send(f"👤 Mensajes de **{usuario}** en los últimos {dias} días: **{mensajes_usuario}**")
        else:  # Si no se especifica usuario, mostrar todos
            result = "\n".join([f"{user}: {count}" for user, count in mensajes_por_usuario.items()])
            await ctx.send(f"👤 Mensajes por usuario:\n{result}")

    else:
        await ctx.send("⚠️ Opción inválida. Usa `!mensajes mes YYYY-MM`, `!mensajes día [N]` o `!mensajes usuario [nombre] [N días]`.")


@bot.command(name="analizar")
async def analizar_emojis(ctx, limit: int = 100):
    """Analiza los últimos N mensajes del canal y cuenta los emojis usados."""
    emoji_counter = Counter()

    async for message in ctx.channel.history(limit=limit):
        for reaction in message.reactions:
            emoji_counter[reaction.emoji] += reaction.count  # Sumar el número de reacciones


    if not emoji_counter:
        await ctx.send("No se encontraron emojis en los últimos mensajes.")
        return
    
    result = "\n".join([f"{emoji}: {count} veces" for emoji, count in emoji_counter.most_common()])
    # await ctx.send(f"**Uso de emojis en los últimos {limit} mensajes:**\n{result}")
    embed_help=discord.Embed(title="**Helper**", color=0xff0000)
    embed_help.add_field(name=f"**Uso de emojis en los últimos {limit} mensajes:**", value=f"**{result}**", inline=True)
    await typing(ctx,embed=embed_help,time=1)

bot.run(DISCORD_TOKEN)