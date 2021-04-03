
from app.helpers import fill_user_data, convert_timestamp
from app.models import create_tables, db, Tweet, TwitterUser
from app.services import TwitterAPI, DiscordAPI, MicrosoftAPI
from config import DevConfig


class App(object):
    '''Main application class.'''

    def __init__(self):
        '''Loads and prefetches necessary information, initializes the tables for the DB, syncs the tracked user list, and provides a singular (most recent) tweet per tracked user.
        '''
        # Creates tables if necessary.
        create_tables()
        # Fills and updates JSON data with the required fields.
        json_users = fill_user_data()
        # Synchronizes the DB with the JSON data.
        TwitterUser.sync_users(json_users)

        self.tracked_users = TwitterUser.select()
        # Seeds tweets if they don't exist for all the idols (pulls the most recent tweet).
        self.seed_tweets()
        print("done sseding")

    def seed_tweets(self):
        '''Fetches 1 tweet (their most recent) per tracked user IF the user doesn't have any tweets in the DB already.
            returns:
                None
        '''

        for user in self.tracked_users:
            if not user.tweets:
                tweet = TwitterAPI.fetch_most_recent_tweet(user.id)

                if tweet:
                    Tweet.create(id=tweet['id'],
                                 text=tweet['text'],
                                 created_at=tweet['created_at'],
                                 user_id=user.id,
                                 needs_to_be_sent=False)

    def get_recent_tweets(self):
        '''Fetches all recent tweets for all the tracked users.
            returns:
                None
        '''

        for user in self.tracked_users:
            last_saved_tweet = Tweet.get_most_recent_by_user_id(user.id)

            # This is for certain users who have their twitter empty (EG: Mana Aloe).
            if last_saved_tweet is not None:
                new_tweets = TwitterAPI.fetch_tweets(user.id, last_saved_tweet.id)

                for tweet in new_tweets:
                    if not Tweet.exists_by_id(tweet['id']):
                        # If it is NOT a retweet from another holopro member OR if it is a reply TO another holopro member...
                        if (not Tweet.is_hp_retweet(self.tracked_users, tweet)) or Tweet.is_hp_reply(self.tracked_users, tweet):
                            Tweet.create(
                                id=tweet['id'],
                                created_at=tweet['created_at'],
                                text=tweet['text'], 
                                user_id=user.id, 
                                needs_to_be_sent=True
                                )
                    else:
                        # Still make the tweet for recording/timestamp purposes, but it doesn't need to be sent to the channel.
                        Tweet.create(
                            id=tweet['id'],
                            created_at=tweet['created_at'],
                            text=tweet['text'], 
                            user_id=user.id,  
                            )

    def send_unsent_tweets(self):
        '''Sends unsent tweets to the discord webhook.'''

        for user in self.tracked_users:
            tweets = Tweet.get_unsent_tweets_by_user_id(user.id)
            for tweet in tweets:
                translated_text = MicrosoftAPI.translate_text(tweet.text)

                orig_formatted_message = '**{} ({}) tweeted at {}**:\n\n{}'.format(tweet.user.name, tweet.user.screen_name, convert_timestamp(tweet.created_at), tweet.text)
                orig_msg_link = DiscordAPI.send_message_to_orig_channel(orig_formatted_message)

                trans_formatted_message = '**Translation of {}\'s tweet at {} (<{}>)**:\n\n{}'.format(tweet.user.screen_name, convert_timestamp(tweet.created_at), orig_msg_link, translated_text)
                DiscordAPI.send_message_to_trans_channel(trans_formatted_message)

                tweet.needs_to_be_sent = False
                tweet.save()

    def mainloop(self):
        self.get_recent_tweets()
        self.send_unsent_tweets()

def run():
    app = App()
    app.mainloop()


