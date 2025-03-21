import discord
from discord.ext import commands
from commands.game import Game
from entities.challenge import Challenge

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
            await ctx.send(f'{self._challenge.get_all_challenges_on_day()}')