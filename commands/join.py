from nextcord.ext import commands
from auxiliar import registrar_comando

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
# Función necesaria para cargar el comando
def setup(bot):
    registrar_comando(bot, join)

# Conectarse a un canal de voz
@commands.command(name="join", aliases=["unirse"])
async def join(ctx):
    """El bot se une al canal de voz."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Me uní a {channel.name}!")
    else:
        await ctx.send("¿Quieres escuchar música sin estar en un canal de voz? Buena esa")
        
        
