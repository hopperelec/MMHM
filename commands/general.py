import discord
from discord.ext import commands
from commands.addcommand import addcommand

class GeneralCommands(commands.Cog):
    def __init__(self,bot): self.bot = bot
    async def cog_check(self,ctx): return ctx.prefix == "?" and str(ctx.channel) == "general"
    
    @addcommand()
    async def ping(self,ctx): await ctx.send("Pong! "+str(int(round(self.bot.latency,3)*1000))+"ms")

    @addcommand(aliases=["youtube"])
    @commands.cooldown(rate=1,per=1800,type=commands.BucketType.guild)
    async def yt(self,ctx): await ctx.send("https://yt.hopperelec.co.uk")
    @addcommand()
    @commands.cooldown(rate=1,per=1800,type=commands.BucketType.guild)
    async def discord(self,ctx): await ctx.send("https://discord.gg/TAfUHS6")
    @addcommand(aliases=["facebook"])
    @commands.cooldown(rate=1,per=1800,type=commands.BucketType.guild)
    async def fb(self,ctx): await ctx.send("https://fb.com/HopperElec")
    @addcommand()
    @commands.cooldown(rate=1,per=1800,type=commands.BucketType.guild)
    async def twitter(self,ctx): await ctx.send("https://twitter.com/HopperElec")
    @addcommand(aliases=["merchandise","tshirt"])
    @commands.cooldown(rate=1,per=1800,type=commands.BucketType.guild)
    async def merch(self,ctx): await ctx.send("https://store.hopperelec.co.uk")
def setup(bot): bot.add_cog(GeneralCommands(bot))