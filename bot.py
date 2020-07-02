import discord
from discord.ext import commands, tasks
from pygooglenews import GoogleNews
from itertools import cycle
import time

import config


bot = commands.Bot(command_prefix = '!')

def help_message():
    return "To get the latest news, you should write \"!news <2 letter-code language> <2 letter-code country> <how many articles>\""

def get_articles(lang,country,number_articles):
    gn = GoogleNews(lang.lower(),country.upper())
    gn.BASE_URL = gn.BASE_URL+"?hl={}&gl={}".format(gn.lang,gn.country)
    top_news = gn.top_news()
    entries = top_news["entries"]

    if number_articles < len(entries):
        entries = entries[:number_articles]

    return entries


@bot.event
async def on_ready():
    print('Bot is ready!')
    fetch_headline.start()


@bot.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(bot.latency*1000)} ms')


@bot.command(aliases=['getnews','getNews'])
async def news(ctx, *, params=None):
    if params==None:
        await ctx.send(help_message())
    else:
        params = params.split(' ')        
        if len(params)<3:
            await ctx.send(help_message)
        else:
            await ctx.send("Fetching the latest news.")
            lang , country, number_articles = params
                        
            entries = get_articles(lang,country,int(number_articles))
            for entry in entries:
                await ctx.send(entry.link)          


@tasks.loop(hours=6)
async def fetch_headline():
    
    await bot.wait_until_ready()
    channel = bot.get_channel(id=int(config.CHANNEL_ID))

    if channel != None:

        entries = get_articles(config.LANGUAGE,config.COUNTRY,config.NUMBER)
        for entry in entries:
            await channel.send(entry.link)


bot.run(config.BOT_TOKEN)


