import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import aiohttp
import os

SYSTEM_PROMPT = """Sos Botardito, un asistente pensado para acompañar el estudio en Pensamiento Computacional del CBC (UBA).

Tu forma de responder ante ejercicios o problemas:
- NO RESPONDES si la pregunta no tiene nada que ver con la materia
- NUNCA das la solución directamente
- Guiás al estudiante con preguntas que lo llevan a pensar: "¿qué harías primero?", "¿qué devuelve esta operación?", etc.
- Podés dar una pista conceptual pero sin escribir el código
- Si el estudiante ya intentó algo, analizás su razonamiento y lo orientás desde ahí
- Terminás siempre con una pregunta que lo invite a seguir pensando

Tu forma de responder ante dudas teóricas o conceptuales:
- Explicás de forma clara y directa, con ejemplos simples si hace falta
- Podés mostrar código solo si es para ilustrar un concepto, nunca para resolver un ejercicio

Reglas generales:
- Usás vocabulario rioplatense (vos, dale, re, etc.)
- Tus respuestas son concisas, máximo 5-6 oraciones
- Si la pregunta es muy amplia o compleja, recomendás consultar a lxs docentes
- Si no sabés algo, lo decís con honestidad sin inventar"""

MAX_HISTORIAL = 10


class Preguntas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.historial: dict[int, list] = {}

    def _get_historial(self, user_id: int) -> list:
        return self.historial.get(user_id, [])

    def _agregar_mensaje(self, user_id: int, role: str, content: str):
        if user_id not in self.historial:
            self.historial[user_id] = []
        self.historial[user_id].append({"role": role, "content": content})

        if len(self.historial[user_id]) > MAX_HISTORIAL:
            self.historial[user_id] = self.historial[user_id][-MAX_HISTORIAL:]

    def _limpiar_historial(self, user_id: int):
        self.historial.pop(user_id, None)

    async def _consultar_groq(self, user_id: int, pregunta: str) -> str:
        groq_key = os.getenv("GROQ_API_KEY")

        if not groq_key:
            "❌ Falta configurar la API key de Groq. Revisá el archivo `.env`."

        self._agregar_mensaje(user_id, "user", pregunta)

        try:
            timeout = aiohttp.ClientTimeout(total=20)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {groq_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "max_tokens": 300,
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            *self._get_historial(user_id),
                            ],
                        },
                    ) as resp:
                    data = await resp.json()
                    if resp.status != 200:
                        print(f"Error Groq {resp.status}: {data}")

                        if resp.status == 401:
                            return "❌ La API key de Groq no es válida o no está autorizada."

                        if resp.status == 429:
                            return "⏳ Botardito recibió muchas consultas seguidas. Probá de nuevo en unos segundos."

                        return "❌ No pude conectarme bien con Groq. Probá de nuevo más tarde."
                    
            respuesta = data["choices"][0]["message"]["content"]
            self._agregar_mensaje(user_id, "assistant", respuesta)
            return respuesta

        except aiohttp.ClientError as error:
            print(f"Error de conexión con Groq: {error}")
            return "❌ Hubo un problema de conexión. Probá de nuevo en unos segundos."
        
        except KeyError as error:
            print(f"Respuesta inesperada de Groq: {error}")
            return "❌ Groq respondió con un formato inesperado. Probá de nuevo."

        except asyncio.TimeoutError:
            return "⏳ La consulta tardó demasiado. Probá de nuevo con una pregunta más corta."

        except Exception as error:
            print(f"Error inesperado en _consultar_groq: {error}")
            return "❌ Ocurrió un error inesperado. Probá de nuevo más tarde."


    @app_commands.command(name="preguntarle", description="Hacele una pregunta a Botardito")
    @app_commands.describe(pregunta="Tu pregunta para Botardito")
    async def preguntarle(self, interaction: discord.Interaction, pregunta: str):
        await interaction.response.defer(ephemeral=True)

        if not os.getenv("GROQ_API_KEY"):
            await interaction.followup.send("⚠️ No tengo la API key configurada.", ephemeral=True)
            return

        try:
            self._limpiar_historial(interaction.user.id)
            respuesta = await self._consultar_groq(interaction.user.id, pregunta)

            embed = discord.Embed(
                description=f"**{interaction.user.display_name} preguntó:**\n\n🤖 {respuesta}",
                color=discord.Color.blurple()
            )
            embed.set_author(name="Botardito responde")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1499173908547371111/1499205900047483052/botardito.png?ex=69f3f3cc&is=69f2a24c&hm=5d770e2a3f52897eecdd1e401ad9ba6a35e6cbcb879651187bd2b3ce5f4385a6&")
            embed.set_footer(text="Podés seguir la conversación mencionando @Botardito, sino para seguir en privado, usá /preguntarle")
            await interaction.followup.send(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.followup.send("💥 Ups, algo salió mal. Intentá de nuevo más tarde.", ephemeral=True)
            print(f"Error en /preguntarle: {e}")


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        
        if self.bot.user not in message.mentions:
            return
        
        if message.attachments:
            tiene_imagen = any(
                a.content_type and a.content_type.startswith("image/")
                for a in message.attachments
                )
            if tiene_imagen:
                await message.reply(
                    "🖼️ Todavía no puedo analizar imágenes, ¡pero estamos trabajando en eso!\n"
                    "Por ahora podés describir tu código o el error en texto.\n\n"
                    "Si necesitás ayuda visual, probá el Botardito original acá: "
                    "https://chatgpt.com/g/g-69862f8e9da481919f27fcb35cc06b4a-botardito"
                    )
                return

        pregunta = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
        if not pregunta:
            await message.reply("¿Me preguntabas algo? Escribí tu duda después de mencionarme.")
            return

        if not os.getenv("GROQ_API_KEY"):
            await message.reply("⚠️ No tengo la API key configurada.")
            return

        async with message.channel.typing():
            try:
                respuesta = await self._consultar_groq(message.author.id, pregunta)
                embed = discord.Embed(
                    description=f"🤖 {respuesta}",
                    color=discord.Color.blurple()
                )
                embed.set_author(name="Botardito responde")
                embed.set_footer(text="Para preguntar en privado, usá /preguntarle")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1499173908547371111/1499205900047483052/botardito.png?ex=69f3f3cc&is=69f2a24c&hm=5d770e2a3f52897eecdd1e401ad9ba6a35e6cbcb879651187bd2b3ce5f4385a6&")
                await message.reply(embed=embed)

            except Exception as e:
                await message.reply("💥 Ups, algo salió mal. Intentá de nuevo más tarde.")
                print(f"Error en mención: {e}")


async def setup(bot):
    await bot.add_cog(Preguntas(bot))