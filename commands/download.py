import os
import yt_dlp
from music_controls import *
from nextcord.ext import commands
from auxiliar import registrar_comando

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Registrar el comando en el bot
def setup(bot):
    registrar_comando(bot, download)

# Descargar música desde YouTube
@commands.command(name="download", aliases=["descargar"])
async def download(ctx, url):
    """Descarga la canción."""
    with yt_dlp.YoutubeDL() as ydl:
        video_info = ydl.extract_info(url, download=False)
        video_title = video_info['title']

    # Formatear el título del archivo
    safe_title = "".join(c for c in video_title if c.isalnum() or c in " -_").rstrip()
    file_path = os.path.join(download_folder, f"{safe_title}.mp3")

    if os.path.exists(file_path):
        await ctx.send(f"⚠️ **{video_title}** ya está descargado.")
        return

    # Enviar mensaje inicial
    message = await ctx.send(f"🎵 **Descargando:** `{video_title}`...")

    # Descargar la canción en formato MP3
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': file_path, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Editar el mensaje cuando la descarga termine
    await message.edit(content=f"✅ **Descargado:** `{video_title}`")
