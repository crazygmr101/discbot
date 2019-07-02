# Work with Python 3.6
from discord import *
from discord.ext import commands
import random
import pytz
import sqlite3
from datetime import datetime
import requests
import os

# user-defined .py files
# these are part of UWU Bot
from timezones import *
from misc import *
from mixer import *
from diag import *
from wiki import *
from help import *
from experience import *
from mth import *
from roles import *
from moderation import *
from mojang import mjcommand
from hypixelapi import hypxl
from game import start_game

TOKEN = 'NTc4OTk5Mzc1NjQ1MTE0MzY5.XN8Qog.m4pR2QgevWel2_Q9PRHWwESiSos' # UWU Bot's API Token

BOT_PREFIX = ("uwu", "!")
client = discord.Client()
bot = commands.Bot(command_prefix='uwu ')
pre = "uwu"

bot.remove_command('help')

@bot.command()
async def hp(ctx, sub, a1=None, a2=None, a3=None, a4=None, a5=None):
    await hypxl(ctx)

@bot.command()
async def help(ctx):
    await print_help(ctx)

@bot.command()
async def game(ctx):
    if isBotDev(ctx.author):
        await start_game(ctx,client,bot)

@bot.command()
async def restart(ctx):
    if isBotDev(ctx.author) or isOfficial(ctx.author):
        await ctx.send("UWU Bot Restarting")
        os.execl('/home/bot/restart','/home/bot/restart')
    else:
        await ctx.send("You're not allowed to do that")

@bot.command()
async def mod(ctx):
    if isBotDev(ctx.author) or isOfficial(ctx.author):
        await moderate(ctx,bot)

@bot.command()
async def mixer(ctx, a):
    await ctx.send(embed=membed(a))

@bot.command()
async def mojang(ctx):
    await mjcommand(ctx)

@bot.command()
async def wikif(ctx, a):
    await wlu(ctx, a)

@bot.command()
async def wiki(ctx, a):
    await wsm(ctx, a)

@bot.command()
async def pusheen(ctx):
    await ctx.send("<:pusheenblob:575691433520922674>")

@bot.command()
async def dab(ctx):
    await ctx.send("<o/")

@bot.command()
async def cookie(ctx):
    await ctx.send("You don't need a cookie, " + ctx.author.mention)

@bot.command()
async def drink(ctx):
    msgs = 'pepsi,orange juice,mud,lava,coke,tea,milk,water,oil'.split(',')
    msg = '*gives ' + random.choice(msgs) + ' to {0.author.mention}*'
    msg = msg.format(ctx)
    await ctx.send(msg)

@bot.command()
async def level(ctx):
    await glevel(ctx)

@bot.command()
async def leaderboard(ctx):
    await leader(ctx)

@bot.command()
async def m(ctx):
    await mthf(ctx)

@bot.command()
async def hello(ctx):
    await ctx.send('Hello {0.author.mention}'.format(ctx.message))

@bot.command()
async def cake(ctx):
    if random.randint(1,5) == 1:
        msg = 'nah, {0.author.mention}'.format(ctx.message)
    else:
        msg = '*gives :cake: to {0.author.mention}*'.format(ctx.message)
    await ctx.send(msg)

@bot.command()
async def givecake(ctx, user):
    await ctx.send('*takes :cake: from {0.author.mention} and gives it to {1}*'.format(ctx.message, user))

@bot.command()
async def hug(ctx, user):
    await ctx.send('*{0.author.mention} hugs {1}*'.format(ctx, user))

@bot.command()
async def lemon(ctx):
    await ctx.send('here\'s a :lemon: , {0.author.mention}'.format(ctx))

#i enjoy spaghetti

@bot.command()
async def hem(ctx,amt=1):
    try:
        int(amt)
        resp = "{0.author.mention}, here\'s {1} <:yarn:595037192200388621> ".format(ctx,amt)
    except:
        resp = "how much yarn do you want?"
    finally:
        await ctx.send(resp)

@bot.command()
async def time(ctx):
    await ctx.send(tlu(ctx.message.mentions[0]))

@bot.command()
async def timezone(ctx, timezone):
    tzadd(ctx.message.author, timezone)

@bot.command()
async def mtz(ctx, id, timezone):
    if isOfficial(ctx.author):
        tzset(id, timezone)

@bot.command()
async def uc(ctx):
    if isOfficial(ctx.author):
        await brodcast(ctx, True, bot)

@bot.command()
async def bc(ctx):
    if isOfficial(ctx.author):
        await brodcast(ctx, False, bot)

@bot.command()
async def diag(ctx):
    if isBotDev(ctx.author) or isOfficial(ctx.author):
        await ctx.send(embed=get_diag())
    else:
        await ctx.send("You're not allowed to do that")

async def on_msg(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    m = message.content.split(" ")

    if (message.channel.id==570393863559315458 or \
        message.channel.id==579140367207628820 or \
    message.channel.id==588410804534116405) and \
        message.author.bot == False and m[0] != "uwu":
        #message.author.id != "267499094090579970":
        await gainxp(message,bot)

    if "owo" in message.content.split(" "):
        await message.channel.send("..o-owo? I thought you were uwu... :cry:")

bot.add_listener(on_msg, 'on_message')

@bot.event
async def on_member_join(member):
    ch = bot.get_guild(570393863559315456).get_channel(579116179646447626)
    embed = discord.Embed(title= '**Welcome to the UWU\'s R Us discord server, {0}!**'.format(member.name), \
                          url="https://cdn.discordapp.com/attachments/570393863559315458/579812965407129666/Uwu_2.jpg", \
                          color=0x8888ff)
    embed.add_field(name="Roles",value='If you don\'t have the `@hypixeluwu` role yet, ping a `@hypixel officer` and they\'ll make sure you\'re in the guild and give you the role!')
    embed.add_field(name="Rules",value=("Make sure to look at #rules, and most of all have fun, "+ member.mention + '!'))
    embed.add_field(name="OH yeah..",value='And it might be a good idea to mute #botspam, #mod-logging, and #muwusic-control')
    embed.set_image(url="https://cdn.discordapp.com/attachments/570393863559315458/579812965407129666/Uwu_2.jpg")
    await ch.send(embed=embed)
    await ch.send(member.mention)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    ch = bot.get_guild(570393863559315456).get_channel(579140367207628820)
    await bot.change_presence(activity=discord.Game("How to Be UWU"),status=discord.Status.online)
    await ch.send("UWU Bot Online :computer:")

print("Discord Auth started...")
bot.run(TOKEN)
print("Discord Auth finished")
