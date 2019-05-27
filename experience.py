import discord
from discord.ext.commands import Bot
import random
import pytz
import sqlite3
from datetime import datetime
import requests
from misc import *
import pprint
import math

def inclvl(lvl): # amount of total xp needed for a levelup
    return (lvl*lvl+150*lvl+100)*2

def calclvl(xp):
    return math.sqrt(xp/2+5525)-75

def getxp(id):
    c = sqlite3.connect("users.db")
    cc = c.cursor()
    cc.execute("select rowid,id,xp,lvl from xp where id = ?", (str(id),))
    d = cc.fetchone()
    if d == None:
        cc.execute("insert into xp values (?,?,?);",(str(id),0,0))
    cc.execute("select rowid,id,xp,lvl from xp where id = ?", (str(id),))
    c.commit()
    c.close()
    return d[2]

async def setxp(id, xp,bot):
    c = sqlite3.connect("users.db")
    cc = c.cursor()
    cc.execute("select rowid,id,xp,lvl from xp where id = ?", (str(id),))
    d = cc.fetchone()
    if d == None:
        cc.execute("insert into xp values (?,?,?);",(str(id),0,0))
    user = await bot.fetch_user(id)
    name = get_name(user)
    name = None if name==None else name
    cc.execute("update xp set xp=?, lvl=?, name=?, url=? where id=?",(xp,int(calclvl(xp)),get_name(user),str(user.avatar_url),str(id)))
    c.commit()
    c.close()
    print(d)
    await update_ldb(bot)
    await update_role(await bot.fetch_user(id),bot)

def remove(id):
    c = sqlite3.connect("users.db")
    cc = c.cursor()
    cc.execute("select rowid,id,xp,lvl from xp where id = ?", (str(id),))
    d = cc.fetchone()
    if d == None:
        cc.execute("insert into xp values (?,?,?);",(str(id),0,0))
    cc.execute("delete from xp where id=?",(str(id),))
    c.commit()
    c.close()
    print(d)

async def recalc(bot):
    da = ldb()
    for i in da:
        await setxp(int(i[0]),i[1],bot)
    await update_ldb(bot)

async def gainxp(message, bot): # function to gain xp from talking
    # id, xp, lvl
    user = message.author
    print(user.id)
    c = sqlite3.connect("users.db")
    cc = c.cursor()
    cc.execute("select rowid,id,xp,lvl from xp where id = ?", (str(user.id),))
    d = cc.fetchone()
    if d == None:
        cc.execute("insert into xp values (?,?,?,?,?);",(str(user.id),0,0,get_name(user),str(user.avatar_url)))
    else:
        row = d[0]
        id = d[1]
        xp = d[2]
        lvl = d[3]
        xp += random.randint(0,7)
        if xp >= inclvl(lvl+1):
            lvl += 1
            t = get_name(user)
            embed = discord.Embed(title=(t+" has leveled up!"), color=user.color)
            embed.add_field(name="Level",value=str(lvl))
            embed.set_thumbnail(url=user.avatar_url)
            await message.guild.get_channel(579456831328616473).send(embed=embed)
        cc.execute("update xp set xp=?, lvl=? where id=?",(xp,lvl,id))
    c.commit()
    c.close()
    await update_ldb(bot)
    await update_role(message.author, bot)
    print(d)


async def glevel(ctx):
    c = sqlite3.connect("users.db")
    cc = c.cursor()
    if len(ctx.message.mentions) > 0:
        a = ctx.message.mentions[0]
    else:
        a = ctx.author
    d = cc.execute("select rowid,id,xp,lvl from xp where id = ?", (a.id,)).fetchone()
    if d == None:
        cc.execute("insert into xp values (?,?,?);",(str(a.id),0,0))
        d = cc.execute("select rowid,id,xp,lvl from xp where id = ?", (a.id,)).fetchone()
    row = d[0]
    id = d[1]
    xp = d[2]
    lvl = d[3]
    t = get_name(a)
    embed = discord.Embed(title=(t+"'s Level"), color=a.color)
    embed.add_field(name="Experience",value=str(xp) + " UwuXP")
    embed.add_field(name="Level",value=str(lvl))
    embed.add_field(name="Next Level up",value=str(inclvl(lvl+1)) + " UwuXP")
    embed.set_thumbnail(url=a.avatar_url)
    await ctx.send(embed=embed)
    c.commit()
    c.close()

def ldb():
    c = sqlite3.connect("users.db")
    cc = c.cursor()
    da = cc.execute("select id,xp,lvl,name,url from xp where id is not ?",(".267499094090579970",)).fetchall()
    da.sort(key=lkey, reverse=True)
    return da

def lkey(val):
    return val[1]

# id's for roles
BRONZE = 578233845397323777 #1 5-7
SILVER = 578233976351883264 #2 8-11
GOLD = 578233930201956362 #3 12-15
DIAMOND = 578234017875230731 #4 16-19
PLATINUM = 578234065874976789 #5 20-23
EMERALD = 578235010503671808 #6 24+

def getRole(xp):
    l = calclvl(xp)
    if l >= 24:
        return 6
    if l >= 20:
        return 5
    if l >= 16:
        return 4
    if l >= 12:
        return 3
    if l >= 8:
        return 2
    if l >= 5:
        return 1
    return 0

async def update_role(user, bot):
    pass

async def update_ldb(bot):
    da = ldb()
    g = bot.get_guild(570393863559315456)
    s = "```Rnk  Lvl  Name\n" + \
        "--------------------------------------------------\n"
    r = 1
    for i in da:
        try:
            u = g.get_member(int(i[0]))
            xp = i[1]
            lvl = i[2]
            s += str(r) + '\t' + str(lvl) + '\t' + get_name(u) + ' (' + str(xp) + ' UwuXP)\n'
            r += 1
        except:
            pass
    s += "```"
    await (await g.get_channel(581278386522030115).fetch_message(581284105866706965)).edit(content=s)


def sanitize():
    c = sqlite3.connect("users.db")
    cc = c.cursor()
    da = cc.execute("select id,xp,lvl,name,url from xp where id is not ?",(".267499094090579970",)).fetchall()
    for i in da:
        try:
            if len(a) < 15:
                raise Exception
            a = int(i[0])
        except:
            cc.execute("delete from xp where id = ?",(i[0],))
    c.commit()
    c.close()

async def leader(ctx):
    da = ldb()
    fields = ["Emerald","Platinum","Diamond","Gold","Silver","Bronze","None"]
    vals = ["","","","","","",""]
    r = 1
    for i in da:
        try:
            u = ctx.author.guild.get_member(int(i[0]))
            xp = i[1]
            lvl = i[2]
            vals[6 - getRole(xp)] += str(r).ljust(3) + "Lvl " + str(lvl).ljust(3) + str(xp).rjust(6) + ' UwuXP  ' + get_name(u) + '\n'
            r += 1
        except:
            pass
    r = discord.Embed(title="Leaderboard")
    for i in range(7):
        if vals[i].rstrip() != "":
            r.add_field(name=fields[i],value="```"+vals[i].rstrip()+"```")
    r.add_field(name="Go here for the prettier leaderboard, and to see how ranking works!",value="http://34.73.78.74/index.html")
    await ctx.send(embed=r)

def userdump():
    da = ldb()
    s = "```\n"
    for i in da:
        s += pprint.pformat(i) + "\n"
    return s + "```"
