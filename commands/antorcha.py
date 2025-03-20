import os
from nextcord.ext import commands

def setup(bot):
    bot.add_command(antorcha)

FIRMAS_FILE = "./antorcha_firmas.txt"

def leer_firmas():
    if not os.path.exists(FIRMAS_FILE):
        with open(FIRMAS_FILE, "w") as f:
            f.write("0")
    with open(FIRMAS_FILE, "r") as f:
        return int(f.read().strip())

def guardar_firmas(cantidad):
    with open(FIRMAS_FILE, "w") as f:
        f.write(str(cantidad))

@commands.command(name="antorcha")
async def antorcha(ctx):
    """Ayuda a Antorcha a que active Windows!"""
    firmas = leer_firmas()
    firmas += 1
    guardar_firmas(firmas)
    await ctx.send(f"🔥 Se han juntado **{firmas} firmas** para que Antorcha active Windows 🔥")

