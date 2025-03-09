from nextcord.ext import commands
from auxiliar import registrar_comando

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
# Función para registrar el comando en el bot
def setup(bot):
    registrar_comando(bot, pause)

# Pausar la música
@commands.command(name="pause", aliases=["pausar"])
async def pause(ctx):
    """Pausa la canción."""
    global is_paused
    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        is_paused = True
        await ctx.send("Música pausada.")
    else:
        await ctx.send("No hay música para pausar.")