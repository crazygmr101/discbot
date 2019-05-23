import discord
import requests
import json

emoji = {
	"green":":white_check_mark:",
	"yellow":":exclamation:",
	"red":"x:"
}

async def mjcommand(ctx):
	m = ctx.message.content.split(" ")
	if m[2] == "status":
		await ctx.send(mojang_status())
	if m[2] == "uuid":
		try:
			await ctx.send("UUID of " + m[3] + " is " + uuid(m[3]))
		except:
			await ctx.send("UUID of " + m[3] + " cannot be found")

def mojang_status():
	d = requests.get("https://status.mojang.com/check").json()
	s = ""
	for i in d:
		for k in i:
			s += emoji[i[k]] + k + "\n"
	return s

def uuid(s):
	d = requests.get("https://api.mojang.com/users/profiles/minecraft/" + s).json()
	return d["id"]