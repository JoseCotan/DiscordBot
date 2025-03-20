from nextcord.ext import commands
from auxiliar import registrar_comando
from bot_config import song_queue

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
# Función para registrar el comando en el bot
def setup(bot):
    registrar_comando(bot, stop)

# Detener la música
@commands.command(name="stop", aliases=["detener"])
async def stop(ctx):
    """Detiene la canción."""
    voice_client = ctx.voice_client
    
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        song_queue.clear()
    else:
        await ctx.send("No estoy reproduciendo nada.")