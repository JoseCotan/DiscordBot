import yt_dlp
from music_controls import *
from nextcord.ext import commands
from auxiliar import registrar_comando

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
# Función para registrar el comando en el bot
def setup(bot):
    registrar_comando(bot, play)

# Reproducir música desde YouTube
@commands.command(name="play", aliases=["reproducir"])
async def play(ctx, url):
    """Reproduce la canción."""
    voice_client = ctx.voice_client

    if not voice_client:
        await ctx.invoke(join)

    # Obtener información de la canción
    with yt_dlp.YoutubeDL() as ydl:
        video_info = ydl.extract_info(url, download=False)
        video_title = video_info['title']
        
    # Formatear el título del archivo
    safe_title = "".join(c for c in video_title if c.isalnum() or c in " -_").rstrip()
    file_path = os.path.join(download_folder, f"{safe_title}.mp3")

    if not os.path.exists(file_path):  # Evitar descargas duplicadas
        message = await ctx.send(f"🎶 **Descargando:** `{video_title}`... 🎶")
        ydl_opts = {'format': 'bestaudio/best', 'outtmpl': file_path, 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        await message.edit(content=f"✅ **Descargado:** `{video_title}` ✅")

    # Si ya hay música sonando, agregar a la cola
    if voice_client and voice_client.is_playing():
        song_queue.append(file_path)  # Asegurar que la cola tenga archivos reales
        await ctx.send(f"➖➖🔹**NUEVA CANCIÓN EN COLA**🔹➖➖\n 🎶 **{os.path.basename(file_path)}** 🎶\n📀 Canciones restantes en cola: **{len(song_queue) - config.counter_song - 1}**")
    else:
        # Si no hay música sonando, empezar la reproducción
        song_queue.append(file_path)
        await ctx.send(f"➖➖🔹**NUEVA CANCIÓN EN COLA**🔹➖➖\n 🎶 **{os.path.basename(file_path)}** 🎶\n📀 Canciones restantes en cola: **{len(song_queue) - config.counter_song - 1}**")
        await play_next(ctx)