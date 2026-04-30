import discord
from discord.ext import commands
from discord import app_commands

import random
import json
import os


EMOJIS_OPCIONES = ["🇦", "🇧", "🇨", "🇩"]

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, "data", "preguntas.json"), encoding="utf-8") as f:
    PREGUNTAS = json.load(f)


class QuizView(discord.ui.View):
    def __init__(self, pregunta: dict, user_id: int):
        super().__init__(timeout=120)
        self.pregunta = pregunta
        self.user_id = user_id
        self.respondido = False
        self._crear_botones()

    def _crear_botones(self):
        for indice, _ in enumerate(self.pregunta["opciones"]):
            boton = discord.ui.Button(
                label=chr(65 + indice),
                emoji=EMOJIS_OPCIONES[indice],
                style=discord.ButtonStyle.primary,
                custom_id=f"quiz_opcion_{indice}",
            )

            boton.callback = self._crear_callback(indice)
            self.add_item(boton)

    def _crear_callback(self, indice_opcion: int):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message(
                    "⚠️ Este quiz no es tuyo. Usá `/quiz` para empezar uno propio.",
                    ephemeral=True,
                )
                return

            if self.respondido:
                await interaction.response.send_message(
                    "⚠️ Ya respondiste este quiz.",
                    ephemeral=True,
                )
                return

            self.respondido = True

            correcta = self.pregunta["correcta"]
            es_correcta = indice_opcion == correcta

            for item in self.children:
                item.disabled = True

            if es_correcta:
                color = discord.Color.green()
                resultado = "✅ **Correcto.** Muy bien."
            else:
                color = discord.Color.red()
                resultado = (
                    f"❌ **Incorrecto.**\n"
                    f"La respuesta correcta era **{chr(65 + correcta)}**."
                )

            explicacion = self.pregunta.get("explicacion")

            embed = discord.Embed(
                title="🧠 Resultado del quiz",
                description=resultado,
                color=color,
            )

            embed.add_field(
                name="Pregunta",
                value=self.pregunta["pregunta"],
                inline=False,
            )

            embed.add_field(
                name="Tu respuesta",
                value=f"{chr(65 + indice_opcion)}. {self.pregunta['opciones'][indice_opcion]}",
                inline=False,
            )

            embed.add_field(
                name="Respuesta correcta",
                value=f"{chr(65 + correcta)}. {self.pregunta['opciones'][correcta]}",
                inline=False,
            )

            if explicacion:
                embed.add_field(
                    name="Explicación",
                    value=explicacion,
                    inline=False,
                )

            embed.set_footer(text="Usá /quiz para practicar otra pregunta.")

            await interaction.response.edit_message(
                embed=embed,
                view=self,
            )

            self.stop()

        return callback

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="quiz",
        description="Botardito te tira una pregunta rápida de práctica"
    )
    async def quiz(self, interaction: discord.Interaction):
        pregunta = random.choice(PREGUNTAS)

        opciones_texto = "\n".join(
            f"{EMOJIS_OPCIONES[i]} **{chr(65 + i)}.** {opcion}"
            for i, opcion in enumerate(pregunta["opciones"])
        )

        embed = discord.Embed(
            title="🧠 Quiz de Pensamiento Computacional",
            description=f"**{pregunta['pregunta']}**\n\n{opciones_texto}",
            color=discord.Color.purple(),
        )

        embed.set_footer(text="Respondé con los botones. Solo vos podés ver este quiz.")

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1499173908547371111/1499205900047483052/botardito.png?ex=69f3f3cc&is=69f2a24c&hm=5d770e2a3f52897eecdd1e401ad9ba6a35e6cbcb879651187bd2b3ce5f4385a6&"
        )

        view = QuizView(
            pregunta=pregunta,
            user_id=interaction.user.id,
        )

        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(Quiz(bot))
