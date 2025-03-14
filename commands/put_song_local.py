import os
import nextcord
from nextcord.ext import commands
from nextcord.ui import Modal, TextInput, View, Select
from bot_config import song_queue, config

@commands.command(name="put_song_local")
async def put_song_local_command(ctx, *, nombre_cancion):
    # Abre el modal para buscar canciones locales
    modal = PlayModalLocal()
    await ctx.send_modal(modal)

# Registrar el comando
def setup(bot):
    bot.add_command(put_song_local_command)

class PlayModalLocal(Modal):
    def __init__(self):
        super().__init__(
            title="Buscar canción local",
            timeout=60
        )
        self.cancion_input = TextInput(
            label="Nombre o parte del nombre de la canción",
            placeholder="Ejemplo: despacito",
            required=True,
            max_length=100
        )
        self.add_item(self.cancion_input)

    async def callback(self, interaction: nextcord.Interaction):
        # Recuperar el nombre de la canción y convertirlo a minúsculas
        nombre_cancion = self.cancion_input.value.lower()
        carpeta_canciones = "./canciones"

        # Buscar canciones que coincidan con el nombre proporcionado
        canciones_disponibles = [
            archivo for archivo in os.listdir(carpeta_canciones)
            if archivo.endswith(".mp3") and nombre_cancion in archivo.lower()
        ]

        if not canciones_disponibles:
            # Si no se encuentran canciones, avisar al usuario
            await interaction.response.send_message(
                f"❌ No se encontraron canciones que coincidan con: **{nombre_cancion}**",
                ephemeral=True
            )
            return

        # Mostrar un Select con las canciones encontradas
        view = SelectCancionesLocalModal(canciones_disponibles, interaction.user)
        await interaction.response.send_message(
            "🎵 Canciones encontradas, selecciona una para añadir a la cola:",
            view=view,
            ephemeral=True
        )


class SelectCancionesLocalModal(View):
    def __init__(self, canciones, usuario):
        super().__init__(timeout=60)
        self.usuario = usuario
        self.select = Select(
            placeholder="Selecciona una canción",
            options=[nextcord.SelectOption(label=c[:100], value=c) for c in canciones[:25]]  # Limitar a 25 canciones
        )
        self.select.callback = self.seleccion_cancion
        self.add_item(self.select)

    async def seleccion_cancion(self, interaction: nextcord.Interaction):
        # Solo permitir al usuario que abrió el modal hacer la selección
        if interaction.user != self.usuario:
            await interaction.response.send_message("⚠️ Solo el usuario que abrió el modal puede seleccionar.", ephemeral=True)
            return

        cancion_elegida = self.select.values[0]
        ruta = f"./canciones/{cancion_elegida}"

        # Agregar la canción seleccionada a la cola
        if 0 <= config.counter_song < len(song_queue):
            song_queue.insert(config.counter_song + 1, ruta)
        else:
            song_queue.append(ruta)

        await interaction.response.send_message(f"✅ **{cancion_elegida}** añadida a la cola.", ephemeral=True)
