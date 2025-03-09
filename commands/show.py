import os
from nextcord.ext import commands
from auxiliar import registrar_comando

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
# Función para registrar el comando en el bot
def setup(bot):
    registrar_comando(bot, mostrar)


@commands.command(name="show", aliases=["mostrar"])
async def mostrar(ctx, nombre: str):
    """Muestra las canciones dentro de una lista de reproducción."""
    playlist_path = f"{nombre}.txt"

    if not os.path.exists(playlist_path):
        await ctx.send(f"❌ La lista `{nombre}` no existe.")
        return

    with open(playlist_path, 'r') as f:
        canciones = f.read().splitlines()

    if not canciones:
        await ctx.send(f"📂 La lista `{nombre}` está vacía.")
        return

    # Formatear las canciones para mostrarlas
    mensaje = f"📜 **Lista de reproducción: {nombre}**\n\n"
    mensaje += "\n".join([f"🎵 **{i+1}.-** {os.path.basename(c)}" for i, c in enumerate(canciones[:20])])

    if len(canciones) > 20:
        mensaje += "\n... y más 🎶"

    await ctx.send(mensaje)