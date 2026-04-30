import discord
from discord.ext import commands
from discord import app_commands
import random


FRASES = [
    "El que no entiende la recursión está condenado a no entenderla... a no entenderla...",
    "Un loop infinito no es un error, es un estilo de vida.",
    "Antes de pedir ayuda en el canal, googlealo. Te lo digo con amor.",
    "El mejor comentario en el código es el que no necesita existir.",
    "Si funciona, no lo toques. Si no funciona, tampoco.",
    "Compilar sin errores no significa que el programa esté bien.",
    "La única diferencia entre un bug y una feature es la documentación.",
]

RESPUESTAS_SI_NO = ["Sí, definitivamente.", "No, para nada.", "Tal vez... depende.", 
                     "El oráculo dice que sí.", "El oráculo dice que no.", "Preguntame de nuevo más tarde.",
                     "Las señales no son claras.", "Todo indica que sí.", "Todo indica que no."]


class Botardito(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="frase", description="Botardito te tira una frase random")
    async def frase(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"💬 {random.choice(FRASES)}", ephemeral=True)


    @app_commands.command(name="dado", description="Tira un dado de N caras (por defecto 6)")
    @app_commands.describe(caras="Número de caras del dado (mínimo 2)")
    async def dado(self, interaction: discord.Interaction, caras: int = 6):
        if caras < 2:
            await interaction.response.send_message("❌ El dado necesita al menos 2 caras.", ephemeral=True)
            return
        resultado = random.randint(1, caras)
        await interaction.response.send_message(f"🎲 Dado de {caras} caras → **{resultado}**")


    @app_commands.command(name="oraculo", description="Hacele una pregunta de sí o no a Botardito")
    @app_commands.describe(pregunta="Tu pregunta")
    async def oraculo(self, interaction: discord.Interaction, pregunta: str):
        await interaction.response.send_message(
            f"🔮 **{interaction.user.display_name} pregunta:** {pregunta}\n"
            f"➤ {random.choice(RESPUESTAS_SI_NO)}"
        )


async def setup(bot):
    await bot.add_cog(Botardito(bot))
