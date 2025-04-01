import discord
from discord.ext import commands
from commands.game import Game
from entities.challenge import Challenge
import random
import re

class Challenges(commands.Cog):
    def __init__(self, game : Game):
        self._game = game
        self._challenge = Challenge()

    @commands.command()
    async def today(self, ctx):
        """Add new members in list of members"""
        guild = ctx.guild.id
        index = self._game.index_of_member(ctx.author)
        if index != -1:
            if self._game.get_all_members()[index].get_is_play(guild):
                challenges = self._challenge.get_all_challenges_on_day()
                if challenges:
                    for c in challenges:
                        await ctx.send(embed=self._generate_embed_to_display_information_challenge(c))
                else:
                    await ctx.send(embed=self._generate_embed(
                        discord.Color.red(),
                        title="Pas de défi aujourd'hui 😕",
                        description="Malheureusement, il n'y a pas de défi disponible pour le moment.\nRevenez demain pour de nouvelles aventures coding !"
                    ))
        else:
            await ctx.send(embed=discord.Embed(
                color=discord.Color.red(),
                title="Recherche du ou des défis du jour 😕",
                description="Vous n'avez pas accès tant que vous vous y inscrivez pas."
            ))

    @commands.command()
    async def challenge(self, ctx, index : int = 1):
        guild = ctx.guild.id
        index_member = self._game.index_of_member(ctx.author)
        if index_member != -1:
            if self._game.get_all_members()[index_member].get_is_play(guild):
                challenge = self._challenge.get_one_challenge_on_day(index)
                if challenge:
                    await ctx.send(embed=self._generate_embed_to_display_information_challenge(challenge))
                else:
                    await ctx.send(embed=self._generate_embed(
                        discord.Color.red(),
                        title=f"Recherche du défi d'identifiant {index}  - Défi introuvable 😕",
                        description=f"Le défi avec l'index {index} n'a pas été trouvé pour aujourd'hui."
                    ))
        else:
            await ctx.send(embed=discord.Embed(
                color=discord.Color.red(),
                title=f"Recherche du défi d'identifiant {index} 😕",
                description="Vous n'avez pas accès tant que vous vous y inscrivez pas."
            ))

    @commands.command()
    async def publish(self, ctx, git_link : str, index : int = 1):
        if not self._challenge.have_challenge_with_index(index):
            await ctx.send(embed=self._generate_embed(
                discord.Color.red(),
                title="Publication du défi du jour 😕",
                description=f"Le défi d'identifiant {index} n'existe pas"
            ))
            return

        m = self._game.get_all_members()[self._game.index_of_member(ctx.author)]
        guild = ctx.guild.id
        if m.get_is_play(guild):
            if not self._is_valid_url(git_link):
                await ctx.send(embed=self._generate_embed(
                    discord.Color.red(),
                    title="Publication du défi du jour - Lien invalide 😕",
                    description="Le lien spécifié n'est pas valide. Assurez-vous qu'il s'agit d'un lien git amenant au repository."
                ))
                return
            m.add_participate(index, guild)
            await ctx.send(embed=self._generate_embed(
                discord.Color.green(),
                title="Publication du défi du jour 😊",
                description=f"En attente des votes sur le défi publié par {m.get_member().mention}!"
            ))
        else:
            await ctx.send(embed=self._generate_embed(
                discord.Color.red(),
                title="Publication du défi du jour - Erreur du rôle 😕",
                description="Tu ne peux pas réaliser de défi car tu n'es pas inscrit dans la liste des participants."
            ))
            return

    @commands.command()
    async def vote(self, ctx, member: discord.Member, score : int, index : int = 1):
        if not self._challenge.have_challenge_with_index(index):
            await ctx.send(embed=self._generate_embed(
                discord.Color.red(),
                title="Vote d'un défi réalisé par un joueur 😕",
                description=f"Le défi d'identifiant {index} n'existe pas"
            ))
            return

        if score < 1 or score > 10 or index < 1:
            await ctx.send(embed=discord.Embed(
                color=discord.Color.red(),
                title="Vote d'un défi réalisé par un joueur 😕",
                description="Soit l'identifiant du défi n'est pas valide, soit la note n'est pas un nombre compris entre 1 et 10."
            ))
            return

        guild = ctx.guild.id
        m = self._game.search_member(member.name, guild)

        if not m:
            await ctx.send(embed=discord.Embed(
                color=discord.Color.red(),
                title="Vote d'un défi réalisé par un joueur 😕",
                description="Le membre n'est pas inscrit dans la liste des participants."
            ))
            return
        if m.get_member() == ctx.author:
            await ctx.send(embed=discord.Embed(
                color=discord.Color.red(),
                title="Vote d'un défi réalisé par un joueur 😕",
                description="Vous ne pouvez pas noter votre propre défi."
            ))
            return

        if m.has_realized(index, guild):
            m.add_points(score)
            await ctx.send(embed=discord.Embed(
                color=discord.Color.green(),
                title="Vote d'un défi réalisé par un joueur ✅",
                description=f'{m.get_member().mention} a reçu {score} points pour ce challenge par {ctx.author.mention}!'
            ))
        else:
            await ctx.send(embed=discord.Embed(
                color=discord.Color.red(),
                title="Vote d'un défi réalisé par un joueur 😕",
                description="Le membre n'a pas réalisé le défi du jour."
            ))

    def _is_valid_url(self, url):
        git_url_regex = r'^(https?://(www\.)?(github|gitlab|bitbucket)\.com/[\w-]+/[\w-]+(\.git)?)|(^git@(?:www\.)?(github|gitlab|bitbucket)\.com:([\w-]+/[\w-]+)(\.git)$)'
        return bool(re.match(git_url_regex, url))

    def _is_numeric(self, index):
        is_numeric = True
        for c in index:
            if not 47 < ord(c) < 58:
                is_numeric = False
                break
        return is_numeric

    def _get_random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = (r << 16) + (g << 8) + b
        return color

    def _generate_embed(self, color, title="Erreur", description="Une erreur s'est produite."):
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )
        return embed

    def _generate_embed_to_display_information_challenge(self, information):
        e = discord.Embed(
            title = information["titre"],
            description = information["description"],
            color = self._get_random_color()
        )
        e.add_field(name="Explications", value=information["explication"], inline=False)
        e.add_field(name="Fonctionnement", value=information["fonctionnement"], inline=False)
        e.add_field(name="Temps d'exécution", value=information["temps_execution"], inline=False)
        if "objectifs" in information:
            e.add_field(name="La liste des objectifs", value=information["objectifs"], inline=False)
        if "criteres" in information:
            e.add_field(name="Critères de réussites", value=information["criteres"], inline=False)
        if "extensions_facultatives" in information:
            e.add_field(name="Extensions facultatives", value=information["extensions_facultatives"], inline=False)
        if "instructions" in information:
            e.add_field(name="Les instructions", value=information["instructions"], inline=False)
        if "output" in information:
            e.add_field(name="Sortie", value=information["output"], inline=False)
        if "exemple_de_deroulement" in information:
            e.add_field(name="Exemples de réalisations", value=information["exemple_de_deroulement"], inline=False)
        return e