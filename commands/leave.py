from nextcord.ext import commands
from auxiliar import registrar_comando

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
# Función para registrar el comando en el bot
def setup(bot):
    registrar_comando(bot, leave)

# Salir del canal de voz
@commands.command(name="leave", aliases=["salir"])
async def leave(ctx):
    """El bot se desconecta del canal de voz."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("¿Por qué me echas?")
    else:
        await ctx.send("¿Acaso me ves en un canal de voz?")