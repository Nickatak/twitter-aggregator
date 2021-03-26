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
                cls.create(id=idol['id'], twitter_username=idol['username'])

class Tweet(pw.Model):
    id = pw.BigIntegerField()
    created_at = pw.DateTimeField()
    text = pw.CharField()
    has_been_sent = pw.BooleanField(default=False)

    idol = pw.ForeignKeyField(Idol, backref='tweets')

    class Meta:
        table_name = 'tweets'
        database = db

    @classmethod
    def get_latest_by_idol_id(cls, idol_id):
        '''Fetches the latest tweet in the DB by a certain idol, given that idol's ID.
                :idol_id: Idol's ID (integer).
            returns:
                Tweet instance OR None.
        '''
        return cls.select().where(cls.idol_id == idol_id).order_by(cls.created_at.desc())

    @classmethod
    def seed_tweets(cls, idols):
        # Populates the DB with one tweet per idol.
        for idol in idols:
            if Tweet.get_or_none(cls.idol_id == idol['id']) is None:
                latest_tweet = TwitterAPI.fetch_tweets(idol['id'])
                #I've marked them as has_been_sent already so we don't flood discord on initial run.
                Tweet.create(id=latest_tweet['id'], tweeted_at=latest_tweet['created_at'], text=latest_tweet['text'], idol_id=idol['id'], has_been_sent=True)



def init_db():
    # Initializes the tables.
    ALL_TABLES = (Idol, Tweet)

    if DevConfig.DROP_DB:
        db.drop_tables(DROP_DB)

    db.create_tables(ALL_TABLES)