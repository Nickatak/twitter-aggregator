
from app.helpers import load_idols_from_json, fill_idol_data, convert_timestamp
from app.models import db, Idol, init_db, Tweet
from app.services import TwitterAPI, DiscordAPI
from config import DevConfig



class App(object):
    '''Main application class.'''

    def __init__(self):
        # Creates tables if necessary.
        init_db()
        # Fills and updates JSON data with the required fields.
        fill_idol_data()
        # Synchronizes the DB with the JSON data
        idols = load_idols_from_json()
        Idol.sync_idols(idols)

        self.idols = Idol.select()
        # Seeds tweets if they don't exist for all the idols (pulls the most recent tweet).
        self.seed_tweets()

    def seed_tweets(self):
        '''Fetches 1 tweet (their most recent) per idol IF the idol doesn't have any tweet in the DB already.
            returns:
                None
        '''

        for idol in self.idols:
            if not Idol.get(Idol.id == idol.id).tweets:
                tweet = TwitterAPI.fetch_most_recent_tweet(idol.id)

                if tweet is None:
                    raise ValueError("One of your idols doesn't have any tweets yet.")

                Tweet.create(id=tweet['id'], text=tweet['text'], created_at=tweet['created_at'], idol_id=idol.id, has_been_sent=True)

    def get_recent_tweets(self):
        '''Fetches all recent tweets for all the idols.
            returns:
                None
        '''

        for idol in self.idols:
            most_recent_db_tweet = Tweet.get_most_recent_by_idol_id(idol.id)
            new_tweets = TwitterAPI.fetch_tweets(idol.id, most_recent_db_tweet.created_at)
            for tweet in new_tweets:
                if not Tweet.exists_by_id(tweet['id']):
                    Tweet.create(id=tweet['id'], created_at=tweet['created_at'], text=tweet['text'], idol_id=idol.id)

    def send_unsent_tweets(self):
        '''Sends unsent tweets to the discord webhook.'''

        # This is inefficient, I'd rather not call the DB so much, but it'll do for now.
        for idol in self.idols:
            tweets = Tweet.get_unsent_tweets_by_idol_id(idol.id)
            for tweet in tweets:
                formatted_message = '{} ({}) tweeted at {}:\n\n {}'.format(tweet.idol.name, tweet.idol.username, convert_timestamp(tweet.created_at), tweet.text)
                tweet.has_been_sent = True
                tweet.save()
                DiscordAPI.send_message(formatted_message)

    def mainloop(self):
        self.get_recent_tweets()
        self.send_unsent_tweets()

def run():
    app = App()
    app.mainloop()


