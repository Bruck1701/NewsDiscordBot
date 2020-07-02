import discord
from discord.ext import commands, tasks
from pygooglenews import GoogleNews
from itertools import cycle
import requests
from bs4 import BeautifulSoup

import time
import config
import sys
import default_values


bot = commands.Bot(command_prefix = '!')
bot.remove_command("help")


def get_description_and_image(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    metas = soup.find_all('meta')
    description = ''.join([ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ])

    images = soup.find_all(itemprop="image")
    first_image=""
    if len(images)>1:
        first_image = images[0].attrs['content']

    return description,first_image


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
    #fetch_headline.start()

@bot.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(bot.latency*1000)} ms')

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        colour= discord.Color.blue(),
        title = "Help",
        description = "Available functions"
    )
    
    embed.add_field(name="!ping", value="The bot answers with his latency", inline=False)
    embed.add_field(name="!news <2-letter-language> <2-letter-country> <number_of articles>", value="The bot answers with number of articles of the given country in the given language ", inline=False)
    
    await ctx.send(embed=embed)


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
                description, image_url = get_description_and_image(entry.link)
                embed = discord.Embed(
                    colour= discord.Color.blue(),
                    title=entry.title,
                    url=entry.link,
                    description= description
                )
                if len(image_url)>0:
                    embed.set_image(url=image_url)

                await ctx.send(embed=embed)          


@tasks.loop(hours=6)
async def fetch_headline():
  
    await bot.wait_until_ready()
    channel = bot.get_channel(id=int(config.CHANNEL_ID))

    if channel != None:

        entries = get_articles(default_values.LANGUAGE,default_values.COUNTRY,default_values.NUMBER)
        for entry in entries:
            await channel.send(entry.link)


bot.run(config.BOT_TOKEN)


