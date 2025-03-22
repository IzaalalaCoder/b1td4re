import discord
from discord.ext import commands
from commands.game import Game
from entities.challenge import Challenge

class Challenges(commands.Cog):
    def __init__(self, bot, game : Game):
        self.bot = bot
        self._game = game
        self._challenge = Challenge()

    def is_numeric(self, index):
        is_numeric = True
        for c in index:
            if not 47 < ord(c) < 58:
                is_numeric = False
                break
        return is_numeric

    @commands.command()
    async def today(self, ctx, *, member: discord.Member = None):
        """Add new members in list of members"""
        guild = ctx.message.guild.id
        if self._game.get_all_members()[self._game.index_of_member(member)].get_is_play(guild):
            await ctx.send(f'{self._challenge.get_all_challenges_on_day()}')

    @commands.command()
    async def challenge(self, ctx, *index, member: discord.Member = None):
        if len(index) != 1 or not self.is_numeric(index[0]):
            await ctx.send("Aucun challenge n'a été spécifié")
            return
        guild = ctx.message.guild.id
        if self._game.get_all_members()[self._game.index_of_member(member)].get_is_play(guild):
            await ctx.send(f'{self._challenge.get_one_challenge_on_day(int(index[0]))}')