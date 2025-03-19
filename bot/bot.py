import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from commands.greetings import Greetings
from commands.game import Game

load_dotenv()

bot = commands.Bot(command_prefix = ">", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    try:
        await bot.add_cog(Greetings(bot))
        await bot.add_cog(Game(bot))
    except Exception as e:
        print(f"Erreur lors du chargement de l'extension : {e}")

bot.run(os.getenv("TOKEN"))