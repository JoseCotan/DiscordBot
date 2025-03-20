import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

is_paused = False
song_queue = []
global_volume = 0.5
download_folder = "./canciones"
list_folder = "./listas"

class Config:
    def __init__(self):
        self.counter_song = -1
        self.is_playing_next = False
        self.current_player_message = None
        self.next_song_message = None
        self.extra_message = ""

# Instancia global
config = Config()

