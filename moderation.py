import discord
from roles import *
from experience import *
from misc import *
from shutil import copyfile

async def moderate(ctx,bot):
	m = ctx.message.content.split(' ')
	if m[2] == "setxp":
		await setxp(ctx.message.mentions[0].id, int(m[4]),bot)
		embed = discord.Embed(title="XP Set",color=0xff0000)
		embed.add_field(name="User",value=get_name(ctx.message.mentions[0]))
		embed.add_field(name="XP",value=m[4])
		embed.add_field(name="Level",value=str(calclvl(int(m[4]))))
		embed.set_thumbnail(url=ctx.message.mentions[0].avatar_url)
		await ctx.send(embed=embed)
	if m[2] == "recalc":
		m.append(str(getxp(ctx.message.mentions[0].id)))
		setxp(ctx.message.mentions[0].id, getxp(ctx.message.mentions[0].id))
		embed = discord.Embed(title="Level Recalculated",color=0xff0000)
		embed.add_field(name="User",value=get_name(ctx.message.mentions[0]))
		embed.add_field(name="XP",value=m[4])
		embed.add_field(name="Level",value=str(calclvl(int(m[4]))))
		embed.set_thumbnail(url=ctx.message.mentions[0].avatar_url)
		await ctx.send(embed=embed)
	if m[2] == "remove":
		remove(ctx.message.mentions[0].id)
		embed = discord.Embed(title="User Removed from XP List",color=0xff0000)
		embed.add_field(name="User",value=get_name(ctx.message.mentions[0]))
		embed.set_thumbnail(url=ctx.message.mentions[0].avatar_url)
		await ctx.send(embed=embed)
	if m[2] == "recalc-all":
		recalc()
		embed = discord.Embed(title="Levels Recalculated",color=0xff0000)
		await ctx.send(embed=embed)
		await leader(ctx)
	if m[2] == "sanitize":
		sanitize()
	if m[2] == "userdump":
		await ctx.send(userdump())
	if m[2] == "ldb-backup":
		copyfile("users.db","users.db.b")
		await ctx.send("Done")
	if m[2] == "ldb-restore":
		copyfile("users.db.b","users.db")
		await ctx.send("Done")