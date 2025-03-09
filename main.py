import os
import secrets
from nextcord.ext import commands
from nextcord import Interaction
from auxiliar import *
from dotenv import load_dotenv
from bot_config import *
load_dotenv()

# 🎯 ID o nombre del rol permitido (ajusta esto a tu rol)
ROL_PERMITIDO = "DJ"  # Puedes usar el nombre o el ID del rol

# ✅ Check global para permitir solo a usuarios con el rol especificado
def tiene_rol_permitido(ctx):
    return any(role.name == ROL_PERMITIDO for role in ctx.author.roles)

# 🛡️ Agrega el check global para todos los comandos
bot.add_check(tiene_rol_permitido)

# 🚫 Mensaje personalizado si el usuario no tiene el rol requerido
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("🚫 No tienes permiso para usar este comando.")
    else:
        raise error

# 🚀 Cargar los comandos desde la carpeta "comandos"
for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        extension = f"commands.{filename[:-3]}"
        try:
            if extension not in bot.extensions:
                bot.load_extension(extension)
            print(f"✅ Cargado: {extension}")
        except Exception as e:
            print(f"❌ Error al cargar {extension}: {e}")

# 🟢 Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# 🔑 Ejecutar el bot
bot.run(secrets.TOKEN)