"""Main Bot class file."""
import discord
from discord.ext import tasks
from models import db, Idol, Tweet
from config import DevConfig




class Bot(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    async def on_ready(self):
        """Discord.py API override for on_ready.  Just a sanity check to make sure my script started properly."""
        print("logged on as {0}".format(self.user))
        self.send_new_tweets.start()

    @tasks.loop(seconds=30)
    async def send_new_tweets(self):
        new_tweets = Tweet.select().where(Tweet.has_been_sent == False).order_by(Tweet.tweeted_at.desc())

        if len(new_tweets):
            for guild in self.guilds:
                for chan in guild.channels:
                    if chan.name == 'hololive-nickatak':
                        for tweet in new_tweets:
                            tweet.has_been_sent = True
                            tweet.save()
                            await chan.send("{} has tweeted: {}".format(tweet.idol.twitter_username, tweet.text))
                        self.counter += 1

def run_bot():
    bot = Bot()
    bot.run(DevConfig.DISC_TOKEN)
