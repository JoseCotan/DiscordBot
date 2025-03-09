import nextcord
from nextcord.ext import commands

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="vanessa")
    async def vanessa(self, ctx):
        kepikete_id = 659384159629737995
        kepikete_mention = f"<@{kepikete_id}>"
    
        image_path = "nami.jpg"
        try:
            with open(image_path, "rb") as file:
                picture = nextcord.File(file, filename="nami.jpg")
                await ctx.send(f"{kepikete_mention}, La Nami más chula!", file=picture)
        except FileNotFoundError:
            await ctx.send(f"{kepikete_mention}, ⚠️ No encontré la imagen `nami.jpg` en la carpeta raíz.")

    @commands.command(name="pengu")
    async def pengu(self, ctx):
        pengu_id = 140254092634226689
        pengu_mention = f"<@{pengu_id}>"
    
        image_path = "pengu.jpg"
        try:
            with open(image_path, "rb") as file:
                picture = nextcord.File(file, filename="pengu.jpg")
                await ctx.send(f"{pengu_mention}, PENGU PENGU PENGU!", file=picture)
        except FileNotFoundError:
            await ctx.send(f"{pengu_mention}, ⚠️ No encontré la imagen `pengu.jpg` en la carpeta raíz.")

# Función para registrar el cog
def setup(bot):
    bot.add_cog(Cog(bot))