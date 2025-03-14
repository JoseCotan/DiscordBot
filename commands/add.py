import glob
import os
import asyncio
from nextcord.ext import commands
from nextcord import Interaction, SelectOption
from nextcord.ui import View, Select
from music_controls import song_queue

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

class ListaSelect(Select):
    def __init__(self, listas):
        options = [
            SelectOption(label=os.path.basename(l)[:-4], value=l) for l in listas
        ]
        super().__init__(placeholder="📂 Selecciona la lista de reproducción", options=options)

    async def callback(self, interaction: Interaction):
        self.view.lista_seleccionada = self.values[0]
        await interaction.response.send_message(
            f"📥 Lista seleccionada: **{os.path.basename(self.values[0])[:-4]}**",
            ephemeral=True
        )
        self.view.stop()

class Agregar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="agregar", aliases=["add"])
    async def agregar(self, ctx, *, nombre: str):
        """Agrega canciones a una lista de reproducción. [ $agregar don omar ]"""
        canciones = glob.glob("./canciones/*.mp3")
        coincidencias = [c for c in canciones if nombre.lower() in os.path.basename(c).lower()]

        if not coincidencias:
            msg = await ctx.send("❌ No se encontraron canciones con ese nombre.")
            await asyncio.sleep(60)
            await msg.delete()
            return

        cancion_view = View()
        cancion_view.add_item(CancionSelect(coincidencias))
        seleccion_cancion_msg = await ctx.send("🎶 Selecciona las canciones:", view=cancion_view)

        try:
            await asyncio.wait_for(cancion_view.wait(), timeout=60)
        except asyncio.TimeoutError:
            await seleccion_cancion_msg.delete()
            await ctx.send("⏳ Tiempo de selección expirado.", delete_after=5)
            return

        if not hasattr(cancion_view, 'canciones_seleccionadas'):
            await seleccion_cancion_msg.delete()
            await ctx.send("⏳ No se seleccionaron canciones.", delete_after=5)
            return

        listas = glob.glob("./listas/*.txt")
        if not listas:
            msg = await ctx.send("❌ No hay listas de reproducción disponibles.")
            await asyncio.sleep(60)
            await msg.delete()
            return

        lista_view = View()
        lista_view.add_item(ListaSelect(listas))
        seleccion_lista_msg = await ctx.send("📂 Selecciona la lista:", view=lista_view)

        try:
            await asyncio.wait_for(lista_view.wait(), timeout=60)
        except asyncio.TimeoutError:
            await seleccion_lista_msg.delete()
            await ctx.send("⏳ Tiempo de selección expirado.", delete_after=5)
            return

        if not hasattr(lista_view, 'lista_seleccionada'):
            await seleccion_lista_msg.delete()
            await ctx.send("⏳ No se seleccionó ninguna lista.", delete_after=5)
            return

        lista_seleccionada = lista_view.lista_seleccionada
        canciones_seleccionadas = cancion_view.canciones_seleccionadas

        with open(lista_seleccionada, "a") as f:
            for cancion in canciones_seleccionadas:
                f.write(os.path.basename(cancion) + "\n")
                song_queue.append(cancion)

        canciones_nombres = ", ".join([os.path.basename(c)[:-4] for c in canciones_seleccionadas])
        confirmacion_msg = await ctx.send(
            f"✅ **{canciones_nombres}** añadidas a **{os.path.basename(lista_seleccionada)[:-4]}** y a la cola."
        )

        # Borrar todos los mensajes relevantes después de 60 segundos si no se eliminan antes
        await asyncio.sleep(60)
        for msg in [seleccion_cancion_msg, seleccion_lista_msg, confirmacion_msg]:
            try:
                await msg.delete()
            except:
                pass 

def setup(bot):
    bot.add_cog(Agregar(bot))
