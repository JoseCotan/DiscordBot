import os
import asyncio
from nextcord.ext import commands
from auxiliar import registrar_comando
from bot_config import *

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
# Función para registrar el comando en el bot
def setup(bot):
    registrar_comando(bot, queue)


@commands.command(name="queue", aliases=["cola"])
async def queue(ctx):
    """Muestra las siguientes 10 canciones de la cola."""
    if not song_queue:
        await ctx.send("🚫 **La cola está vacía.**")
    else:
        # Empezamos a construir el mensaje de la cola
        queue_list = "**Cola de música:**\n\n"

        # Añadimos las primeras 10 canciones
        queue_list += "\n".join([f"🎵 **{i+1}.- ** {os.path.splitext(os.path.basename(song))[0]}" for i, song in enumerate(song_queue[config.counter_song + 1:][:10])])

        # Si hay más de 10 canciones, añadimos "..."
        if len(song_queue) > 10:
            queue_list += "\n\n**...y más canciones en la cola...**"

        # Enviar el mensaje de la cola con formato
        message = await ctx.send(queue_list)

        # Eliminar el mensaje después de 20 segundos
        await asyncio.sleep(20)
        await message.delete()