from nextcord.ext import commands
from auxiliar import registrar_comando

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
# Función para registrar el comando en el bot
def setup(bot):
    registrar_comando(bot, commands_list)


@commands.command(name="commands", aliases=["comandos"])
async def commands_list(ctx):
    """Muestra los comandos del bot (desactualizado)"""
    commands_text = """
    **Comandos disponibles:**

**$unirse**: Únete al canal de voz en el que estás.
**$salir**: Sal del canal de voz en el que estás.
**$reproducir [URL]**: Reproduce una canción desde YouTube.
**$detener**: Detén la música.
**$pausar**: Pausa la música actual.
**$reanudar**: Reanuda la música pausada.
**$saltar**: Salta la canción actual.
**$buscar**: Busca el nombre de la canción.
**$cola**: Muestra la cola actual de música.
**$mix**: Añade a la cola todas las canciones.
**$mix [Nombre]**: Añade a la cola todas las canciones con el nombre buscado.
**$comandos**: Muestra esta lista de comandos y su descripción.

**In English for Pengu:**

**$join**: Join the voice channel you're in.
**$leave**: Leave the voice channel you're in.
**$play [URL]**: Play a song from YouTube.
**$stop**: Stop the music.
**$pause**: Pause the current song.
**$resume**: Resume the paused song.
**$skip/next**: Skip the current song.
**$search**: Search for the song name.
**$queue**: Displays the current music queue.
**$mix**: Add all songs to queue.
**$mix[name]**: Add all songs with the searched name to the queue.
**$commands**: Shows this list of commands and their description.
    """
    await ctx.send(commands_text)

