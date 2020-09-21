from time import time; starttime = time()
import discord
from discord.ext import commands
bot = commands.Bot(command_prefix=['/','$','£','!','?'],case_insensitive=True,activity=discord.Activity(name="Hopper's stream", type=discord.ActivityType.watching)); bot.remove_command('help')
from os import listdir
from json import load

@bot.event
async def on_ready():
    for extension in [extension for extension in listdir('./commands') if extension[-3:] == ".py" and extension != "addcommand.py"]: bot.load_extension(f'commands.{extension[:-3]}')
    print(f"Bot started in {int((time()-starttime)*1000)} milliseconds!")
@bot.event
async def on_member_join(self,member): await member.send("Welcome to the server! Read #description then enjoy!")

async def temp(ctx,text):
    if type(ctx.channel) == discord.TextChannel: await ctx.send(text,delete_after=10); await ctx.message.delete(delay=10)
    else: await ctx.send(text)
@bot.event
async def on_command_error(ctx,error):
    if hasattr(ctx.command,"on_error") and ctx.handled: pass
    else:
        if isinstance(error,commands.CheckFailure):
            if type(ctx.channel) == discord.TextChannel: await temp(ctx,f"Incorrect use of command '{ctx.command}' (you might not have permission to use it), {ctx.author.name}")
            else: await ctx.send(f"Incorrect use of command '{ctx.command}', {ctx.author.name}")
        elif isinstance(error,commands.CommandNotFound): pass
        elif isinstance(error,commands.DisabledCommand): await temp(ctx,f"'{ctx.command}' has been temperarily disabled, {ctx.author.name}")
        elif isinstance(error,commands.TooManyArguments): await temp(ctx,f"Too many arguments entered into '{ctx.command}', {ctx.author.name}")
        elif isinstance(error,commands.CommandOnCooldown): await temp(ctx,f"'{ctx.command} is on cooldown, {ctx.author.name}. It can be used {error.cooldown.rate} times per {int(error.cooldown.per)/60} minutes. There is {int(error.retry_after)} seconds left till your cooldown ends!")
        elif isinstance(error,commands.MissingRequiredArgument):
            try:
                with open("help.json","r",encoding="utf-8") as jsonfile: cmdinfo = load(jsonfile)[ctx.command.cog.qualified_name[:-8]]["commands"][str(ctx.command)]
                await ctx.send(
                    "\n".join([
                        f"You are missing required arguments for '{ctx.command}':",
                        f"```asciidoc",
                        f"= {ctx.command} =",
                        f"- Command: {cmdinfo['command']}",
                        f"- Aliases: {'None' if cmdinfo['aliases'] == [] else ', '.join(cmdinfo['aliases'])}",
                        f"- Description: {cmdinfo['description']}"]+[
                        f"- {argument}" for argument in cmdinfo['arguments']]+["```"]))
            except KeyError: await temp(ctx,f"Missing required arguments for '{ctx.command}'")
        else: raise error; await ctx.send(error)

with open('token','r') as token: token = token.readline()
bot.run(token)