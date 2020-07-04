import discord
from discord.ext import commands, tasks

import time
import sys
import default_values

import os
from helper import help_message, get_articles,get_description_and_image


is_prod = os.environ.get('IS_HEROKU', None)
if is_prod:
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
else:
    import config
    BOT_TOKEN = config.BOT_TOKEN



bot = commands.Bot(command_prefix = '!')
bot.remove_command("help")




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
            if len(entries)<int(number_articles):
                await ctx.send("Sorry! Only {} articles were found".format(str(len(entries))))

            for entry in entries:
                description, image_url = get_description_and_image(entry.link)
                #print(entry.link)
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


bot.run(BOT_TOKEN)


