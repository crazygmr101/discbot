import discord
from roles import *

async def print_help(ctx):
    message = ctx.message
    e = discord.Embed(title="UWU Bot Help")
    e.add_field(name="uwu m commands",value=\
                "`uwu m roll6` - roll a 6 sided die\n" +\
                "`uwu m roll20` - roll a 20 sided die\n" +\
                "`uwu m roll 20 6` - roll 20 6-sided dice and print total")
    e.add_field(name="uwu commands",value=\
                "`uwu mixer {player}`\n"+\
                "`uwu hug {person}`\n"+\
                "`uwu givecake {person}`\n"+\
                "`uwu cake|drink|cookie|pusheen|lemon`\n"+\
                "`uwu wiki {thing}` - wiki summary\n"+\
                "`uwu wikif {thing}` - wiki snippet\n"+\
                "`uwu level` - check your uwu level\n"+\
                "`uwu level @{user}` - check someone's uwu level\n"+\
                "`uwu leaderboard`\n"+\
                "`uwu hello`\n"+\
                "`uwu time {user}`")
    if isBotDev(ctx.author) or isOfficial(ctx.author):
        e.add_field(name="uwu bot dev commands",value=\
                    "`uwu restart` - restart uwu bot\n"+\
                    "`uwu diag` - view ram and cpu\n"+\
                    "`uwu mod userdump` - print the leaderboard database\n"+\
                    "`uwu mod sanitze` - remove all bad values from leaderboard database\n"+\
                    "`uwu mod ldb-backup|ldb-restore` - leaderboard backup/restore")
        e.add_field(name="uwu admin commands",value=\
                    "`uwu bc {message}` - brodcast a message\n"+\
                    "`uwu uc {message}` - urgent brodcast\n"+\
                    "`uwu mod setxp {user} {xp}`\n"+\
                    "`uwu mod remove {user}` - remove a user from the xp list\n"+\
                    "`uwu mod recalc {user}` - recalcs a user's xp level\n"+\
                    "`uwu mod recalc-all` - recalc all xp levels")
    await ctx.send(embed=e)
