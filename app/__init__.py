
from app.helpers import load_idols_from_json, fill_idol_data
from app.models import db, Idol, init_db, Tweet
from app.services import TwitterAPI
from config import DevConfig



class App(object):
    '''Main application class.'''

    def __init__(self):
        # Create tables if necessary.
        init_db()
        # Fill and update JSON data with the required fields.
        fill_idol_data()
        self.idols = load_idols_from_json()

        # synchronized the DB with the JSON data.
        if DevConfig.SYNC_DB:
            Idol.sync_idols(self.idols)

        print("done syncing")
        # Seeds tweets if they don't exist for all the idols (pulls the most recent tweet).
        self.seed_tweets()
        print("done seeding.")

    def seed_tweets(self):
        '''Fetches 1 tweet (their most recent) per idol IF the idol doesn't have any tweet in the DB already.'''

        for idol in self.idols:
            if not Idol.get(Idol.id == idol['id']).tweets:
                tweet = TwitterAPI.fetch_most_recent_tweet(idol['id'])
                print(tweet)
                print('-' * 50)
                Tweet.create(id=tweet['id'], text=tweet['text'], created_at=tweet['created_at'], idol_id=idol['id'])


    def get_recent_tweets(self):
        '''Fetches all recent tweets for all the idols.'''
        for idol in self.idols:
            most_recent_tweet = Tweet.select().where(Tweet.idol_id == idol['id']).order_by(Tweet.tweeted_at.desc()).limit(1)[0]
            new_tweets = TwitterAPI.fetch_tweets(idol['id'], most_recent_tweet.tweeted_at)
            for tweet in new_tweets:
                print("working")
                Tweet.create(id=tweet['id'], tweeted_at=tweet['created_at'], text=tweet['text'], idol_id=idol['id'])

def run():
    app = App()
    #app.get_recent_tweets()


