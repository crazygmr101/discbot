import wikipedia
import discord

def wikibed(query):
    try:
        pg = wikipedia.page(query)
    except Exception as e:
        embed = discord.Embed(title=query,color=0x000000)
        embed.add_field(name="Topic too broad",value="Your topic matched more than one page. Try narrowing it down")
        return embed
    embed = discord.Embed(title=pg.title,color=0xffffff)
    r = pg.content if len(pg.content) < 1000 else (pg.content[0:998] + "...")
    embed.add_field(name="Content",value=r)
    return embed

async def wlu(ctx, query): #full result
    await ctx.send(embed=wikibed(query))

async def wsm(ctx, query): #summary
    await ctx.send(embed=wikisum(query))

def wikisum(query):
    try:
        pg = wikipedia.summary(query,sentences=2)
    except Exception as e:
        embed = discord.Embed(title=query,color=0x000000)
        embed.add_field(name="Topic too broad",value="Your topic matched more than one page. Try narrowing it down")
        return embed
    embed = discord.Embed(title=query,color=0xffffff)
    embed.add_field(name="Content",value=pg)
    embed.add_field(name="This is a summary",value="For a full result do `uwu wikif {term}`")
    return embed
