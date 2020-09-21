from discord.ext.commands import Command
def addcommand(name=None,cls=None,**attrs):
    if cls is None: cls = Command
    def decorator(func): return cls(func,name=name,ignore_extra=False,**attrs)
    return decorator