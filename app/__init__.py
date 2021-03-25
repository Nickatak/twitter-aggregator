
from models import db, Idol, init_db, Tweet

from app.helpers import load_idols_from_json
from config import DevConfig
from services import fetch_tweets


class App(object):
    def __init__(self):
        self.idols = load_idols_from_json()

        # Create tables.
        init_db()
        # synchronized the DB with the JSON data.
        if DevConfig.SYNC_DB:
            Idol.sync_idols(self.idols)

        # Seeds tweets if they don't exist for all the idols (pulls the most recent tweet).
        Tweet.seed_tweets(self.idols)

    def get_recent_tweets(self):
        '''Fetches all recent tweets for all the idols.'''
        for idol in self.idols:
            most_recent_tweet = Tweet.select().where(Tweet.idol_id == idol['id']).order_by(Tweet.tweeted_at.desc()).limit(1)[0]
            new_tweets = fetch_tweets(idol['id'], most_recent_tweet.tweeted_at)
            for tweet in new_tweets:
                print("working")
                Tweet.create(id=tweet['id'], tweeted_at=tweet['created_at'], text=tweet['text'], idol_id=idol['id'])

def run():
    app = App()
    app.get_recent_tweets()


