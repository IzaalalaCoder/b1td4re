import discord
from discord.ext import commands
from entities.member import Member

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._members = []

    @commands.command()
    async def add(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        """Add new members in list of members"""
        index = self.index_of_member(member)
        if index == -1 and member != None:
            self._members.append(Member(member))
            await ctx.send(f'{member.name} est ajouté à la liste des participants')
        else:
            m = self._members[index]
            if not m.get_is_play():
                m.set_is_play(True)
                await ctx.send(f'{member.name} est a nouveau dans la liste des participants')
            else:
                await ctx.send(f'{member.name} fait déjà partie des participants')

    @commands.command()
    async def rem(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        """Remove members of the game"""
        index = self.index_of_member(member)
        if index != -1 and member != None:
            m = self._members[index]
            if m.get_is_play():
                m.set_is_play(False)
                await ctx.send(f'{member.name} est retiré de la liste des participants')
            else:
                await ctx.send(f'{member.name} s\' déjà retiré des participants')
        else:
            await ctx.send(f'{member.name} n\'a jamais participé')

    @commands.command()
    async def delete(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        """Remove definitely members in list of members"""
        index = self.index_of_member(member)
        if index != -1 and member != None:
            self._members.pop(index)
            await ctx.send(f'{member.name} est retiré de la liste des membres')
        else:
            await ctx.send(f'{member.name} n\'a jamais participé')

    @commands.command()
    async def rank(self, ctx):
        """Display rank"""
        if not self._members:
            await ctx.send("Aucun membre dans le classement.")
            return
        members = sorted(self._members, key=lambda m: m.get_points(), reverse=True)
        text = ""
        for m in members:
            playing = "Participe" if m.get_is_play() else "Ne participe plus"
            text += f"{m.get_member().name} - {m.get_points()} - {playing} \n"
        await ctx.send(text)

    def index_of_member(self, member: discord.Member):
        for m in self._members:
            if member == m.get_member():
                return self._members.index(m)
        return -1