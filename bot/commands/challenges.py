import discord
from discord.ext import commands
from commands.game import Game

import xml.etree.ElementTree as ET

# Chargement du fichier XML

class Challenges(commands.Cog):
    def __init__(self, bot, game : Game):
        self.bot = bot
        self._game = game

    # Récupération des informations spécifiques
    def get_challenge_details(self):
        tree = ET.parse('bot/assets/april/2025.xml')  # Remplacer par le chemin de votre fichier XML
        root = tree.getroot()
        # Trouver le challenge du jour 1 (ou autre jour selon votre besoin)
        challenge = root.find(".//challenge[@jour='1']")

        if challenge is not None:
            # Récupérer les informations spécifiques du challenge
            titre = challenge.find("titre").text
            explication = challenge.find("explication").text
            description = challenge.find("description").text

            # Récupérer les critères de succès
            criteres_succes = []
            for critere in challenge.findall(".//criteres_succes/critere"):
                criteres_succes.append(critere.text)

            # Affichage des résultats
            text = f"Titre: {titre}\nExplication: {explication}\nDescription: {description} \nCritères de succès:"
            for critere in criteres_succes:
                text += f"\n- {critere}"
            return text
        else:
            return "Le challenge pour le jour spécifié n'a pas été trouvé."

    @commands.command()
    async def today(self, ctx, *, member: discord.Member = None):
        """Add new members in list of members"""
        guild = ctx.message.guild.id
        if self._game.get_all_members()[self._game.index_of_member(member)].get_is_play(guild):
            await ctx.send(f'{self.get_challenge_details()}')