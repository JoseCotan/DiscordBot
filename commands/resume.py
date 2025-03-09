from nextcord.ext import commands
from auxiliar import registrar_comando

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
# Función para registrar el comando en el bot
def setup(bot):
    registrar_comando(bot, resume)

# Reanudar la música pausada
@commands.command(name="resume", aliases=["reanudar"])
async def resume(ctx):
    """Reanuda la canción."""
    global is_paused
    voice_client = ctx.voice_client
    if voice_client and not voice_client.is_playing():
        voice_client.resume()
        is_paused = False
        await ctx.send("Música reanudada.")
    else:
        await ctx.send("No hay música pausada para reanudar.")
