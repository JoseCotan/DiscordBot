import os
import nextcord
import asyncio
import subprocess
from nextcord.ext import commands
from bot_config import song_queue

class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tts")
    async def tts(self, ctx, *, texto: str):
        """Convierte texto en voz y lo reproduce en Discord con Espeak."""
        if not ctx.author.voice:
            await ctx.send("❌ Debes estar en un canal de voz.")
            return

        if song_queue != []:
            await ctx.send("❌ No puedes usar el TTS mientras haya canciones en cola.")
            return

        channel = ctx.author.voice.channel
        vc = ctx.voice_client
        if not vc:
            vc = await channel.connect()

        # Usar espeak para generar el audio
        subprocess.run([
            "C:\\Program Files (x86)\\eSpeak\\command_line\\espeak.exe", 
            "-v", "es+m3", "-s", "150", "-p", "60", "-w", "voz.wav", texto])
        # Convertir a MP3 para reproducirlo en Discord
        subprocess.run(["ffmpeg", "-i", "voz.wav", "-filter:a", "volume=20", "voz.mp3", "-y"])

        # Reproducir el audio
        vc.play(nextcord.FFmpegPCMAudio("voz.mp3"), after=lambda e: print("Reproducción terminada"))

        while vc.is_playing():
            await asyncio.sleep(1)

        os.remove("voz.wav")
        os.remove("voz.mp3")

# Registrar el comando en el bot
def setup(bot):
    bot.add_cog(TTS(bot))
