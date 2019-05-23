# this file has misc functions dealing with members
import discord

def get_name(member):
    if member.nick == None:
        return member.name
    else:
        return member.nick

async def brodcast(ctx, urgent, bot):
    ch = ["570393863559315458","579787400939700248","571775329920745503", \
         "572485548392841256","571152592068018187","570681839329738772"]
    if urgent:
        ch.append("571755121269276713")
    embed = discord.Embed(title="Server Brodcast",color=0x000000 if not urgent else 0xff0000)
    embed.add_field(name="Officer",value=get_name(ctx.author))
    embed.add_field(name="Priority",value="Low" if not urgent else "High")
    embed.add_field(name="Message",value=ctx.message.content[7:],inline=False)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    for c in ch:
        x = bot.get_guild(570393863559315456).get_channel(579140367207628820)
        await x.send(embed=embed)
