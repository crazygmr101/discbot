import random

context = None
client = None
bot = None

async def start_game(ctx,c,b):
    global context
    context = ctx
    global client
    client = c
    global bot
    bot = b
    await say("test")
    await say((await get_input()).content)
    await say((await get_input_m(["yes"])).content)

async def get_input():
    global context
    global client
    global bot
    channel = context.channel
    m = await bot.wait_for('message',check=lambda message:message.channel == channel)
    print(m)
    return m

async def get_input_m(match):
    global context
    global client
    global bot
    channel = context.channel
    m = await bot.wait_for('message',check=lambda message:message.channel == channel and message.content in match)
    print(m)
    return m


async def say(msg):
    await context.send(msg)
