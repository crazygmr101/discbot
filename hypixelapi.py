import requests
from pprint import pprint, pformat
import mojang
import discord

with open("keys/hypixel.key") as file:
	key = file.read()
base = "https://api.hypixel.net/"


async def hypxl(ctx):
	args = ctx.args
	if args[1] == "player":
		await ctx.send(embed=getPlayerEmbed(args[2]))
	if args[1] == "guild":
		await ctx.send(embed=getGuildEmbed())

def getGuildEmbed():
	g = getGuild("a5f38c7337ae45e3a130d64b48e529da")
	g = g["guild"]
	embed = discord.Embed(title=g["name"])
	embed.add_field(name="Description",value=g["description"],inline=False)
	embed.add_field(name="Members",value=", ".join([getPlayer(m["uuid"])["player"]["displayname"] for m in g["members"]]))
	return embed

pcache = {}

def getPlayer(uuid):
	if uuid not in pcache.keys():
		pcache[uuid] = requests.get(base + "player?key=" + key + "&uuid=" + uuid).json()
	return pcache[uuid]

def getPlayerEmbed(user):
	uuid = mojang.uuid(user)
	p = getPlayer(uuid)['player']
	embed = discord.Embed(title=user+"'s Hypixel Profile")
	embed.set_thumbnail(url="https://minotar.net/body/" + user + "/100.png")
	embed.add_field(name="Minecraft Version",value=p['mcVersionRp'])
	embed.add_field(name="Guild",value=getGuildName(uuid))
	return embed

def getGuildID(uuid):
	return requests.get(base+"findGuild?key=" + key + "&byUuid=" + uuid).json()

def getGuildName(uuid):
	g = getGuild(uuid)
	if g == None:
		return None
	return g["guild"]["name"]

def getGuild(uuid):
	g = getGuildID(uuid)
	if g["success"]==False:
		return None
	return requests.get(base + "guild?key=" + key + "&id=" + g["guild"]).json()