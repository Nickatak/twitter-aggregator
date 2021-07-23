import peewee as pw

from app.errors import UserDataIntegrityError

db = pw.SqliteDatabase('idols.db')
db.connect()


class TwitterUser(pw.Model):
    '''A wrapper class around Twitter's User model.'''

    id = pw.BigIntegerField()
    name = pw.CharField()
    screen_name = pw.CharField()


    class Meta:
        table_name = 'twitter_users'
        database = db


    @classmethod
    def sync_users(cls, users):
        '''Synchronizes the database with the tracked users.  This method removes un-tracked users from the DB.
                :users: List of dictionaries.  The dictionaries are gauranteed to have three keys: "id", "name", and "screen_name".
            returns:
                None.
        '''

        db_ids = dict((user.id, None) for user in cls.select())
        try:
            json_ids = dict((user['id'], None) for user in users)

            # Delete users that have been removed from our tracked-user list from the existing DB.
            for db_id in db_ids:
                if db_id not in json_ids:
                    cls.delete().where(cls.id == db_id).execute()
    
            # Add in any missing users to the DB.
            for user in users:
                if user['id'] not in db_ids:
                    cls.create(id=user['id'], screen_name=user['screen_name'], name=user['name'])
        except KeyError as e:
            raise UserDataIntegrityError(e.args[0])


class Tweet(pw.Model):
    '''A wrapper class around Twitter's Tweet model.'''

    id = pw.BigIntegerField()
    text = pw.CharField()
    created_at = pw.DateTimeField()
    needs_to_be_sent = pw.BooleanField(default=False)

    user = pw.ForeignKeyField(TwitterUser, backref='tweets')


    class Meta:
        table_name = 'tweets'
        database = db


    @classmethod
    def create(cls, tweet, user, needs_to_be_sent=True):
        '''Creation method override.'''

        # Unntruncate on retweets (We CANNOT depend upon the "truncated" key as it doesn't work).
        if 'retweeted_status' in tweet:
            tweet['text'] = tweet['retweeted_status']['full_text']
        else:
            tweet['text'] = tweet['full_text']

        # Filter out retweets/replies we don't want.
        if 'user_mentions' in tweet['entities']:
            # We do not want retweets of another tracked user.
            if cls._is_retweet_of_user(tweet):
                needs_to_be_sent = False

            # If it's a reply:
            if tweet.get("in_reply_to_status_id", None) is not None:
                # We do not wantreplies to another tracked user.
                if cls._is_reply_to_user(tweet):
                    needs_to_be_sent = False

        return super().create(
            id=tweet['id'],
            text=tweet['text'],
            created_at=tweet['created_at'],
            user_id=user.id,
            needs_to_be_sent=needs_to_be_sent,
        )


    @classmethod
    def _is_retweet_of_user(self, tweet):
        '''Helper method to determine whether a tweet is a retweet from another tracked user.
                :tweet: Dictionary representation of a tweet.
            returns:
                Boolean: True if it is a retweet, False if it is not.
        '''

        user_ids = dict((user.id, None) for user in TwitterUser.select(TwitterUser.id))

        for mentioned_user in tweet['entities']['user_mentions']:
            # If one of our entities is marked at the third index within the message tweet (EG: `RT @username ...` where @username starts at the third index), then we know it's a retweet.
            if mentioned_user['indices'][0] == 3 and mentioned_user['id'] in user_ids:
                return True

        return False


    @classmethod
    def _is_reply_to_user(self, tweet):
        '''Helper method to determine whether a tweet is a reply to another tracked user.
                :tweet: Dictionary representation of a tweet.
            returns:
                Boolean: True if it is a reply to another holopro member, False if it is not.
        '''

        user_ids = dict((user.id, None) for user in TwitterUser.select(TwitterUser.id))

        for mentioned_user in tweet['entities']['user_mentions']:
            # If one of our entities is marked at the zeroth index within the message tweet (EG: `@username ...` where @username starts at the zeroth index), then we know it's a reply.
            if mentioned_user['indices'][0] == 0 and mentioned_user['id'] in user_ids:
                return True

        return False


    @classmethod
    def get_most_recent_by_user_id(cls, user_id):
        '''Gets the latest tweet in the DB by a certain idol, given that idol's ID.
                :idol_id: Idol's ID (integer).
            returns:
                Tweet instance OR None.
        '''

        try:
            return cls.select().where(Tweet.user_id == user_id).order_by(Tweet.created_at.desc()).limit(1)[0]
        except IndexError:
            return None


    @classmethod
    def exists_by_id(cls, tweet_id):
        '''Determines whether or not a tweet exists in the DB already, given an ID.
                :tweet_id: Tweet's ID (integer).
        
            returns:
                Boolean (True) or None
        '''

        return cls.get_or_none(Tweet.id == tweet_id)


    @classmethod
    def get_unsent_tweets_by_user_id(cls, user_id):
        '''Gets all unsent tweets in chronological order (oldest first) by a certain idol, given that idol's ID.
                :user_id: User's ID (integer).
            returns:
                List of Tweet objects.
        '''

        return cls.select().where((Tweet.user_id == user_id) & (Tweet.needs_to_be_sent == True)).order_by(Tweet.created_at)


db.create_tables([Tweet, TwitterUser], safe=True)
