from discord.ext import commands

@commands.command()
async def coucou(ctx):
    await ctx.send("coucou")

def setup(bot):
    bot.add_command(coucou)