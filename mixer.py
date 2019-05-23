import requests
import sys
import pprint
import discord

with open("keys/mixer.key") as file:
    MIXER = file.read()

print("Opening mixer session...")
s = requests.Session()
s.headers.update({'Client-ID': MIXER})
print("Mixer session opened")


def mlookup(user):
    return s.get('https://mixer.com/api/v1/channels/{}'.format(user)).json()

def minfo(user):
    j = mlookup(user)
    return {
        'Total Viewers':j['viewersTotal'],
        'Audience':j['audience'],
        'Followers':j['numFollowers'],
        'Bio':j['user']['bio'],
        'Level':j['user']['level'],
        'avatar_url':j['user']['avatarUrl'],
        'Online':j['online'],
        'Viewers':j['viewersCurrent'],
        'Name':j['name']
    }

def membed(user):
    j = minfo(user)
    embed = discord.Embed(title=(user+"'s Mixer"), color=0x0000ff)
    embed.add_field(name="Bio", value=j['Bio'], inline=False)
    embed.add_field(name="Latest Stream", value=j['Name'], inline=False)
    embed.add_field(name="Total Viewers", value=j['Total Viewers'])
    embed.add_field(name="Viewers", value=j['Viewers'])
    embed.add_field(name="Audience", value=j['Audience'])
    embed.add_field(name="Online", value=j['Online'])
    embed.set_thumbnail(url=j['avatar_url'])
    return embed
