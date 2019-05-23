import discord
from discord.ext.commands import Bot
import random
import pytz
import sqlite3
from datetime import datetime
import requests
from misc import *
import pprint



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
    if str(u.id) in dict.keys():
        if u.nick == None:
            t = u.name
        else:
            t = u.nick
        tz = pytz.timezone(dict[str(u.id)])
        return datetime.now(tz).strftime("It is **%X** ") + "for *" + t + "*"
    else:
        if u.nick == None:
            t = u.name
        else:
            t = u.nick
        return "*" + t + "* doesn't have their time zone available."
