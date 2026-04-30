import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

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


@bot.event
async def on_ready():
    print(f"\n🤖 Botardito conectado como {bot.user}")

    await load_cogs()

    synced = await bot.tree.sync()
    print(f"✓ {len(synced)} comandos globales sincronizados\n")


if not TOKEN:
    raise RuntimeError("Falta TOKEN en el archivo .env")

bot.run(TOKEN)