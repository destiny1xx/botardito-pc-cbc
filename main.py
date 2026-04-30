import os
import discord
import random
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

ESTADOS = [
    "📚 Repasando Pensamiento Computacional",
    "🐍 Practicando Python",
    "🧠 Preparando simulacros de parcial",
    "💬 Usá /preguntarle para consultar dudas",
    "🎯 Usá /quiz para practicar",
    "🤖 Botardito activo para el CBC",
]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if not filename.endswith(".py"):
            continue

        if filename.startswith("_"):
            continue

        extension = f"cogs.{filename[:-3]}"

        if extension in bot.extensions:
            continue

        try:
            await bot.load_extension(extension)
            print(f"✓ Cog cargado: {filename}")
        except Exception as error:
            print(f"✗ Error cargando {filename}: {error}")

@tasks.loop(minutes=2)
async def cambiar_estado():
    estado = random.choice(ESTADOS)

    await bot.change_presence(
        activity=discord.Game(name=estado)
    )

@bot.event
async def on_ready():
    print(f"\n🤖 Botardito conectado como {bot.user}")

    await load_cogs()

    if not cambiar_estado.is_running():
        cambiar_estado.start()

    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} comandos sincronizados")
    except Exception as error:
        print(f"Error sincronizando comandos: {error}")


if not TOKEN:
    raise RuntimeError("Falta TOKEN en el archivo .env")

bot.run(TOKEN)