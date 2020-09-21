import discord
from discord.ext import commands
from json import load

prefixes = {"!":["Fun","fun"],"?":["General","general"],"$":["Eco","economy"],"£":["Eco","economy"],"/":["Troll","trollme"]}
class HelpCommands(commands.Cog):
    def __init__(self,bot): self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1,per=300,type=commands.BucketType.user)
    @commands.cooldown(rate=1,per=300,type=commands.BucketType.channel)
    async def help(self,ctx):
        if str(ctx.channel) == prefixes[ctx.prefix][1]:
            with open("help.json","r",encoding="utf-8") as jsonfile: cmdinfo = load(jsonfile)[prefixes[ctx.prefix][0]]
            cmds = [f"- Using the prefix {' or '.join(cmdinfo['prefixes'])}, you can use the {prefixes[ctx.prefix][0].lower()} commands ({cmdinfo['description']})"]+["\n".join([
                f"= {command} =",
                f"- Command: {cmdinfo['commands'][command]['command']}",
                f"- Aliases: {'None' if cmdinfo['commands'][command]['aliases'] == [] else ', '.join(cmdinfo['commands'][command]['aliases'])}",
                f"- Description: {cmdinfo['commands'][command]['description']}"]+[
                f"- {argument}" for argument in cmdinfo['commands'][command]['arguments']])
                for command in cmdinfo["commands"]]

            msg = ""
            for cmd in cmds:
                if len(f"{msg}\n\n{cmd}") <= 1964:
                    if cmd == cmds[-1]: await ctx.send(f"```asciidoc\n{msg}\n\n{cmd}```")
                    else: msg = f"{msg}\n\n{cmd}"
                else: await ctx.author.send(f"```asciidoc\n{msg}```"); msg = cmd
        else: await ctx.message.delete()

def setup(bot): bot.add_cog(HelpCommands(bot))