import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from commands.game import Game
from commands.help import Help
from commands.challenges import Challenges

load_dotenv()

bot = commands.Bot(command_prefix = ">", intents = discord.Intents.all())

@bot.event
async def on_ready():
    game = Game()
    try:
        await bot.add_cog(Help())
        await bot.add_cog(game)
        await bot.add_cog(Challenges(game))
    except Exception as e:
        print(f"Erreur lors du chargement de l'extension : {e}")

bot.run(os.getenv("TOKEN"))