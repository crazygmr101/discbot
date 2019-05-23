
def isOfficial(member):
    return 572244343507910656 in [y.id for y in member.roles]

def isBotDev(member):
    return 579710841566265453 in [y.id for y in member.roles]
