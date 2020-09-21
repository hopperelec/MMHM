# print(self.bot.get_cog("EcoCommands").economy["HopperElecYT#2211"]["balance"])
# await mcrsend(["say Hey guys wassup","say It's ya boy chips ahoy"],message.channel)

import discord
from discord.ext import commands
from mcrcon import mcrcon,mcrsend
from commands.addcommand import addcommand

class TrollCommands(commands.Cog):
    def __init__(self,bot): self.bot = bot
    async def cog_check(self,ctx): return ctx.prefix == "/" and str(ctx.channel) == "trollme"

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.content != "":
            if message.content[0] == "/" and str(message.channel) == "trollme":
                await message.channel.send(f"Hopper is not currently streaming and so these commands are disabled, {ctx.author.name}",delete_after=10)
                await message.delete(delay=10)

def setup(bot): bot.add_cog(TrollCommands(bot))