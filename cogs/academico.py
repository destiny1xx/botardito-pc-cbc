import discord
from discord.ext import commands
from discord import app_commands
from data.calendario import (SEMANAS, DIA_OFFSET, GRUPOS_DIA, ESPECIALES, CONTENIDO, RECOMENDACIONES, COL_DIA,)
from datetime import datetime, timedelta
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_fecha(semana: int, dia: str) -> str:
    lunes = datetime.strptime(SEMANAS[semana], "%d/%m/%Y")
    return (lunes + timedelta(days=DIA_OFFSET[dia])).strftime("%d/%m/%Y")

def get_dia(num: int) -> str:
    for dia, nums in GRUPOS_DIA.items():
        if num in nums:
            return dia
    return "Desconocido"

def build_temario(dia: str) -> list[tuple[str, str, str]]:
    col = COL_DIA[dia]
    temario = []
    for semana in range(1, 15):
        fecha = get_fecha(semana, dia)
        if semana in ESPECIALES:
            contenido = f"⚠️ {ESPECIALES[semana]}"
        else:
            contenido = CONTENIDO[semana][col]
        temario.append((f"Semana {semana}", fecha, contenido))
    return temario

def build_fechas_clave(dia: str) -> list[tuple[str, str]]:
    return [(ESPECIALES[sem], get_fecha(sem, dia)) for sem in ESPECIALES]


def _build_cursos() -> dict:
    cursos = {}
    for dia, nums in GRUPOS_DIA.items():
        temario = build_temario(dia)
        fechas_clave = build_fechas_clave(dia)
        for num in nums:
            key = f"curso-{num:02d}"
            cursos[key] = {
                "dia": dia,
                "canal": f"#curso-{num:02d}",
                "fechas": fechas_clave,
                "temario": temario,
                "faq": {
                    "¿Qué día tengo práctica?": f"Tu día de práctica es el **{dia}**.",
                    "¿Cuándo es el Parcial I?": f"El **{get_fecha(7, dia)}** (semana 7).",
                    "¿Cuándo es el Recuperatorio Parcial I?": f"El **{get_fecha(10, dia)}** (semana 10).",
                    "¿Cuándo es el Parcial II?": f"El **{get_fecha(12, dia)}** (semana 12).",
                    "¿Cuándo es el Recuperatorio Parcial II?": f"El **{get_fecha(14, dia)}** (semana 14).",
                    "¿Dónde consulto novedades?": f"En el canal #curso-{num:02d} del servidor.",
                },
            }
    return cursos

CURSOS = _build_cursos()

def ahora_argentina() -> datetime:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).replace(tzinfo=None)
    return datetime.today()

def get_semana_actual(data: dict) -> int | None:
    hoy = ahora_argentina()
    for label, fecha_str, _ in data["temario"]:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
        dias = (fecha - hoy).days
        if -6 <= dias <= 0:
            return int(label.split()[1])
        if dias > 0:
            return int(label.split()[1])
    return None


def get_curso(member: discord.Member) -> tuple[str, dict] | tuple[None, None]:
    for role in member.roles:
        nombre = role.name.lower().strip().replace(" ", "-")
        if nombre in CURSOS:
            return nombre, CURSOS[nombre]
    return None, None


class Academico(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _sin_curso(self) -> discord.Embed:
        return discord.Embed(
            description="❌ No tengo tu curso asignado. Pedile a un admin que te dé el rol.",
            color=discord.Color.red()
        )
    
    @app_commands.command(name="ayuda", description="Muestra todos los comandos de Botardito")
    async def ayuda(self, interaction: discord.Interaction):
        embed = discord.Embed(
        title="🤖 Ayuda de Botardito",
        description="Comandos útiles para Pensamiento Computacional del CBC.",
        color=discord.Color.blurple()
        )
        embed.add_field(
            name="📚 Organización",
            value=(
            "`/fechas` — fechas clave de tu curso\n"
            "`/temario` — cronograma semana por semana\n"
            "`/repasar` — qué conviene estudiar ahora\n"
            "`/recursos` — canal y recursos de tu curso\n"
            "`/faq` — preguntas frecuentes"),  inline=False
            )
        embed.add_field(
            name="🧠 Práctica",
            value=(
                "`/quiz` — una pregunta rápida en el canal\n"
                "`/parcial` — mini parcial individual de 10 preguntas"),
                inline=False
                )
        embed.add_field(
            name="💬 Consultas",
            value=(
                "`/preguntarle` — preguntarle algo a Botardito\n"
                "También podés mencionar al bot con `@Botardito` para seguir una conversación."
                ),
                inline=False
                )
        embed.add_field(
            name="🎮 Juegos",
            value=(
                "`/frase` — Botardito te tira una frase random\n"
                "`/dado ` — Tira un dado de N caras (por defecto 6)\n"
                "`/oraculo ` — Hacele una pregunta de sí o no a Botardito"
                ),
                inline=False
                )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1499173908547371111/1499205900047483052/botardito.png?ex=69f3f3cc&is=69f2a24c&hm=5d770e2a3f52897eecdd1e401ad9ba6a35e6cbcb879651187bd2b3ce5f4385a6&")
        embed.set_footer(text="Tip: si no te detecta el curso, pedile a un admin que te asigne el rol curso-XX.")

        await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name="repasar", description="Te dice qué conviene repasar según tu curso y la semana actual")
    async def repasar(self, interaction: discord.Interaction):
        nombre_curso, data = get_curso(interaction.user)
        if not data:
            await interaction.response.send_message(embed=self._sin_curso(), ephemeral=True)
            return
            
        semana_actual = get_semana_actual(data)
        if semana_actual is None:
            await interaction.response.send_message(
                "No pude detectar la semana actual del cronograma.",
                ephemeral=True
                )
            return
            
        temario_actual = data["temario"][semana_actual - 1]
        _, fecha_actual, contenido_actual = temario_actual
        proxima_semana = semana_actual + 1 if semana_actual < 14 else None
            
        embed = discord.Embed( 
            title=f"📌 Qué repasar — {nombre_curso.upper()}", 
            description=f"Día de práctica: **{data['dia']}**\nSemana detectada: **{semana_actual}**",
            color=discord.Color.green()
            )
        embed.add_field(
            name=f"Ahora / clase de esta semana ({fecha_actual})",
            value=contenido_actual,
            inline=False
            )

        if proxima_semana is not None:
            _, fecha_prox, contenido_prox = data["temario"][proxima_semana - 1]
            recomendacion = RECOMENDACIONES.get(
                proxima_semana,
                "Repasar lo visto en la clase anterior y practicar ejercicios."
                )
            
            embed.add_field(
                name=f"Para llegar bien a la próxima ({fecha_prox})",
                value=f"{contenido_prox}\n\n📚 **Recomendación:** {recomendacion}",
                inline=False
            )
        else:
            embed.add_field(
                name="Última etapa",
                value="Repaso general: volvé sobre los errores de quizzes y parciales de práctica.",
                inline=False
                )
                
        embed.add_field(
             name="Cómo practicar",
             value="Usá `/quiz` para preguntas rápidas o `/parcial` para simular 10 preguntas seguidas.",
             inline=False
             )
            
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1499173908547371111/1499205900047483052/botardito.png?ex=69f3f3cc&is=69f2a24c&hm=5d770e2a3f52897eecdd1e401ad9ba6a35e6cbcb879651187bd2b3ce5f4385a6&")
            
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name="fechas", description="Fechas clave de tu curso")
    async def fechas(self, interaction: discord.Interaction):
        nombre_curso, data = get_curso(interaction.user)
        if not data:
            await interaction.response.send_message(embed=self._sin_curso(), ephemeral=True)
            return

        embed = discord.Embed(
            title=f"📅 Fechas clave — {nombre_curso.upper()}",
            description=f"📆 Día de práctica: **{data['dia']}**",
            color=discord.Color.blue()
        )
        hoy = ahora_argentina()
        for nombre, fecha_str in data["fechas"]:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
            dias = (fecha - hoy).days
            if dias < 0:    estado = "✅ Ya pasó"
            elif dias == 0: estado = "⚠️ ¡ES HOY!"
            elif dias <= 7: estado = f"🔴 En {dias} días"
            else:           estado = f"🟡 En {dias} días"
            embed.add_field(name=nombre, value=f"{fecha_str} — {estado}", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name="temario", description="Cronograma semana a semana de tu curso")
    async def temario(self, interaction: discord.Interaction):
        nombre_curso, data = get_curso(interaction.user)
        if not data:
            await interaction.response.send_message(embed=self._sin_curso(), ephemeral=True)
            return

        embed = discord.Embed(
            title=f"📖 Temario — {nombre_curso.upper()}",
            description=f"Día de práctica: **{data['dia']}**",
            color=discord.Color.purple()
        )

        hoy = ahora_argentina()

        
        semana_actual = None
        for label, fecha_str, _ in data["temario"]:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
            dias = (fecha - hoy).days
            if -6 <= dias <= 0:
                semana_actual = int(label.split()[1])
                break
            elif dias > 0:
                semana_actual = int(label.split()[1])
                break

        for label, fecha_str, contenido in data["temario"]:
            num_semana = int(label.split()[1])
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
            dias = (fecha - hoy).days

            if dias < -6:
                continue

            es_actual = semana_actual == num_semana
            es_siguiente = semana_actual is not None and num_semana == semana_actual + 1

            prefix = "👉 " if es_actual else ""
            valor = contenido

            if es_actual and (semana_actual + 1) in RECOMENDACIONES:
                valor += f"\n\n📚 **Para la próxima clase:** {RECOMENDACIONES[semana_actual + 1]}"

            if es_siguiente and num_semana in RECOMENDACIONES:
                valor += f"\n\n📚 **Recomendación:** {RECOMENDACIONES[num_semana]}"

            embed.add_field(name=f"{prefix}{label} — {fecha_str}", value=valor, inline=False)

        embed.set_footer(text="👉 = semana actual")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1499173908547371111/1499205900047483052/botardito.png?ex=69f3f3cc&is=69f2a24c&hm=5d770e2a3f52897eecdd1e401ad9ba6a35e6cbcb879651187bd2b3ce5f4385a6&")
        await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name="faq", description="Preguntas frecuentes de tu curso")
    async def faq(self, interaction: discord.Interaction):
        nombre_curso, data = get_curso(interaction.user)
        if not data:
            await interaction.response.send_message(embed=self._sin_curso(), ephemeral=True)
            return

        embed = discord.Embed(
            title=f"❓ FAQ — {nombre_curso.upper()}",
            color=discord.Color.orange()
        )
        for pregunta, respuesta in data["faq"].items():
            embed.add_field(name=pregunta, value=respuesta, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name="recursos", description="Canal y recursos de tu curso")
    async def recursos(self, interaction: discord.Interaction):
        nombre_curso, data = get_curso(interaction.user)
        if not data:
            await interaction.response.send_message(embed=self._sin_curso(), ephemeral=True)
            return

        embed = discord.Embed(
            title=f"🔗 Recursos — {nombre_curso.upper()}",
            color=discord.Color.green()
        )
        embed.add_field(name="Canal del curso", value=data["canal"], inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Academico(bot))