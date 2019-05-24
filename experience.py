import discord
from discord.ext.commands import Bot
import random
import pytz
import sqlite3
from datetime import datetime
import requests
from misc import *
import pprint

def inclvl(lvl): # amount of total xp needed for a levelup
    return lvl*lvl+150*lvl+100

def calclvl(xp):
    i = 0
    while inclvl(i) < xp:
        i += 1
    return i - 1 if i > 0 else 0

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

def setxp(id, xp):
    c = sqlite3.connect("users.db")
    cc = c.cursor()
    cc.execute("select rowid,id,xp,lvl from xp where id = ?", (str(id),))
    d = cc.fetchone()
    if d == None:
        cc.execute("insert into xp values (?,?,?);",(str(id),0,0))
    cc.execute("update xp set xp=?, lvl=? where id=?",(xp,calclvl(xp),str(id)))
    c.commit()
    c.close()
    print(d)

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

def recalc():
    da = ldb()
    for i in da:
        setxp(int(i[0]),i[1])

async def gainxp(message, bot): # function to gain xp from talking
    # id, xp, lvl
    user = message.author
    print(user.id)
    c = sqlite3.connect("users.db")
    cc = c.cursor()
    cc.execute("select rowid,id,xp,lvl from xp where id = ?", (str(user.id),))
    d = cc.fetchone()
    if d == None:
        cc.execute("insert into xp values (?,?,?);",(str(user.id),0,0))
    else:
        row = d[0]
        id = d[1]
        xp = d[2]
        lvl = d[3]
        xp += random.randint(0,10)
        if xp > inclvl(lvl):
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
    da = cc.execute("select id,xp,lvl from xp where id is not ?",(".267499094090579970",)).fetchall()
    da.sort(key=lkey, reverse=True)
    return da

def lkey(val):
    return val[1]

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
    da = cc.execute("select id,xp,lvl from xp where id is not ?",(".267499094090579970",)).fetchall()
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
    s = "```Rnk  Lvl  Name\n" + \
        "--------------------------------------------------\n"
    r = 1
    for i in da:
        try:
            u = ctx.author.guild.get_member(int(i[0]))
            xp = i[1]
            lvl = i[2]
            s += str(r) + '\t' + str(lvl) + '\t' + get_name(u) + ' (' + str(xp) + ' UwuXP)\n'
            r += 1
        except:
            pass
    s += "```"
    await ctx.send(s)

def userdump():
    da = ldb()
    s = "```\n"
    for i in da:
        s += pprint.pformat(i) + "\n"
    return s + "```"