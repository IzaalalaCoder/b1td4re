import discord
from discord.ext import commands
from entities.member import Member

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._members = []

    @commands.command()
    async def add(self, ctx, *, member: discord.Member = None):
        """Add new members in list of members"""
        member = member or ctx.author
        guild = ctx.message.guild.id
        index = self._index_of_member(member)
        if index == -1 and member != None:
            self._members.append(Member(member))
            self._members[-1].set_is_play(True, guild)
        else:
            m = self._members[index]
            m.set_is_play(True, guild)
        await ctx.send(f'{member.name} est maintenant prêt à jouer dans {ctx.message.guild.name}')

    @commands.command()
    async def rem(self, ctx, *, member: discord.Member = None):
        """Remove members of the game"""
        member = member or ctx.author
        guild = ctx.message.guild.id
        index = self._index_of_member(member)
        if index != -1 and member != None:
            m = self._members[index]
            if m.contain_guild(guild):
                if m.get_is_play(guild):
                    m.set_is_play(False, guild)
                    await ctx.send(f'{member.name} se retire de la compétition dans {ctx.message.guild.name}')
            else:
                await ctx.send(f'{member.name} n\'a jamais joué dans {ctx.message.guild.name}')

    @commands.command()
    async def delete(self, ctx, *, member: discord.Member = None):
        """Remove members of the game"""
        member = member or ctx.author
        guild = ctx.message.guild.id
        index = self._index_of_member(member)
        if index != -1 and member != None:
            m = self._members[index]
            if m.contain_guild(guild):
                self._members.pop(index)
                await ctx.send(f'{member.name} ne fait maintenant plus parti des joueurs dans {ctx.message.guild.name}')
            else:
                await ctx.send(f'{member.name} n\'a jamais joué dans {ctx.message.guild.name}')

    @commands.command()
    async def rank(self, ctx):
        """Display rank"""
        guild = ctx.message.guild.id
        members = self._members_by_guild(guild)
        if len(members) == 0:
            await ctx.send(f"Aucun membre dans le classement dans {ctx.message.guild.name}")
            return
        members = sorted(members, key=lambda m: m.get_points(), reverse=True)
        text = ""
        for m in members:
            playing = "Participe" if m.get_is_play(guild) else "Ne participe plus"
            text += f"{m.get_member().name} - {m.get_points()} - {playing} \n"
        await ctx.send(text)

    def _index_of_member(self, member: discord.Member):
        for m in self._members:
            if member == m.get_member():
                return self._members.index(m)
        return -1

    def _members_by_guild(self, guild):
        members = []
        for m in self._members:
            if m.contain_guild(guild):
                members.append(m)
        return members