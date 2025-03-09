import os
import asyncio
from nextcord.ext import commands
from nextcord import Interaction, SelectOption
from nextcord.ui import View, Select
from music_controls import *
from auxiliar import registrar_comando
from bot_config import download_folder

# Función para registrar el comando en el bot
def setup(bot):
    registrar_comando(bot, search)

class CancionSelect(Select):
    def __init__(self, canciones):
        options = [
            SelectOption(label=os.path.basename(c)[:-4], value=c) for c in canciones
        ]
        super().__init__(
            placeholder="🎵 Selecciona una o más canciones",
            options=options,
            min_values=1,
            max_values=len(options)
        )

    async def callback(self, interaction: Interaction):
        self.view.canciones_seleccionadas = self.values
        await interaction.response.send_message(
            f"✅ Canciones seleccionadas: {', '.join([os.path.basename(c)[:-4] for c in self.values])}",
            ephemeral=True
        )
        self.view.stop()

@commands.command(name="search", aliases=["buscar"])
async def search(ctx, *, query):
    """Busca la canción según el nombre [ $search don omar ]"""
    
    files = os.listdir(download_folder)
    matching_files = [f for f in files if query.lower() in f.lower() and f.endswith(".mp3")]
    voice_client = ctx.voice_client

    if not matching_files:
        await ctx.send("No se encontraron canciones con ese nombre.")
        return
        
    cancion_view = View()
    cancion_view.add_item(CancionSelect(matching_files))
    seleccion_cancion_msg = await ctx.send("🎶 Selecciona las canciones:", view=cancion_view)

    try:
        await asyncio.wait_for(cancion_view.wait(), timeout=30)
    except asyncio.TimeoutError:
        await seleccion_cancion_msg.delete()
        await ctx.send("⏳ Tiempo de selección expirado.", delete_after=5)
        return

    if not hasattr(cancion_view, 'canciones_seleccionadas'):
        await seleccion_cancion_msg.delete()
        await ctx.send("⏳ No se seleccionaron canciones.", delete_after=5)
        return

    canciones_seleccionadas = cancion_view.canciones_seleccionadas

    for cancion in canciones_seleccionadas:
        file_path = os.path.join(download_folder, cancion)
        await ctx.send(f"➖➖🔹**NUEVA CANCIÓN EN COLA**🔹➖➖\n 🎶 **{os.path.basename(file_path)}** 🎶\n📀 Canciones restantes en cola: **{len(song_queue) - config.counter_song}**")
        if ctx.voice_client and ctx.voice_client.is_playing():
            song_queue.append(file_path)
        else:
            await ctx.invoke(join)
            song_queue.append(file_path)  
            await play_next(ctx)

    # Elimina el mensaje de selección
    await seleccion_cancion_msg.delete()
    # Elimina el mensaje del usuario con el comando $search
    await ctx.message.delete()
    