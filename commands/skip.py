from nextcord.ext import commands
from auxiliar import registrar_comando

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
# Función para registrar el comando en el bot
def setup(bot):
    registrar_comando(bot, skip)

@commands.command(name="play")
@commands.has_role("DJ")
async def play(ctx, *, song: str):
    await ctx.send(f"🎶 Reproduciendo: {song}")

@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("🚫 Necesitas el rol **DJ** para usar este comando.")
        
# Saltar la canción actual
@commands.command(name="skip", aliases=["saltar", "next"])
async def skip(ctx):
    """Salta la canción actual."""
    voice_client = ctx.voice_client

    if not voice_client:
        await ctx.send("⚠️ No hay ninguna canción reproduciéndose.")
        return
    
    # Simplemente detener la canción y dejar que el after llame a play_next(ctx)
    voice_client.stop()
