import os
import random
from nextcord.ext import commands
from auxiliar import registrar_comando
from music_controls import song_queue, download_folder, play_next

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
# Función para registrar el comando en el bot
def setup(bot):
    registrar_comando(bot, mix)

# Comando $mix con argumento opcional
@commands.command(name="mix")
async def mix(ctx, *, query=None):
    """Añade de forma aleatoria todas las canciones a la cola. 
    
    Con $mix don omar, añade todas las canciones que tenga 'don omar'"""
    # Verificar si el bot está conectado a un canal de voz
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"Me uní a {channel.name} para mezclar las canciones. DJ BOT TRAVIESO IS HERE!")
        else:
            await ctx.send("No estás en un canal de voz, no puedo unirme.")
            return

    # Obtener todas las canciones MP3 en la carpeta raíz
    files = os.listdir(download_folder)
    mp3_files = [f for f in files if f.endswith(".mp3")]

    if not mp3_files:
        await ctx.send("No hay canciones MP3 en la carpeta para mezclar.")
        return

    # Filtrar las canciones si se proporcionó un término de búsqueda
    if query:
        mp3_files = [f for f in mp3_files if query.lower() in f.lower()]

    if not mp3_files:
        await ctx.send(f"No se encontraron canciones que coincidan con '{query}'." if query else "No hay canciones en la carpeta para mezclar.")
        return

    # Mezclar las canciones aleatoriamente
    random.shuffle(mp3_files)

    # Verificar si ya se está reproduciendo una canción
    if ctx.voice_client.is_playing():
        # Si ya hay música reproduciéndose, solo añadir las canciones a la cola
        for file in mp3_files:
            file_path = os.path.join(download_folder, file)
            song_queue.append(file_path)
        await ctx.send(f"🎶 Las canciones han sido añadidas aleatoriamente a la cola{' para el término de búsqueda: ' + query if query else ''}.")
    else:
        # Si no hay música reproduciéndose, añadir las canciones a la cola y comenzar a reproducir la primera
        for file in mp3_files:
            file_path = os.path.join(download_folder, file)
            song_queue.append(file_path)

        # Reproducir la primera canción de la cola mezclada
        await play_next(ctx)
        await ctx.send(f"🎶 Las canciones han sido añadidas aleatoriamente a la cola{' para el término de búsqueda: ' + query if query else ''} y se está reproduciendo la primera canción.")