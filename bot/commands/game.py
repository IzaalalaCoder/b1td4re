import discord
from discord.ext import commands
from entities.member import Member

class Game(commands.Cog):
    def __init__(self):
        self._members = []

    def get_all_members(self):
        return self._members

    def search_member(self, name, guild):
        for member in self._members:
            if member.get_member().name == name and member.get_is_play(guild):
                return member
        return None

    def index_of_member(self, member: discord.Member):
        for m in self._members:
            if member == m.get_member():
                return self._members.index(m)
        return -1

    @commands.command()
    async def add(self, ctx):
        """Add new members in list of members"""
        member = ctx.author
        guild = ctx.guild.id
        index = self.index_of_member(member)
        if index == -1:
            self._members.append(Member(member))
            self._members[-1].set_is_play(True, guild)
            embed = discord.Embed(
                color=discord.Color.green(),
                title="Ajout d'un membre 😊",
                description=f'{member.name} est maintenant prêt à jouer dans {ctx.guild.name}'
            )
            await ctx.send(embed=embed)
        else:
            m = self._members[index]
            if not m.contain_guild(guild):
                m.set_is_play(True, guild)
                description = f'{member.name} est maintenant prêt à jouer dans {ctx.guild.name}'
            elif not m.get_is_play(guild):
                description = f'{member.name} est maintenant à nouveau prêt à jouer dans {ctx.guild.name}'
            else:
                description = f'{member.name} joue déjà dans {ctx.guild.name}'
            embed = discord.Embed(
                color=discord.Color.green(),
                title="Ajout d'un membre 😊",
                description=description
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def rem(self, ctx):
        """Remove members of the game"""
        guild = ctx.guild.id
        index = self.index_of_member(ctx.author)
        if index != -1:
            m = self._members[index]
            if m.contain_guild(guild):
                if m.get_is_play(guild):
                    m.set_is_play(False, guild)
                    embed = discord.Embed(
                        color=discord.Color.green(),
                        title="Retrait d'un membre 😊",
                        description=f'{ctx.author.name} se retire de la compétition dans {ctx.guild.name}'
                    )
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        color=discord.Color.green(),
                        title="Retrait d'un membre 😊",
                        description=f'{ctx.author.name} s\'est déjà retiré de la compétition dans {ctx.guild.name}'
                    )
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    color=discord.Color.red(),
                    title="Retrait d'un membre 😕",
                    description=f'{ctx.author.name} n\'a jamais joué dans {ctx.guild.name}'
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                color=discord.Color.red(),
                title="Retrait d'un membre 😕",
                description=f'{ctx.author.name} n\'a jamais joué dans {ctx.guild.name}'
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def delete(self, ctx):
        """Remove members of the game"""
        member = ctx.author
        guild = ctx.guild.id
        index = self.index_of_member(member)
        if index != -1 and member is not None:
            m = self._members[index]
            if m.contain_guild(guild):
                self._members.pop(index)
                embed = discord.Embed(
                    color=discord.Color.green(),
                    title="Retrait définitif d'un membre 😊",
                    description=f'{member.name} ne fait maintenant plus parti des joueurs dans {ctx.guild.name}'
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    color=discord.Color.red(),
                    title="Retrait définitif d'un membre 😕",
                    description=f'{member.name} n\'a jamais joué dans {ctx.guild.name}'
                )
                await ctx.send(embed=embed)

    @commands.command()
    async def rank(self, ctx):
        """Display rank"""
        guild = ctx.guild.id
        members = self._members_by_guild(guild)
        if len(members) == 0:
            await ctx.send(embed=discord.Embed(
                color=discord.Color.red(),
                title="Affichage du classement 😕",
                description=f"Aucun membre dans le classement dans {ctx.guild.name}"
            ))
            return
        members = sorted(members, key=lambda m: m.get_points(), reverse=True)
        text = ""
        for m in members:
            playing = "Participe" if m.get_is_play(guild) else "Ne participe plus"
            text += f"- {m.get_member().name} | {m.get_points()} | {playing} \n"

        await ctx.send(embed=discord.Embed(
                color=discord.Color.green(),
                title="Affichage du classement 😊",
                description=text
            ))

    @commands.command()
    async def players(self, ctx):
        """Display the list of players who are participating"""
        guild = ctx.guild.id
        members = self._members_by_guild(guild)
        if len(members) == 0:
            await ctx.send(embed=discord.Embed(
                color=discord.Color.red(),
                title="Affichage des joueurs 😕",
                description=f"Aucun joueurs dans le classement dans {ctx.guild.name}"
            ))
            return
        text = ""
        for m in members:
            if m.get_is_play(guild):
                text += f"- {m.get_member().name}\n"
        if text == "":
            text = "Aucun membre ne joue pour le moment"

        await ctx.send(embed=discord.Embed(
                color=discord.Color.green(),
                title="Affichage des joueurs 😊",
                description=text
            ))

    @commands.command()
    async def calendar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        index = self.index_of_member(member)

        if index != -1 and member is not None:
            m = self._members[index]
            if m.contain_guild(ctx.guild.id):
                calendar_data = m.get_calendar_playing_by_guild(ctx.guild.id)
                playings = calendar_data[0]
                day_counter = calendar_data[1]

                text = "```\n"
                text += "Lu  Ma  Me  Je  Ve  Sa  Di\n"
                text += "--- --- --- --- --- --- ---\n"

                text += "    " * day_counter

                for i, value in enumerate(playings):

                    text += f"{'✅' if value else '❌'}  "
                    day_counter += 1

                    if day_counter == 7:
                        text += "\n"
                        day_counter = 0

                text += "```"
                await ctx.send(text)
            else:
                await ctx.send(embed=discord.Embed(
                    color=discord.Color.red(),
                    title="Affichage du calendrier de défis 😕",
                    description=f'{member.name} n\'a jamais joué dans {ctx.guild.name}'
                ))
        else:
            await ctx.send(embed=discord.Embed(
                color=discord.Color.red(),
                title="Affichage du calendrier de défis 😕",
                description=f'{member.name} n\'a jamais joué dans {ctx.guild.name}'
            ))

    def _members_by_guild(self, guild):
        members = []
        for m in self._members:
            if m.contain_guild(guild):
                members.append(m)
        return members