import discord
from discord.ext import commands

class Help(commands.Cog):

    @commands.command()
    async def helps(self, ctx):
        embed = discord.Embed(
            color=discord.Color.blue(),
            title="Liste des commandes disponibles",
            description="Voici la liste des commandes que vous pouvez utiliser pour interagir avec le bot."
        )

        embed.add_field(
            name=">add",
            value="Ajoute un membre à la liste des joueurs. Si aucun membre n'est spécifié, cela s'applique à l'utilisateur qui envoie la commande.",
            inline=False
        )

        embed.add_field(
            name=">rem",
            value="Retire un membre de la compétition. Si aucun membre n'est spécifié, cela s'applique à l'utilisateur qui envoie la commande.",
            inline=False
        )

        embed.add_field(
            name=">delete",
            value="Supprime un membre de la liste des joueurs. Cela les retire définitivement de la compétition.",
            inline=False
        )

        embed.add_field(
            name=">rank",
            value="Affiche le classement actuel des joueurs, trié par points.",
            inline=False
        )

        embed.add_field(
            name=">players",
            value="Affiche la liste des joueurs qui participent actuellement.",
            inline=False
        )

        embed.add_field(
            name=">calendar [@membre]",
            value="Affiche le calendrier des défis pour un joueur. Si aucun membre n'est spécifié, cela s'applique à l'utilisateur qui envoie la commande.",
            inline=False
        )

        embed.add_field(
            name=">today",
            value="Affiche les défis du jour pour un membre. Si aucun membre n'est spécifié, cela s'applique à l'utilisateur qui envoie la commande.",
            inline=False
        )

        embed.add_field(
            name=">challenge [index:int]",
            value="Affiche les détails du défi avec l'index spécifié pour un membre. Si aucun membre n'est spécifié, cela s'applique à l'utilisateur qui envoie la commande. L'index par défaut est 1.",
            inline=False
        )

        embed.add_field(
            name=">publish <git_link:str> [index:int]",
            value="Publie un défi pour un joueur, associant un lien vers un repository Git. L'index par défaut est 1. Le lien doit être valide.",
            inline=False
        )

        embed.add_field(
            name=">vote <member:discord.Member> <score:int> [index:int]",
            value="Permet de voter sur un défi réalisé par un autre joueur. Vous devez spécifier le membre, le score (entre 1 et 10), et l'index du défi. L'index par défaut est 1.",
            inline=False
        )

        embed.set_footer(text="Utilisez >help pour afficher cette liste.")
        await ctx.send(embed=embed)

