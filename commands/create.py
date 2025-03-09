import os
from nextcord.ext import commands
from auxiliar import registrar_comando
from music_controls import list_folder

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Función para registrar el comando en el bot
def setup(bot):
    registrar_comando(bot, crear)

@commands.command(name="create", aliases=["crear"])
async def crear(ctx, *, nombre: str):
    """Crea una lista de reproducción [ $crear don omar ]"""
    ruta = os.path.join(list_folder, f"{nombre}.txt")
    
    # Crear la carpeta si no existe
    if not os.path.exists(list_folder):
        os.makedirs(list_folder)
    
    if os.path.exists(ruta):
        await ctx.send(f"La lista de reproducción `{nombre}` ya existe.")
    else:
        with open(ruta, "w") as f:
            pass  # Crea un archivo vacío
        await ctx.send(f"✅ Lista de reproducción `{nombre}` creada exitosamente.")
