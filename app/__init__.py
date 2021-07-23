from app.actions.twitter import fetch_most_recent_tweet, fetch_new_tweets
from app.actions.microsoft import translate_text
from app.actions.discord import send_msg_to_orig_channel, send_msg_to_trans_channel
from app.helpers import convert_timestamp, fill_user_data
from app.models import Tweet, TwitterUser


class App(object):
    '''Main application class.'''


    def __init__(self):
        '''Loads and prefetches necessary information, initializes the tables for the DB, syncs the tracked user list, and provides a singular (most recent) tweet per tracked user.
        '''

        # Fills and updates JSON data with the required fields.
        json_users = fill_user_data()
        # Synchronizes the DB with the JSON data.
        TwitterUser.sync_users(json_users)
        self.tracked_users = TwitterUser.select()

        # Seeds tweets if they don't exist for all the idols (pulls the most recent tweet).
        self.seed_tweets()


    def seed_tweets(self):
        '''Fetches 1 tweet (their most recent) per tracked user IF the user doesn't have any tweets in the DB already.
            returns:
                None
        '''

        for user in self.tracked_users:
            if not user.tweets:
                tweet = fetch_most_recent_tweet(user.id)

                if tweet is not None:
                    Tweet.create(tweet, user, needs_to_be_sent=False)


    def get_recent_tweets(self):
        '''Fetches all recent tweets for all the tracked users and then inserts them into the DB.
            returns:
                None
        '''

        for user in self.tracked_users:
            last_saved_tweet = Tweet.get_most_recent_by_user_id(user.id)

            # This is for certain users who have their twitter empty (EG: Mana Aloe).
            if last_saved_tweet is not None:
                new_tweets = fetch_new_tweets(user.id, last_saved_tweet.id)

                for tweet in new_tweets:
                    if not Tweet.exists_by_id(tweet['id']):
                        Tweet.create(tweet, user)


    def send_unsent_tweets(self):
        '''Sends unsent tweets to the discord webhook.'''

        for user in self.tracked_users:
            tweets_to_send = Tweet.get_unsent_tweets_by_user_id(user.id)
            from app.actions.microsoft import translate_text

            for tweet in tweets_to_send:
                orig_formatted_msg = (
                    f"**{tweet.user.name} ({tweet.user.screen_name}) tweeted at {convert_timestamp(tweet.created_at)}**:"
                    f"{tweet.text}"
                )

                orig_msg_link = send_msg_to_orig_channel(orig_formatted_msg)

                trans_formatted_msg = (
                    f"**Translation of {tweet.user.screen_name}\'s tweet at {convert_timestamp(tweet.created_at)} (<{orig_msg_link}>):"
                    f"{translate_text(tweet.text)}"
                )

                send_msg_to_trans_channel(trans_formatted_msg)

                tweet.needs_to_be_sent = False
                tweet.save()


    def run(self):
        self.get_recent_tweets()
        self.send_unsent_tweets()

def create_app():
    app = App()

    return app