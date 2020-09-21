import discord
from discord.ext import commands
from os.path import isfile
from json import load,dump
from asyncio import sleep
from commands.addcommand import addcommand
from random import randint,choice
from datetime import datetime
from datetime import timedelta

class EcoCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        if isfile('economy.json'):
            with open('economy.json','r') as jsonfile: self.economy = load(jsonfile)
        else:
            with open('economy.json','w') as jsonfile: self.economy = {}; dump({},jsonfile)
        self.bot.loop.create_task(self.ecoloop())
    async def cog_check(self,ctx): return ctx.prefix in ["$","£"] and (str(ctx.channel) == "economy" or str(ctx.channel).startswith("Direct Message with "))

    @commands.Cog.listener()
    async def on_member_join(self,member):
        if not member.bot: await self.adduser(member.id)
    @commands.Cog.listener()
    async def on_message(self,message):
        if str(message.channel) == "general" and len(message.content) >= 7 and not message.content[0] in ['/','$','£','!','?'] and not message.author.bot:
            if str(message.author.id) in self.economy:
                if datetime.fromisoformat(self.economy[str(message.author.id)]["allowmsg"]) > datetime.now(): return
            await sleep(0.2)
            if await message.channel.fetch_message(message.id) == message:
                await message.channel.send("True!")
                self.economy[message.author.id]["allowmsg"] = str(datetime.now()+timedelta(seconds=30))
                self.economy[message.author.id]["cash"] += randint(1,5)
                await self.economyupdate()

    @addcommand(aliases=["balance","bank","cash","bankbal","bankbalance"])
    @commands.cooldown(rate=3,per=60,type=commands.BucketType.user)
    async def bal(self,ctx,*member):
        if member != ():
            ctx.member = member; member = await self.findmemberfrom(ctx)
            if type(member) == str:
                await ctx.send(embed=(discord.Embed(
                    title=f"Balance of {self.bot.get_user(int(member)).name}#{self.bot.get_user(int(member)).discriminator}",
                    description=f"Bank : {str(self.economy[member]['bank'])} | Cash : {str(self.economy[str(member)]['cash'])}",
                    color=0xe31313).set_footer(text=f"Requested by {ctx.author}")).set_thumbnail(url=self.bot.get_user(int(member)).avatar_url))
        else:
            if str(ctx.author.id) in self.economy:
                await ctx.send(embed=(discord.Embed(
                    title=f"Balance of {str(ctx.author)}",
                    description=f"Bank : {str(self.economy[str(ctx.author.id)]['bank'])} | Cash : {str(self.economy[str(ctx.author.id)]['cash'])}",
                    color=0xe31313).set_footer(text=f"Requested by {ctx.author}")).set_thumbnail(url=ctx.author.avatar_url))
            else:
                await self.adduser(ctx.author.id);
                await ctx.send("Balance of "+str(ctx.author)+":")
                await ctx.send(f"Bank : 1440 | Cash : 10")

    @addcommand(aliases=["leaderboard"])
    @commands.cooldown(rate=2,per=120,type=commands.BucketType.user)
    async def lb(self,ctx,cash=None):
        if cash == None:
            embed = discord.Embed(title="Economy leaderboard", description="List of peoples' money in the economy in order of balance", color=0xe31313)
            for i,member in enumerate(sorted(self.economy.items(),key=lambda e:e[1]["cash"]+e[1]["bank"],reverse=True)):
                embed.add_field(name=str(i+1)+". "+member[1]["lastname"],value="Cash: "+str(member[1]["cash"])+" | Bank: "+str(member[1]["bank"]),inline=False)
        elif cash.lower() in ["-c","-cash","cash","c"]:
            embed = discord.Embed(title="Economy cash leaderboard", description="List of peoples' money in the economy in order of cash balance", color=0xe31313)
            for i,member in enumerate(sorted(self.economy.items(),key=lambda e:e[1]["cash"],reverse=True)):
                embed.add_field(name=str(i+1)+". "+member[1]["lastname"],value="Cash: "+str(member[1]["cash"])+" | Bank: "+str(member[1]["bank"]),inline=False)
        else: await ctx.send(f"Invalid parameter '{cash}', {ctx.author.name}"); return
        await ctx.send(embed=embed)

    @addcommand(aliases=["dep"])
    @commands.cooldown(rate=2,per=120,type=commands.BucketType.user)
    async def deposit(self,ctx,amount):
        if amount == "all":
            if self.economy[str(ctx.author.id)]["cash"] == 0: await ctx.send("You have nothing to deposit!")
            else:
                await ctx.send(f"Depositing {str(self.economy[str(ctx.author.id)]['cash'])} into the bank")
                self.economy[str(ctx.author.id)]["bank"] += self.economy[str(ctx.author.id)]["cash"]
                self.economy[str(ctx.author.id)]["cash"] = 0
                await self.economyupdate()
        else:
            try: amount = int(amount)
            except ValueError: await ctx.send(f"Invalid amount '{amount}', {ctx.author.name}")
            else:
                if self.economy[str(ctx.author.id)]["cash"] >= amount:
                    await ctx.send(f"Depositing {str(amount)} into the bank")
                    self.economy[str(ctx.author.id)]["bank"] += amount
                    self.economy[str(ctx.author.id)]["cash"] -= amount
                    await self.economyupdate()
                else: await ctx.send(f"You don't have {amount} to deposit, {ctx.author.name}")

    @addcommand(aliases=["with"])
    @commands.cooldown(rate=2,per=120,type=commands.BucketType.user)
    async def withdraw(self,ctx,amount):
        if amount == "all":
            if self.economy[str(ctx.author.id)]["bank"] == 0: await ctx.send("You have nothing to withdraw!")
            else:
                await ctx.send(f"Withdrawing {str(self.economy[str(ctx.author.id)]['bank'])} into your cash balance")
                self.economy[str(ctx.author.id)]["cash"] += int(self.economy[str(ctx.author.id)]["bank"]*0.95)
                self.economy[str(ctx.author.id)]["bank"] = 0
                await self.economyupdate()
        else:
            try: amount = int(amount)
            except ValueError: await ctx.send(f"Invalid amount '{amount}', {ctx.author.name}")
            else:
                if self.economy[str(ctx.author.id)]["bank"] >= amount:
                    await ctx.send(f"Withdrawing {str(amount)} into your cash balance")
                    self.economy[str(ctx.author.id)]["cash"] += int(amount*0.95)
                    self.economy[str(ctx.author.id)]["bank"] -= amount
                    await self.economyupdate()
                else: await ctx.send(f"You don't have {amount} to withdraw, {ctx.author.name}")

    @addcommand(aliases=["gamble","roll"])
    # @commands.cooldown(rate=2,per=120,type=commands.BucketType.user)
    async def bet(self,ctx,amount):
        try: amount = int(amount)
        except ValueError: await ctx.send(f"Invalid amount '{amount}', {ctx.author.name}")
        else:
            if self.economy[str(ctx.author.id)]["cash"] >= amount:
                if amount >= 1:
                    if randint(1,100) <= 37:
                        await ctx.send(f"{ctx.author.name}, you won! Adding {amount} to your cash balance")
                        self.economy[str(ctx.author.id)]["cash"] += amount
                        await self.economyupdate()
                    else:
                        await ctx.send(f"{ctx.author.name}, you lost... Taking {amount} from your cash balance")
                        self.economy[str(ctx.author.id)]["cash"] -= amount
                        await self.economyupdate()
                else: await ctx.send(f"You can't bet negative amounts, {ctx.author.name}!")
            else: await ctx.send(f"You don't have {amount} in your cash balance to bet, {ctx.author.name}")

    @addcommand(aliases=["steal"])
    @commands.cooldown(rate=5,per=1800,type=commands.BucketType.user)
    async def rob(self,ctx,amount,*member):
        if member != ():
            ctx.member = member; member = await self.findmemberfrom(ctx)
            if member == str(ctx.author.id): await ctx.send(f"You can't rob yourself, {ctx.author.name}!"); return
        else:
            choices = []
            for member in self.bot.get_guild(703314062360182825).members:
                if member.id != ctx.author.id and self.economy[str(member.id)]["cash"] >= amount: choices.append(str(member.id))
            if len(choices) == 0: await ctx.send(f"There are no members with a cash balance over {amount}, {ctx.author.name}")
            else: member = choice(choices)
        if type(member) == str:
            try: amount = int(amount)
            except ValueError: await ctx.send(f"Invalid amount '{amount}', {ctx.author.name}")
            else:
                if self.economy[member]["cash"] >= amount:
                    if amount >= 60:
                        if randint(1,11250) >= int(amount/self.economy[member]["cash"]*10000):
                            mode = randint(1,3)
                            if mode == 1:
                                await ctx.send(f"{ctx.author.name}, the robbery was successful! You stole exactly {amount}")
                                self.economy[str(ctx.author.id)]["cash"] += amount
                                self.economy[str(member)]["cash"] -= amount
                            elif mode == 2:
                                loss = randint(1,int(amount/5))
                                await ctx.send(f"{ctx.author.name}, the robbery was successful! However, you lost {loss} in the getaway so you ended up with {amount-loss}")
                                self.economy[str(ctx.author.id)]["cash"] += amount-loss
                                self.economy[str(member)]["cash"] -= amount
                            elif mode == 3:
                                gain = randint(1,int(amount/5))
                                await ctx.send(f"{ctx.author.name}, the robbery was successful! You even gained an extra {gain} with the spare time so you ended up with {amount+gain}")
                                self.economy[str(ctx.author.id)]["cash"] += amount+gain
                                self.economy[str(member)]["cash"] -= amount-gain
                            await self.economyupdate()
                        else:
                            loss = randint(int(amount/5),int(amount/2))
                            await ctx.send(f"{ctx.author.name}, you were caught... Taking a fine of {loss} from your cash balance")
                            self.economy[str(ctx.author.id)]["cash"] -= loss
                            await self.economyupdate()
                    else: await ctx.send(f"{amount} is too low, {ctx.author.name}! It must be above 60")
                else: await ctx.send(f"{self.bot.get_user(int(member)).name}#{self.bot.get_user(int(member)).discriminator} doesn't have {amount} in their cash balance to steal, {ctx.author.name}")

#    @addcommand(aliases=["give","donate"])
#    async def pay(self,ctx,amount,*member):

    @addcommand(aliases=["set"])
    @commands.is_owner()
    async def setvalue(self,ctx,value,key="bank",*member):
        try: value = int(value)
        except ValueError: pass
        try: 
            if member == ():
                for member in self.economy: self.economy[member][key] = value
                await self.economyupdate(); await ctx.send("Done!")
            else:
                ctx.member = member; member = await self.findmemberfrom(ctx)
                if type(member) == str:
                    self.economy[member][key] = value
                    await self.economyupdate(); await ctx.send("Done!")
        except KeyError: await ctx.send("Key Error")

    @addcommand(aliases=["add"])
    @commands.is_owner()
    async def addvalue(self,ctx,value:int,key="cash",*member):
        try:
            if member == ():
                for member in self.economy: self.economy[member][key] += value
                await self.economyupdate(); await ctx.send("Done!")
            else:
                ctx.member = member; member = await self.findmemberfrom(ctx)
                if type(member) == str:
                    self.economy[member][key] += value
                    await self.economyupdate(); await ctx.send("Done!")
        except KeyError: await ctx.send("Key Error")

    @addcommand()
    @commands.is_owner()
    async def reset(self,ctx):
        for member in self.economy: await self.adduser(int(member),False)
        await self.economyupdate(); await ctx.send("Reset balances of all members")
    
    async def findmemberfrom(self,ctx):
        if len(ctx.message.mentions) == 0:
            possiblemembers = []
            for member in self.economy:
                if " ".join(ctx.member) in self.economy[member]["lastname"]: possiblemembers.append(member)
            for member in self.bot.get_guild(703314062360182825).members:
                if (" ".join(ctx.member) in f"{member.name}#{member.discriminator}" or " ".join(ctx.member) in f"{member.nick}#{member.discriminator}") and str(member.id) not in possiblemembers:
                    possiblemembers.append(str(member.id))
            if len(possiblemembers) == 0:
                try:
                    if ctx.member[0] in self.economy: return ctx.member[0]
                    else: await ctx.send(f"Cannot find a member by ID {ctx.member[0]}, {ctx.author.name}")
                except ValueError: await ctx.send("Cannot find a member for "+" ".join(ctx.member))
            elif len(possiblemembers) == 1: return possiblemembers[0]
            else:
                print(possiblemembers)
                await ctx.send(f"Too many members that you could have meant; please be more specific, {ctx.author.name}:")
                await ctx.send(", ".join([f"{self.bot.get_user(possiblemember).name}#{self.bot.get_user(possiblemember).discriminator}" for possiblemember in possiblemembers]))
        elif len(ctx.message.mentions) == 1:
            if str(ctx.message.mentions[0].id) in self.economy: return str(ctx.message.mentions[0].id)
            else: await ctx.send(f"Member '"+str(ctx.message.mentions[0])+"' not currently registered in the economy, {ctx.author.name}")
        else: await ctx.send(f"Too many members mentioned, {ctx.author.name}!")
        
    async def ecoloop(self):
        for member in self.bot.get_guild(703314062360182825).members:
            if not member.bot and not str(member.id) in self.economy: await self.adduser(member.id,False)
        await self.economyupdate()
        await sleep((datetime.now().replace(second=0,microsecond=0)+timedelta(minutes=1)-datetime.now()).total_seconds())
        waitfor = datetime.now().replace(minute=0,second=0,microsecond=0)+timedelta(hours=1)
        while True:
            for member in self.economy:
                self.economy[member]["lastname"] = f"{self.bot.get_user(int(member)).name}#{self.bot.get_user(int(member)).discriminator}"
                self.economy[member]["cash"] += 1
            await self.economyupdate()
            await sleep((datetime.now().replace(second=0,microsecond=0)+timedelta(minutes=1)-datetime.now()).total_seconds())
            if datetime.now() > waitfor:
                for member in self.economy: self.economy[member]["bank"] *= 1.05
                self.economy[member]["bank"] -= 5
                waitfor = datetime.now().replace(minute=0,second=0,microsecond=0)+timedelta(hours=1)
    async def economyupdate(self):
        with open('economy.json','w') as jsonfile: dump(self.economy,jsonfile,indent=4)
    async def adduser(self,userid,update=True):
        self.economy[str(userid)] = {"cash":10,"bank":1440,"lastname":f"{self.bot.get_user(userid).name}#{self.bot.get_user(userid).discriminator}","allowmsg":str(datetime.now()+timedelta(seconds=30))}
        if update: await self.economyupdate()
def setup(bot): bot.add_cog(EcoCommands(bot))