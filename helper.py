import requests
from bs4 import BeautifulSoup
from pygooglenews import GoogleNews


def get_description_and_image(url):
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    metas = soup.find_all('meta')
    description = ''.join([ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ])

    images = soup.find_all(itemprop="image")
    first_image=""
    if (len(images)>1 and 'content' in images[0].attrs):
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