import random
import os
from music_controls import song_queue, download_folder, play_next
from nextcord.ext import commands
from auxiliar import registrar_comando

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
# Función para registrar el comando en el bot
def setup(bot):
    registrar_comando(bot, lista)


@commands.command(name="lista")
async def lista(ctx, *, nombre: str):
    """Reproduce una lista de reproducción aleatoriamente desde la carpeta './listas'."""
    playlist_path = f"./listas/{nombre}.txt"  # Buscar en la carpeta './listas'
    
    if not os.path.exists(playlist_path):
        await ctx.send(f"La lista `{nombre}` no existe en la carpeta `listas`.")
        return
    
    with open(playlist_path, 'r') as f:
        canciones = f.read().splitlines()
    
    if not canciones:
        await ctx.send(f"La lista `{nombre}` está vacía.")
        return
    
    # Verificar si el bot está conectado a un canal de voz
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"Me uní a {channel.name} para mezclar las canciones. PONGAMOS {nombre}!")
        else:
            await ctx.send("No estás en un canal de voz, no puedo unirme.")
            return
    
    random.shuffle(canciones)  # Mezclar aleatoriamente
    mensaje_cola = "🎶 Las canciones han sido añadidas aleatoriamente a la cola:\n"
    
    # Si no hay música reproduciéndose, añadir las canciones a la cola y comenzar a reproducir la primera
    for file in canciones:
        file_path = os.path.join(download_folder, file)  # Asegúrate de que los archivos están en la carpeta correcta
        song_queue.append(file_path)
    
    # Mostrar las primeras 10 canciones de la cola
    for i, cancion in enumerate(song_queue[:10]):
        mensaje_cola += f"🎵 **{i+1}.- ** {cancion[12:]}\n"
    
    # Si hay más de 10 canciones, agregar los puntos suspensivos
    if len(song_queue) > 10:
        mensaje_cola += "...\n"
    
    # Si ya hay música reproduciéndose
    if not ctx.voice_client.is_playing():
        # Reproducir la primera canción de la cola mezclada
        await play_next(ctx)
        
    await ctx.send(mensaje_cola)
