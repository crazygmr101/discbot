import discord
from discord.ext.commands import Bot
import random
import pytz
import sqlite3
from datetime import datetime
import requests
from misc import *
import pprint

def tzadd(u, timezone):
    c = sqlite3.connect("users.db")
    cc = c.cursor()
    cc.execute("select rowid,id,timezone from timezone where id = ?", (str(u.id),))
    d = cc.fetchone()
    if d == None:
        cc.execute("insert into timezone values (?,?)", (str(u.id), timezone))
    cc.execute("update timezone set timezone=? where id=?", (timezone, u.id))
    c.commit()
    c.close()

def tzset(id, timezone):
    c = sqlite3.connect("users.db")
    cc = c.cursor()
    cc.execute("select rowid,id,timezone from timezone where id = ?", (str(id),))
    d = cc.fetchone()
    if d == None:
        cc.execute("insert into timezone values (?,?)", (str(id), timezone))
    cc.execute("update timezone set timezone=? where id=?", (timezone, str(id)))
    c.commit()
    c.close()

def tlu(u): # time zone lookup
    dict = {
     "267499094090579970":"US/Eastern", #me
     "418582992101834752":"US/Mountain", #dino
     "288525213593894915":"Etc/GMT+12", #sugar?
     "366808583024672768":"Australia/Sydney", #todo
     "267339837416275968":"Europe/Oslo", #lemon
     "473871238381699104":"Europe/Dublin", #xenia
     "419274124146245647":"Australia/Sydney", #vanessa
     "570852394393534464":"Australia/Sydney", #pebble
    }
    tz = gettz(u)
    if not (tz == None):
        t = wtc(u)
        tz = pytz.timezone(tz)
        return datetime.now(tz).strftime("It is **%X** ") + "for *" + t + "*"
    else:
        t = wtc(u)
        return "*" + t + "* doesn't have their time zone available."
    if str(u.id) in dict.keys():
        t = wtc(u)
        tz = pytz.timezone(dict[str(u.id)])
        return datetime.now(tz).strftime("It is **%X** ") + "for *" + t + "*"
    else:
        t = wtc(u)
        return "*" + t + "* doesn't have their time zone available."

def gettz(u):
    c = sqlite3.connect("users.db")
    cc = c.cursor()
    cc.execute("select rowid,id,timezone from timezone where id = ?", (str(u.id),))
    d = cc.fetchone()
    if d == None:
        return None
    c.commit()
    c.close()
    return d[2]

def wtc(u):
    if u.nick == None:
        return u.name
    else:
        return u.nick
