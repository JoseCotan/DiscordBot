import os
import yt_dlp
from nextcord.ext import commands
from auxiliar import registrar_comando
from bot_config import download_folder, song_queue, config
import re

# Comando de Discord
@commands.command(name="put_song")
async def put_song_command(ctx, url):
    await put_song(ctx, url)

# Registrar el comando
def setup(bot):
    registrar_comando(bot, put_song_command)

# Función reutilizable para descargar la canción
async def put_song(ctx, url):

    # Comprobar si la URL es válida
    if not is_valid_url(url):
        # Si no es una URL, buscar la canción en YouTube
        search_url = f"ytsearch:{url}"
        url = get_youtube_url_from_search(search_url)

    # Obtener información del video usando yt-dlp
    with yt_dlp.YoutubeDL() as ydl:
        video_info = ydl.extract_info(url, download=False)
        video_title = video_info['title']

    # Formatear el título del archivo
    safe_title = "".join(c for c in video_title if c.isalnum() or c in " -_").rstrip()
    file_path = os.path.join(download_folder, f"{safe_title}.mp3")

    if os.path.exists(file_path):
        await ctx.send(f"⚠️ **{video_title}** ya está descargado.")
        
    else: 
        # Enviar mensaje inicial
        message = await ctx.send(f"🎵 **Descargando:** {video_title}...")

        # Descargar la canción en formato MP3
        ydl_opts = {'format': 'bestaudio/best', 'outtmpl': file_path, 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Actualizar el mensaje de descarga
        await message.edit(content=f"✅ **Descargado:** {video_title}")
        
    # Insertar la canción en la cola en la posición indicada por `config.counter_song`
    if 0 <= config.counter_song < len(song_queue):
        song_queue.insert(config.counter_song + 1, f"./canciones\{video_title}.mp3")  # Insertar en la posición deseada
    else:
        song_queue.append(video_title)  # Si la posición no es válida, agregar al final
        
    # Enviar mensaje con la cola actualizada
    await ctx.send(f"🔊 **Canción agregada a la cola:** {video_title}")

# Función para verificar si la entrada es una URL válida
def is_valid_url(url):
    return re.match(r"(https?://[^\s]+)", url) is not None

# Función para obtener la URL de YouTube usando la búsqueda de yt-dlp
def get_youtube_url_from_search(search_query):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info_dict = ydl.extract_info(search_query, download=False)
        if 'entries' in info_dict and len(info_dict['entries']) > 0:
            video = info_dict['entries'][0]
            if 'webpage_url' in video:
                return video['webpage_url']  # Obtener la URL del video desde webpage_url
            else:
                raise ValueError("La URL del video no se encontró en los resultados de búsqueda.")
        else:
            raise ValueError("No se encontró ningún resultado para la búsqueda.")
