# News Discord Bot

This is a Google news client bot. It fetches the headlines from Google News using pygooglenews library,
parses the news into embeds and sends to a discord channel. 

# Installation instruction

To run the bot locally, I recommend installing a python virtual environment:
```
python3.x -m venv <virtual env name>
```

then install the requirements

```
pip install -r requirements.txt
```
# Execution 
the bot has currently two methods: 

to get the server response time:
```
!ping

```
to fetch the top news from Google News:
```
!new <2-letter language> <2-letter country> <number of headlines>
i.e
!news en US 10 
returns top 10 english news from the US.
```


#TO DO
Set a schedule in the bot to fetch the news every so hours, but the current version still needs to set the channel_id, the language and the country in-code to use the background task.



