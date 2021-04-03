import peewee as pw
from config import DevConfig
from app.services import TwitterAPI

db = pw.SqliteDatabase('idols.db')
db.connect()

'''CURRENTLY UNDER REWRITE 4/3/2021
'''

class TwitterUser(pw.Model):
    '''Columns have been changed to match Twitter's v1.1 API.  To be consistent across the application, this model has been named TwitterUser, since all Holopro members that we're tracking are indeed twitter users.  Throughout the comments, this model will be referred to as a "tracked user" or "tracked users."
    '''
    # This should work, seeing how ID's are unsigned 64-bit integers.
    id = pw.BigIntegerField()
    screen_name = pw.CharField()
    name = pw.CharField()

    class Meta:
        table_name = 'twitter_users'
        database = db

    @classmethod
    def sync_users(cls, users):
        '''Synchronizes the database with the tracked users (idols.json).
                :users: List of dictionaries.  The dictionaries are gauranteed to have three keys: "id", "name", and "screen_name".

            returns:
                None.

            REWRITE COMPLETE 4/3/2021.                
        '''


        # This method will sync the DB to the current idols.json information (WARNING: it will remove any idols that exist within the DB but aren't in the JSON file).
        db_users = cls.select()

        # Take advantage of hash map lookup speed.
        db_ids = dict((user.id, None) for user in db_users)
        json_ids = dict((user['id'], None) for user in users)

        # Prune users that have been removed from our tracked-user list from the existing DB:
        for db_id in db_ids:
            if db_id not in json_ids:
                cls.delete().where(cls.id == db_twitter_id)

        # Add in any missing idols to the DB:
        for user in users:
            if user['id'] not in db_ids:
                cls.create(id=user['id'], screen_name=user['screen_name'], name=user['name'])


class Tweet(pw.Model):
    id = pw.BigIntegerField()
    text = pw.CharField()
    created_at = pw.DateTimeField()
    needs_to_be_sent = pw.BooleanField(default=False)

    user = pw.ForeignKeyField(TwitterUser, backref='tweets')

    class Meta:
        table_name = 'tweets'
        database = db

    @classmethod
    def is_hp_retweet(cls, holopro_users, tweet):
        '''Determines whether or not a tweet is a retweet of another Holopro member (tracked user).
                :holopro_users: A list of User objects from the DB.
                :tweet: Dictionary representation of a tweet.

            returns:
                Boolean: True if it is a retweet, False if it is not.

            REWRITE COMPLETE 4/3/2021
        '''
        # If there's no mentions, then it CANNOT be a retweet/reply .
        if 'user_mentions' not in tweet['entities']:
            return False

        user_ids = dict((user.id, None) for user in holopro_users))
        tweet_text = tweet['text']

        for mentioned_user in tweet['entities']['user_mentions']:
            # If one of our entities is marked at the third index within the message tweet (EG: `RT @username ...` where @username starts at the third index), then we know it's a retweet.
            if mentioned_user['indices'][0] == 3 and mentioned_user['id'] in user_ids:
                return True

        return False
                    
    @classmethod
    def is_hp_reply(cls, holopro_users, tweet):
        '''Determines whether or not a tweet is a reply TO another Holopro member (tracked user).
                :holopro_users: A list of User objects from the DB.
                :tweet_text: String content of the tweet.

            returns:
                Boolean: True if it is a reply to another holopro member, False if it is not.

            REWRITE COMPLETE 4/3/2021
        '''

        # If there's no mentions, then it CANNOT be a retweet/reply .
        if 'user_mentions' not in tweet['entities']:
            return False

        user_ids = dict((user.id, None) for user in holopro_users))
        tweet_text = tweet['text']

        for mentioned_user in tweet['entities']['user_mentions']:
            # If one of our entities is marked at the zeroth index within the message tweet (EG: `@username ...` where @username starts at the zeroth index), then we know it's a reply.
            if mentioned_user['indices'][0] == 0 and mentioned_user['id'] in user_ids:
                return True

        return False


    @classmethod
    def exists_by_id(cls, tweet_id):
        '''Determines whether or not a tweet exists in the DB already, given an ID.
                :tweet_id: Tweet's ID (integer).
        
            returns:
                Boolean (True) or None
        '''

        return cls.get_or_none(Tweet.id == tweet_id)

    @classmethod
    def get_most_recent_by_user_id(cls, user_id):
        '''Gets the latest tweet in the DB by a certain idol, given that idol's ID.
                :idol_id: Idol's ID (integer).
            returns:
                Tweet instance OR None.

            REWRITE COMPLETE 4/3/2021
        '''
        try:
            return cls.select().where(Tweet.user_id == user_id).order_by(Tweet.created_at.desc()).limit(1)[0]
        except IndexError:
            return None

    @classmethod
    def get_unsent_tweets_by_idol_id(cls, idol_id):
        '''Gets all unsent tweets in chronological order (oldest first) by a certain idol, given that idol's ID.
                :idol_id: Idol's ID (integer).
            returns:
                List of Tweet objects.
        '''

        return cls.select().where((Tweet.idol_id == idol_id) & (Tweet.needs_to_be_sent == True)).order_by(Tweet.created_at)


def create_tables():
    # Initializes the tables.
    ALL_TABLES = (TwitterUser, Tweet)
    db.create_tables(ALL_TABLES)