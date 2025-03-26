import discord
from discord.ext import commands
from commands.game import Game
from entities.challenge import Challenge
import random

class Challenges(commands.Cog):
    def __init__(self, bot, game : Game):
        self.bot = bot
        self._game = game
        self._challenge = Challenge()

    def _is_numeric(self, index):
        is_numeric = True
        for c in index:
            if not 47 < ord(c) < 58:
                is_numeric = False
                break
        return is_numeric

    def _create_embed_for_challenge(self):
        pass

    @commands.command()
    async def today(self, ctx, *, member: discord.Member = None):
        """Add new members in list of members"""
        guild = ctx.message.guild.id
        if self._game.get_all_members()[self._game.index_of_member(member)].get_is_play(guild):
            for c in self._challenge.get_all_challenges_on_day():
                await ctx.send(embed = self._generate_embed_to_display_informations_challenge(c))

    @commands.command()
    async def challenge(self, ctx, *index, member: discord.Member = None):
        if len(index) != 1 or not self._is_numeric(index[0]):
            await ctx.send("Aucun challenge n'a été spécifié")
            return
        guild = ctx.message.guild.id
        if self._game.get_all_members()[self._game.index_of_member(member)].get_is_play(guild):
            challenge = self._challenge.get_one_challenge_on_day(int(index[0]))
            await ctx.send(embed = self._generate_embed_to_display_informations_challenge(challenge))

    @commands.command()
    async def publish(self, ctx, *arg, member: discord.Member = None):
        if len(arg) != 2 or not self._is_numeric(arg[0]):
            await ctx.send("Aucun challenge n'a été spécifié")
            return
        guild = ctx.message.guild.id
        m = self._game.get_all_members()[self._game.index_of_member(member)]
        if m.get_is_play(guild):
            m.add_participate()
            await ctx.send(f'{self._challenge.get_one_challenge_on_day(int(index[0]))}')

    @commands.command()
    async def vote(self, ctx, *arg, member: discord.Member = None):
        if len(arg) != 2 or self._is_numeric(arg[0]) or not self._is_numeric(arg[1]):
            await ctx.send("Aucun membre ou aucune note n'a été spécifié")
            return
        guild = ctx.message.guild.id
        m = self._game.search_member(arg[0])
        if self._game.get_all_members()[self._game.index_of_member(m)].get_is_play(guild):
            m.add_points(int(arg[1]))
            await ctx.send(f'{self._challenge.get_one_challenge_on_day(int(arg[0]))}')

    def _get_random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = (r << 16) + (g << 8) + b
        return color

    def _generate_embed_to_display_informations_challenge(self, informations):
        e = discord.Embed(
            title = informations["titre"],
            description = informations["description"],
            color = self._get_random_color()
        )
        e.add_field(name="Explications", value=informations["explication"])
        if "criteres" in informations:
            e.add_field(name="Critères de réussites", value=informations["criteres"])
        if "exemple_de_deroulement" in informations:
            e.add_field(name="Exemples de réalisations", value=informations["exemple_de_deroulement"])
        return e