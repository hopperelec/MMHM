import discord
from discord.ext import commands
from commands.addcommand import addcommand

async def temp(ctx,text):
    if type(ctx.channel) == discord.TextChannel: await ctx.send(text,delete_after=10); await ctx.message.delete(delay=10)
    else: await ctx.send(text)
class ModCommands(commands.Cog):
    def __init__(self,bot): self.bot = bot
    async def cog_check(self,ctx): return ctx.prefix in ["!","?"] and ctx.author == self.bot.get_user(348083986989449216)

    @addcommand()
    async def stop(self,ctx,cog=None):
        if cog is None:
            await temp(ctx,"Stopping bot...")
            await self.bot.logout()
        else:
            if 'commands.'+cog in self.bot.extensions:
                self.bot.unload_extension(f"commands.{cog.lower()}")
                await temp(ctx,f"Stopped cog {cog}")
            else: await temp(ctx,f"Cog {cog} not running")

    @addcommand()
    async def start(self,ctx,cog):
        if 'commands.'+cog in self.bot.extensions:
            await temp(ctx,f"Cog {cog} already running")
        else:
            self.bot.load_extension(f"commands.{cog.lower()}")
            await temp(ctx,f"Started cog {cog}")

    @addcommand()
    async def restart(self,ctx,cog):
        print(self.bot.extensions)
        if 'commands.'+cog in self.bot.extensions:
            await temp(ctx,f"Stopping cog {cog}...")
            self.bot.unload_extension(f"commands.{cog.lower()}")
        await temp(ctx,f"Starting cog {cog}...")
        self.bot.load_extension(f"commands.{cog.lower()}")
        await temp(ctx,"Done!")

    @addcommand()
    async def disable(self,ctx,command):
        if self.bot.get_command(command) != None:
            if self.bot.get_command(command).enabled == True:
                self.bot.get_command(command).enabled = False
                await temp(ctx,f"Disabled command {command}!")
            else: await temp(ctx,f"Command '{command}' already disabled")
        else: await temp(ctx,f"Command '{command}' cannot be found")

    @addcommand()
    async def enable(self,ctx,command):
        if self.bot.get_command(command) != None:
            if self.bot.get_command(command).enabled == False:
                self.bot.get_command(command).enabled = True
                await temp(ctx,"Enabled command!")
            else: await temp(ctx,f"Command '{command}' already enabled")
        else: await temp(ctx,f"Command '{command}' cannot be found")
        
    @addcommand()
    async def toggle(self,ctx,command):
        if self.bot.get_command(command) != None:
            if self.bot.get_command(command).enabled == True:
                self.bot.get_command(command).enabled = False
                await temp(ctx,"Disabled command!")
            else:
                self.bot.get_command(command).enabled = True
                await temp(ctx,"Enabled command!")
        else: await temp(ctx,f"Command '{command}' cannot be found")

    @addcommand()
    async def purge(self,ctx,count="2047"):
        if type(ctx.channel) == discord.TextChannel:
            ctx.arguments = "one [count]"
            try: await ctx.channel.purge(limit=int(count))
            except ValueError: await temp(ctx,f"Invalid count '{count}'. Must be a number!")
        else: await temp(ctx,"Command 'purge' cannot be used in privates messages")
def setup(bot): bot.add_cog(ModCommands(bot))