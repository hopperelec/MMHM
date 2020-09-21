import discord
from discord.ext import commands
from commands.addcommand import addcommand

class FunCommands(commands.Cog):
    def __init__(self,bot): self.bot = bot
    async def cog_check(self,ctx): return ctx.prefix == "!" and str(ctx.channel) == "fun"
    

def setup(bot): bot.add_cog(FunCommands(bot))