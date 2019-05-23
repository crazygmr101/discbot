import psutil
import discord

def get_diag():
    embed = discord.Embed(title="UWU Bot Diagnostics",color=0xff0000)
    embed.add_field(name="CPU",value=str(psutil.cpu_percent()) + "%")
    embed.add_field(name="RAM",value=str(psutil.virtual_memory()[2]) + "%")
    return embed
