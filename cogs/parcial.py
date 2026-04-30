import json
import random
import os

import discord
from discord.ext import commands
from discord import app_commands


EMOJIS_OPCIONES = ["🇦", "🇧", "🇨", "🇩"]

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

with open(
    os.path.join(BASE_DIR, "data", "preguntas_parciales.json"),
    encoding="utf-8"
) as f:
    PREGUNTAS = json.load(f)


class ParcialView(discord.ui.View):
    def __init__(self, preguntas: list[dict], user_id: int, tipo: str):
        super().__init__(timeout=300)
        self.preguntas = preguntas
        self.user_id = user_id
        self.tipo = tipo
        self.indice_actual = 0
        self.correctas = 0
        self.respuestas: list[tuple[dict, int, bool]] = []
        self._actualizar_botones()

    def _pregunta_actual(self) -> dict:
        return self.preguntas[self.indice_actual]

    def _actualizar_botones(self):
        self.clear_items()
        pregunta = self._pregunta_actual()

        for indice, _ in enumerate(pregunta["opciones"]):
            boton = discord.ui.Button(
                label=chr(65 + indice),
                emoji=EMOJIS_OPCIONES[indice],
                style=discord.ButtonStyle.primary,
                custom_id=f"parcial_opcion_{indice}",
            )
            boton.callback = self._crear_callback(indice)
            self.add_item(boton)

    def _crear_callback(self, indice_opcion: int):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message(
                    "⚠️ Este parcial no es tuyo. Usá `/parcial` para empezar uno propio.",
                    ephemeral=True,
                )
                return

            pregunta = self._pregunta_actual()
            es_correcta = indice_opcion == pregunta["correcta"]

            if es_correcta:
                self.correctas += 1

            self.respuestas.append((pregunta, indice_opcion, es_correcta))
            self.indice_actual += 1

            if self.indice_actual >= len(self.preguntas):
                await interaction.response.edit_message(
                    embed=self._embed_resultado(),
                    view=None,
                )
                self.stop()
                return

            self._actualizar_botones()

            await interaction.response.edit_message(
                embed=self._embed_pregunta(),
                view=self,
            )

        return callback

    def _embed_pregunta(self) -> discord.Embed:
        pregunta = self._pregunta_actual()

        opciones = "\n".join(
            f"{EMOJIS_OPCIONES[i]} **{chr(65 + i)}.** {opcion}"
            for i, opcion in enumerate(pregunta["opciones"])
        )

        tipo_legible = (
            "Primer parcial"
            if self.tipo == "primer_parcial"
            else "Segundo parcial"
        )

        embed = discord.Embed(
            title=f"📝 {tipo_legible} — Pregunta {self.indice_actual + 1}/{len(self.preguntas)}",
            description=f"**{pregunta['pregunta']}**\n\n{opciones}",
            color=discord.Color.blurple(),
        )

        embed.add_field(
            name="Tema",
            value=pregunta.get("tema", "Sin tema"),
            inline=True,
        )

        embed.add_field(
            name="Dificultad",
            value=pregunta.get("dificultad", "normal"),
            inline=True,
        )

        embed.set_footer(
            text="Respondé con los botones. Tenés 5 minutos antes de que se cierre."
        )

        return embed

    def _embed_resultado(self) -> discord.Embed:
        total = len(self.preguntas)
        nota = round((self.correctas / total) * 10, 2)

        if nota >= 8:
            estado = "🔥 Muy bien. Estás para ir confiado."
            color = discord.Color.green()
        elif nota >= 6:
            estado = "🟡 Bien, pero todavía hay errores para corregir."
            color = discord.Color.gold()
        else:
            estado = "🔴 Hay que repasar más. No estás sólido todavía."
            color = discord.Color.red()

        tipo_legible = (
            "Primer parcial"
            if self.tipo == "primer_parcial"
            else "Segundo parcial"
        )

        embed = discord.Embed(
            title=f"📊 Resultado — {tipo_legible}",
            description=(
                f"Correctas: **{self.correctas}/{total}**\n"
                f"Nota estimada: **{nota}/10**\n\n"
                f"{estado}"
            ),
            color=color,
        )

        resumen = []
        errores_por_tema = {}

        for numero, (pregunta, elegida, correcta) in enumerate(self.respuestas, start=1):
            correcta_idx = pregunta["correcta"]
            marca = "✅" if correcta else "❌"
            tema = pregunta.get("tema", "sin tema")

            if not correcta:
                errores_por_tema[tema] = errores_por_tema.get(tema, 0) + 1

            linea = (
                f"{marca} **{numero}.** Tema: `{tema}` | "
                f"Tu respuesta: **{chr(65 + elegida)}** | "
                f"Correcta: **{chr(65 + correcta_idx)}**"
            )

            if not correcta:
                explicacion = pregunta.get(
                    "explicacion",
                    "Sin explicación cargada."
                )
                linea += f"\n└ 💡 {explicacion}"

            resumen.append(linea)

        detalle = "\n\n".join(resumen[:10])

        if len(detalle) > 1024:
            detalle = detalle[:1000] + "\n\n..."

        embed.add_field(
            name="Detalle",
            value=detalle,
            inline=False,
        )

        if errores_por_tema:
            temas_a_repasar = "\n".join(
                f"- **{tema}**: {cantidad} error(es)"
                for tema, cantidad in errores_por_tema.items()
            )

            embed.add_field(
                name="📚 Temas a repasar",
                value=temas_a_repasar,
                inline=False,
            )
        else:
            embed.add_field(
                name="📚 Temas a repasar",
                value="Ninguno fuerte. Metiste todo bien.",
                inline=False,
            )

        embed.set_footer(
            text="Tip: usá /repasar para ver qué conviene estudiar según el cronograma."
        )

        return embed

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


class Parcial(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="parcial",
        description="Simula un parcial de práctica de Pensamiento Computacional",
    )
    @app_commands.describe(
        tipo="Elegí si querés practicar primer parcial o segundo parcial",
        cantidad="Cantidad de preguntas. Recomendado: 10",
    )
    @app_commands.choices(
        tipo=[
            app_commands.Choice(name="Primer parcial", value="primer_parcial"),
            app_commands.Choice(name="Segundo parcial", value="segundo_parcial"),
        ]
    )
    async def parcial(
        self,
        interaction: discord.Interaction,
        tipo: app_commands.Choice[str],
        cantidad: app_commands.Range[int, 5, 20] = 10,
    ):
        preguntas_filtradas = [
            pregunta
            for pregunta in PREGUNTAS
            if pregunta["parcial"] == tipo.value
        ]

        if len(preguntas_filtradas) < cantidad:
            await interaction.response.send_message(
                (
                    f"❌ No hay suficientes preguntas cargadas para "
                    f"**{tipo.name}**.\n"
                    f"Hay **{len(preguntas_filtradas)}** disponibles y pediste **{cantidad}**."
                ),
                ephemeral=True,
            )
            return

        preguntas = random.sample(preguntas_filtradas, cantidad)

        view = ParcialView(
            preguntas=preguntas,
            user_id=interaction.user.id,
            tipo=tipo.value,
        )

        await interaction.response.send_message(
            embed=view._embed_pregunta(),
            view=view,
            ephemeral=True,
        )


async def setup(bot):
    await bot.add_cog(Parcial(bot))