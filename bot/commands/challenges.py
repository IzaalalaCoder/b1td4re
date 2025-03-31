import discord
from discord.ext import commands
from commands.game import Game
from entities.challenge import Challenge
import random
import re

class Challenges(commands.Cog):
    def __init__(self, bot, game : Game):
        self.bot = bot
        self._game = game
        self._challenge = Challenge()

    @commands.command()
    async def today(self, ctx, *, member: discord.Member = None):
        """Add new members in list of members"""
        guild = ctx.message.guild.id
        if self._game.get_all_members()[self._game.index_of_member(member)].get_is_play(guild):
            challenges = self._challenge.get_all_challenges_on_day()
            if challenges:
                for c in challenges:
                    await ctx.send(embed=self._generate_embed_to_display_informations_challenge(c))
            else:
                await ctx.send(embed=self._generate_embed(
                    discord.Color.red(),
                    title="Pas de défi aujourd'hui 😔",
                    description="Malheureusement, il n'y a pas de défi disponible pour le moment.\nRevenez demain pour de nouvelles aventures coding !"
                ))

    @commands.command()
    async def challenge(self, ctx, *index, member: discord.Member = None):
        if len(index) != 1 or not self._is_numeric(index[0]):
            await ctx.send(embed=self._generate_embed(
                discord.Color.red(),
                title="Aucun challenge n'a été spécifié 😕",
                description="La commande est la suivante : >challenge <int>"
            ))
            return
        guild = ctx.message.guild.id
        if self._game.get_all_members()[self._game.index_of_member(member)].get_is_play(guild):
            challenge = self._challenge.get_one_challenge_on_day(int(index[0]))
            if challenge:
                await ctx.send(embed=self._generate_embed_to_display_informations_challenge(challenge))
            else:
                await ctx.send(embed=self._generate_embed(
                    discord.Color.red(),
                    title="Défi introuvable 😕",
                    description=f"Le défi avec l'index {index[0]} n'a pas été trouvé pour aujourd'hui."
                ))

    @commands.command()
    async def publish(self, ctx, *arg, member: discord.Member = None):
        m = self._game.get_all_members()[self._game.index_of_member(member)]
        guild = ctx.message.guild.id
        if m.get_is_play(guild):
            if len(arg) != 2 or not self._is_numeric(arg[0]):
                await ctx.send(embed=self._generate_embed(
                    discord.Color.red(),
                    title="Aucun challenge n'a été spécifié 😕",
                    description="La commande est la suivante : >publish <int> <link>"
                ))
                return
            if not self._is_valid_url(arg[1]):
                await ctx.send(embed=self._generate_embed(
                    discord.Color.red(),
                    title="Lien invalide 😕",
                    description="Le lien spécifié n'est pas valide. Assurez-vous qu'il s'agit d'un lien git amenant au repository."
                ))
                return
            m.add_participate(int(arg[0]), guild)
            await ctx.send(embed=self._generate_embed(
                discord.Color.green(),
                title="Le défi du jour a bien été réalisé 😊",
                description=f"En attente des votes sur le défi publié par {m.get_member().mention}!"
            ))
        else:
            await ctx.send(embed=self._generate_embed(
                discord.Color.red(),
                title="Erreur du rôle 😕",
                description="Tu ne peux pas réaliser de défi car tu n'es pas inscrit dans la liste des participants."
            ))
            return

    @commands.command()
    async def vote(self, ctx, *arg, member: discord.Member = None):
        if len(arg) != 3:
            await ctx.send(embed=discord.Embed(
                color=discord.Color.red(),
                title="Erreur 😕",
                description="Soit aucun membre n'est mentionné, soit aucun défi du jour n'a été désigné ou soit aucun score n'a été donné. La commande est la suivante >vote <name> <id> <score>"
            ))
            return

        if not self._is_numeric(arg[1]) or not self._is_numeric(arg[2]) or (self._is_numeric(arg[2]) and (int(arg[2]) < 1 or int(arg[2]) > 10)):
            await ctx.send(embed=discord.Embed(
                color=discord.Color.red(),
                title="Erreur 😕",
                description="Soit l'identifiant du défi n'est pas valide, soit la note n'est pas valide, soit la note n'est pas un nombre compris entre 1 et 10.."
            ))
            return

        guild = ctx.message.guild.id
        author = self._game.get_all_members()[self._game.index_of_member(member)]
        m = self._game.search_member(arg[0], guild)

        if not m:
            await ctx.send(embed=discord.Embed(
                color=discord.Color.red(),
                title="Erreur 😕",
                description="Le membre n'est pas inscrit dans la liste des participants."
            ))
            return
        if m == author:
            await ctx.send(embed=discord.Embed(
                color=discord.Color.red(),
                title="Erreur 😕",
                description="Vous ne pouvez pas noter votre propre défi."
            ))
            return

        if m.has_realized(int(arg[1]), guild):
            m.add_points(int(arg[2]))
            await ctx.send(embed=discord.Embed(
                color=discord.Color.green(),
                title="Vote réussi ✅",
                description=f'{m.get_member().mention} a reçu {arg[2]} points pour ce challenge par {author.get_member().mention}!'
            ))
        else:
            await ctx.send(embed=discord.Embed(
                color=discord.Color.red(),
                title="Erreur 😕",
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
            description = informations["description"],
            color = self._get_random_color()
        )
        e.add_field(name="Explications", value=information["explication"], inline=False)
        e.add_field(name="Fonctionnement", value=information["fonctionnement"], inline=False)
        e.add_field(name="Temps d'exécution", value=information["temps_execution"], inline=False)
        if "objectifs" in information:
            e.add_field(name="La liste des objectifs", value=information.add_field(name="Critères de réussites", value=information["criteres"], inline=False))
        if "extensions_facultatives" in information:
            e.add_field(name="Extensions facultatives", value=information["extensions_facultatives"], inline=False)
        if "instructions" in information:
            e.add_field(name="Les instructions", value=information["instructions"], inline=False)
        if "output" in information:
            e.add_field(name="Sortie", value=information["output"], inline=False)
        if "exemple_de_deroulement" in information:
            e.add_field(name="Exemples de réalisations", value=information["exemple_de_deroulement"], inline=False)
        return e