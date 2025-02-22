from config import getConfig
from utils.bot_utils import setup_bot,typing
import discord
from collections import Counter
from datetime import datetime, timedelta, timezone


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
        mensajes_por_usuario[message.author.id] += 1

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
            partes = valor.split()
            user_id = None

            # Si es una mención "<@12312353334>"
            if partes[0].startswith("<@") and partes[0].endswith(">"):
                user_id = partes[0].strip("<@>")
            elif partes[0].isdigit():  # Si ya es un ID
                user_id = partes[0]
            else:  # Buscar por nombre de usuario
                usuario_obj = discord.utils.get(ctx.guild.members, name=partes[0])
                if usuario_obj:
                    user_id = str(usuario_obj.id)

            # Verificamos si se obtuvo un ID válido
            if user_id and user_id.isdigit():
                usuario_obj = discord.utils.get(ctx.guild.members, id=int(user_id))

                if usuario_obj:  # Si el usuario existe en el servidor
                    dias = int(partes[1]) if len(partes) > 1 and partes[1].isdigit() else 30
                    mensajes_usuario = mensajes_por_usuario.get(int(user_id), 0)

                    await ctx.send(f"👤 Mensajes de **{usuario_obj.display_name}** en los últimos {dias} días: **{mensajes_usuario}**")
                else:
                    await ctx.send("❌ No se encontró el usuario en este servidor.")
            else:
                await ctx.send("❌ No se pudo identificar el usuario. Usa una mención, un ID o un nombre válido.")
        else:  # Si no se especifica usuario, mostrar todos
            result = "\n".join([f"<@{user_id}>: {count}" for user_id, count in mensajes_por_usuario.items()])
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

if __name__ == "__main__":
    bot.run(getConfig().DISCORD_TOKEN.get_secret_value())