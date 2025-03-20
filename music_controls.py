import nextcord
import os
import asyncio
import yt_dlp
import random
from commands.stop import stop
from commands.skip import skip
from commands.queue import queue
from commands.put_song import *
from commands.put_song_local import *
from bot_config import *
        
class MusicControls(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None) 
        self.ctx = ctx
        self.voice_client = ctx.voice_client
        self.volume = global_volume
        self.is_paused = False
        self.is_muted = False
        self.repeat = False
        self.current_song = None 
        self.back_song = False
        self.random_song = False

        self.update_volume_button_styles()
        if self.voice_client and self.voice_client.source:
            self.voice_client.source = nextcord.PCMVolumeTransformer(self.voice_client.source, volume=self.volume)
            
    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        allowed_role_name = "DJ"
        if any(role.name == allowed_role_name for role in interaction.user.roles):
            return True
        else:
            await interaction.response.send_message(
                f"🚫 No tienes permiso para usar el reproductor. Se requiere el rol **{allowed_role_name}**.",
                ephemeral=True
            )
            return False

    @nextcord.ui.button(label="🔀", style=nextcord.ButtonStyle.secondary, row=0)
    async def random(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.repeat:
                await interaction.response.send_message("⚠️ Desactiva antes la repetición, que me bugueas.", ephemeral=True)
        elif self.voice_client:
            # Cambiar el estado de la canción aleatoria
            self.random_song = not self.random_song
            
            # Actualizar el estilo del botón correspondiente
            for item in self.children:
                if isinstance(item, nextcord.ui.Button) and item.label == "🔀":
                    item.style = nextcord.ButtonStyle.green if self.random_song else nextcord.ButtonStyle.secondary

            # Responder al usuario
            await interaction.response.edit_message(view=self)
            if self.random_song:
                await update_extra_message(self.ctx, "🎶 Modo aleatorio activado.")
            else:
                await update_extra_message(self.ctx, "🎶 Modo aleatorio desactivado.")
        else:
            await update_extra_message(self.ctx, "🎶 No hay canciones en la cola.")


    @nextcord.ui.button(emoji="<:atras:1343686478835879956>", style=nextcord.ButtonStyle.primary, row=0)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.voice_client and config.counter_song > 0 and (self.voice_client.is_playing() or self.voice_client.is_paused()):
            self.back_song = True  # Señal para retroceder en play_next
            await update_extra_message(self.ctx, "⏮️ Reproduciendo la canción anterior...")
            self.voice_client.stop()  # Detiene la canción actual y dispara el after_playing para llamar a play_next
            if not interaction.response.is_done():
                await interaction.response.defer()
        else:
            await update_extra_message(self.ctx, "⚠️ No hay canción anterior para reproducir.")

    @nextcord.ui.button(emoji="<:pausa:1343632142327877765>", style=nextcord.ButtonStyle.green, row=0)
    async def pause_resume(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            self.is_paused = True
            button.emoji = "<:reanudar:1343636106784280677>"  # Cambia el emoji a reanudar
            await interaction.response.edit_message(view=self)  # Actualiza el botón en el mensaje
            await update_extra_message(self.ctx, "🎶 Canción pausada.")
        elif self.voice_client and self.is_paused:
            self.voice_client.resume()
            self.is_paused = False
            button.emoji = "<:pausa:1343632142327877765>"  # Cambia el emoji a pausa
            await interaction.response.edit_message(view=self)  # Actualiza el botón en el mensaje
            await update_extra_message(self.ctx, "🎶 Canción reanudada.")
        else:
            await update_extra_message(self.ctx, "⚠️ No hay ninguna canción reproduciéndose.")

    @nextcord.ui.button(emoji="<:adelante:1343686462964760660>", style=nextcord.ButtonStyle.primary, row=0)
    async def skipp(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if self.voice_client:
            await update_extra_message(self.ctx, "⏭️ Saltando canción...")
            await skip(self.ctx)  # Esto activará el after de play(), llamando a play_next(ctx)
        else:
            await update_extra_message(self.ctx, "⚠️ No hay ninguna canción reproduciéndose.")

    @nextcord.ui.button(label="⏹", style=nextcord.ButtonStyle.secondary, row=0)
    async def stop_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        config.counter_song = -1
        if self.ctx.voice_client:
            await stop(self.ctx)
            
        button.style = nextcord.ButtonStyle.danger

        song_queue.clear()
        await update_extra_message(self.ctx, "🎶 Reproducción detenida y cola vaciada.")

    @nextcord.ui.button(label="🔁", style=nextcord.ButtonStyle.secondary, row=1)
    async def repeat_toggle(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.random_song:
            await interaction.response.send_message("⚠️ Desactiva antes la música aleatoria, que me bugueas.", ephemeral=True)
        else:
            self.repeat = not self.repeat
            button.style = nextcord.ButtonStyle.green if self.repeat else nextcord.ButtonStyle.secondary
            await interaction.response.edit_message(view=self)
            estado = "🔁 Modo repetición activado." if self.repeat else "🔁 Modo repetición desactivado."
            await update_extra_message(self.ctx, estado)

    def update_volume_button_styles(self):
        # Actualiza los estilos de los botones de volumen basados en el volumen actual.
        for item in self.children:
            if isinstance(item, nextcord.ui.Button):
                if item.label == "🔇":
                    # Cambiar a rojo si el volumen es 0 (silenciado)
                    item.style = nextcord.ButtonStyle.danger if self.volume == 0 else nextcord.ButtonStyle.secondary

                # Verificación para evitar AttributeError si item.label es None
                if item.label and item.label[0].isdigit():
                    item.label = f"{int(self.volume * 100)}"

    @nextcord.ui.button(label="🔉", style=nextcord.ButtonStyle.green, row=1)
    async def volume_down(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        global global_volume
        if self.voice_client:
            if self.volume > 0.0:
                self.volume = max(self.volume - 0.1, 0.0)
                global_volume = self.volume
                self.voice_client.source.volume = self.volume
                self.update_volume_button_styles()  # Actualiza los estilos de ambos botones
                await interaction.response.edit_message(view=self)
            else:
                await update_extra_message(self.ctx, "🔇 El volumen ya está en silencio.")
        else:
            await update_extra_message(self.ctx, "🔇 El volumen ya está en silencio.")

    @nextcord.ui.button(label="50", style=nextcord.ButtonStyle.primary, row=1)
    async def volume_display(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    # Botón solo informativo (no hace nada al pulsarlo)
        pass


    @nextcord.ui.button(label="🔊", style=nextcord.ButtonStyle.green, row=1)
    async def volume_up(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        global global_volume
        if self.voice_client:
            if self.volume < 1.0:
                self.volume = min(self.volume + 0.1, 1.0)
                global_volume = self.volume
                self.voice_client.source.volume = self.volume
                self.update_volume_button_styles()  # Actualiza los estilos de ambos botones
                await interaction.response.edit_message(view=self)
            else:
                await interaction.response.defer()
                await update_extra_message(self.ctx, "🎧 El volumen ya está al máximo.")
        else:
            await update_extra_message(self.ctx, "⚠️ No hay música reproduciéndose.")


    @nextcord.ui.button(label="🔇", style=nextcord.ButtonStyle.secondary, row=1)
    async def mute(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        global global_volume
        if self.voice_client:
            if self.is_muted:
                # Desmutear
                self.is_muted = False
                self.voice_client.source.volume = global_volume
                self.volume = global_volume
                await interaction.response.defer()  # Aplaza la respuesta
                await update_extra_message(self.ctx, "🔊 Música desmutada.")
            else:
                # Mutear
                self.is_muted = True
                self.volume = 0  # Establecer volumen a 0
                self.voice_client.source.volume = self.volume
                await interaction.response.defer()  # Aplaza la respuesta
                await update_extra_message(self.ctx, "🔇 Música silenciada.")
            
            # Actualiza los botones después de mutear/desmutear
            self.update_volume_button_styles()
            # Usar interaction.message para editar el mensaje
            await interaction.message.edit(view=self)  # Edita el mensaje con los botones actualizados
        else:
            await update_extra_message(self.ctx, "⚠️ No hay música reproduciéndose.")

    @nextcord.ui.button(label="📝 Cola", style=nextcord.ButtonStyle.primary, row=2)
    async def cola_button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await queue(self.ctx)
        
    @nextcord.ui.button(label="Canción por YT", style=nextcord.ButtonStyle.primary, row=2)
    async def poner_cancion(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = PlayModal(self.ctx)
        await interaction.response.send_modal(modal)
        
    @nextcord.ui.button(label="Canción por local", style=nextcord.ButtonStyle.primary, row=2)
    async def poner_cancion_local(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        modal = PlayModalLocal()
        await interaction.response.send_modal(modal)


async def play_next(ctx, controls: MusicControls = None):
    print(config.counter_song)

    if config.is_playing_next:
        return
    config.is_playing_next = True

    # Verifica si controls es None y crea uno nuevo si es necesario
    if not controls:
        controls = MusicControls(ctx)

    voice_client = ctx.voice_client
    if not voice_client:
        return
    
    if not song_queue:
        await check_disconnect(ctx)
        return

    if controls.back_song:
        if config.counter_song > 0:
            config.counter_song -= 1
        else:
            return
        controls.back_song = False
    elif controls.random_song:
        config.counter_song = random.randint(0, len(song_queue) - 1)
    else:
        if controls.repeat:
            print("hola")
        elif config.counter_song < len(song_queue) - 1:
            config.counter_song += 1
        else:
            await ctx.send("🎶 Has llegado al final de la cola.")
            config.is_playing_next = False
            return

    next_song = song_queue[config.counter_song]
    controls.current_song = next_song

    # Si la canción existe en el sistema de archivos, se usa localmente
    print(next_song)
    if os.path.exists(next_song):
        audio_file = next_song
    else:
        # Si no es una URL, tratamos de buscarla en YouTube con ytsearch
        search_query = f"ytsearch:{next_song},"  # Usamos ytsearch para buscar en YouTube

        with yt_dlp.YoutubeDL({'quiet': True, 'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s')}) as ydl:
            try:
                # Buscamos la canción
                video_info = ydl.extract_info(search_query, download=False)
                safe_title = "".join(c for c in video_info['entries'][0]['title'] if c.isalnum() or c in " -_").rstrip()
                audio_file = os.path.join(download_folder, f"{safe_title}.mp3")

                if not os.path.exists(audio_file):  # Si no existe el archivo, lo descargamos
                    ydl.download([search_query])

            except Exception as e:
                await ctx.send(f"🚫 Error al intentar buscar la canción: {str(e)}")
                return

    def after_playing(_):
        config.is_playing_next = False
        asyncio.run_coroutine_threadsafe(play_next(ctx, controls), bot.loop)

    try:
        if voice_client.is_playing():
            voice_client.stop()
            await asyncio.sleep(1)

        voice_client.play(
            nextcord.FFmpegPCMAudio(audio_file), after=after_playing
        )
        
        voice_client.source = nextcord.PCMVolumeTransformer(voice_client.source, volume=controls.volume)

        if config.current_player_message is None:
            config.current_player_message = await ctx.send(
                f"🎶 Reproduciendo: `{os.path.basename(audio_file[:-4])}`", view=controls
            )

            if song_queue and config.counter_song + 1 < len(song_queue):
                siguiente_texto = "🎶 Siguiente canción: `Aleatorio`" if controls.random_song else f"🎶 Siguiente canción: `{os.path.basename(song_queue[config.counter_song + 1])[:-4]}`"
                config.next_song_message = await ctx.send(siguiente_texto)

        else:
            await config.current_player_message.edit(
                content=f"🎶 Reproduciendo: `{os.path.basename(audio_file[:-4])}`", view=controls
            )

            if song_queue and config.counter_song + 1 < len(song_queue):
                siguiente_texto = "🎶 Siguiente canción: `Aleatorio`" if controls.random_song else f"🎶 Siguiente canción: `{os.path.basename(song_queue[config.counter_song + 1])[:-4]}`"
                await config.next_song_message.edit(content=siguiente_texto)
                
        if config.extra_message == "":
            await update_extra_message(ctx)

    except Exception as e:
        if song_queue:
            await play_next(ctx, controls)

 
# Crear botones para controlar la música
async def create_controls(ctx):
    button_play_pause = nextcord.ui.Button(label="Pausar", style=nextcord.ButtonStyle.primary)
    button_skip = nextcord.ui.Button(label="Saltar", style=nextcord.ButtonStyle.danger)
    
    # Añadir interacción a los botones
    async def play_pause_callback(interaction):
        global is_paused
        voice_client = ctx.voice_client
        if is_paused:
            voice_client.resume()
            is_paused = False
        else:
            voice_client.pause()
            is_paused = True
        await interaction.message.edit(view=view)

    async def skip_callback(interaction):
        await ctx.invoke(stop)  # Detener la canción actual
        await play_next(ctx)  # Reproducir la siguiente canción
        await interaction.message.edit(view=view)

    # Asignar callbacks
    button_play_pause.callback = play_pause_callback
    button_skip.callback = skip_callback

    view = nextcord.ui.View()
    view.add_item(button_play_pause)
    view.add_item(button_skip)

    # Enviar un mensaje con los controles
    await ctx.send("Controles de música:", view=view)


async def update_extra_message(ctx, content=config.extra_message):
    pantalla_text = (
        "🖥️ **Pantalla de estado**\n"
        "╔═════════════════════════════════════════╗\n"
        f"          `{content.center(50)}`\n"
        "╚═════════════════════════════════════════╝"
    )

    try:
        if config.extra_message and config.extra_message.channel:
            await config.extra_message.edit(content=pantalla_text)
        else:
            config.extra_message = await ctx.send(pantalla_text)
    except nextcord.NotFound:
        config.extra_message = await ctx.send(pantalla_text)
    except Exception as e:
        print(f"[Error al actualizar pantalla extra]: {e}")
        config.extra_message = await ctx.send(pantalla_text)

async def check_disconnect(ctx):
    """Espera unos segundos y desconecta si no hay música."""
    await asyncio.sleep(300)  # Espera 300 segundos
    if ctx.voice_client and not ctx.voice_client.is_playing():
        await ctx.voice_client.disconnect()
        await ctx.send("🔌 Me las piro por inactividad.")
    