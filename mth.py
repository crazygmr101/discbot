import random

async def mthf(ctx):
    m = ctx.message.content.split(" ")
    if m[2] == 'roll6':
        await ctx.send(random.randint(1,6))
    if m[2] == 'roll20':
        await ctx.send(random.randint(1,20))
    if m[2] == 'roll':
        s = ''
        n = 0
        for i in range(int(m[3])):
            a = random.randint(1,int(m[4]))
            n += a
            s += str(a) + ' '
        await ctx.send(s + " TTL= " + str(n))
