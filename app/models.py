import peewee as pw
from config import DevConfig
from app.services import TwitterAPI

db = pw.SqliteDatabase('idols.db')
db.connect()


class Idol(pw.Model):
    # This should work, seeing how ID's are unsigned 64-bit integers.
    id = pw.BigIntegerField()
    username = pw.CharField()
    name = pw.CharField()

    class Meta:
        table_name = 'idols'
        database = db

    @classmethod
    def sync_idols(cls, idols):
        # This method will sync the DB to the current idols.json information (WARNING: it will remove any idols that exist within the DB but aren't in the JSON file).
        all_db_idols = cls.select()

        # Take advantage of hash map lookup speed.
        db_twitter_ids = dict((idol.id, None) for idol in all_db_idols)
        json_twitter_ids = dict((idol['id'], None) for idol in idols)

        # Prune removed idols from the existing DB:
        for db_twitter_id in db_twitter_ids:
            if db_twitter_id not in json_twitter_ids:
                cls.delete().where(cls.id == db_twitter_id)

        # Add in any missing idols to the DB:
        for idol in idols:
            if idol['id'] not in db_twitter_ids:
                cls.create(id=idol['id'], username=idol['username'], name=idol['name'])


class Tweet(pw.Model):
    id = pw.BigIntegerField()
    text = pw.CharField()
    created_at = pw.DateTimeField()
    has_been_sent = pw.BooleanField(default=False)

    idol = pw.ForeignKeyField(Idol, backref='tweets')

    class Meta:
        table_name = 'tweets'
        database = db

    @classmethod
    def exists_by_id(cls, tweet_id):
        '''Determines whether or not a tweet exists in the DB already, given an ID.
                :tweet_id: Tweet's ID (integer).
        
            returns:
                Boolean (True) or None
        '''

        return cls.get_or_none(Tweet.id == tweet_id)

    @classmethod
    def get_most_recent_by_idol_id(cls, idol_id):
        '''Gets the latest tweet in the DB by a certain idol, given that idol's ID.
                :idol_id: Idol's ID (integer).
            returns:
                Tweet instance OR None.
        '''

        return cls.select().where(Tweet.idol_id == idol_id).order_by(Tweet.created_at.desc()).limit(1)[0]

    @classmethod
    def get_unsent_tweets_by_idol_id(cls, idol_id):
        '''Gets all unsent tweets in chronological order (oldest first) by a certain idol, given that idol's ID.
                :idol_id: Idol's ID (integer).
            returns:
                List of Tweet objects.
        '''

        return cls.select().where((Tweet.idol_id == idol_id) & (Tweet.has_been_sent == False)).order_by(Tweet.created_at)


def init_db():
    # Initializes the tables.
    ALL_TABLES = (Idol, Tweet)

    if DevConfig.DROP_DB:
        db.drop_tables(DROP_DB)

    db.create_tables(ALL_TABLES)