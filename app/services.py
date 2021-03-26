# Twitter API python wrappers.

import json

import requests

from config import DevConfig

class TwitterAPI(object):
    '''Container class for all Twitter-API related methods.'''

    # Gets users via username.  The maximum for doing it this way is 100 usernames in a single request. (https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by)
    USERNAMES_ENDPOINT = 'https://api.twitter.com/2/users/by?usernames={}'
    # Gets tweets via a user's ID.  Maximum for doing it this way is 100 messages in a single request.
    TIMELINE_ENDPOINT = 'https://api.twitter.com/2/users/{}/tweets?tweet.fields=created_at'

    # App-based authentication headers for twitter's API.
    AUTH_HEADERS = {
        'Authorization' : 'Bearer {}'.format(DevConfig.TW_BEARER_TOKEN),
    }

    @classmethod
    def fetch_ids(cls, usernames):
        '''Fetches ids and names given twitter-usernames.
                :usernames: List of usernames (strings).

            returns: List of dictionaries (users).
        '''

        response = requests.get(cls.USERNAMES_ENDPOINT.format(','.join(usernames)), headers=cls.AUTH_HEADERS)
        users = json.loads(response.content.decode('utf-8'))['data']

        # Change id type from string to int.
        for user in users:
            user['id'] = int(user['id'])

        return users

    @classmethod
    def fetch_tweets(cls, twitter_id, end_date=None):
        '''Fetches tweets given a user's ID
                :twitter_id: Integer ID of the twitter user.
                :end_date: datetime string YYYY-MM-DD-HH:MM:SSZ (? Check this before finalizing docs).

            returns: List of dictionaries (tweets).
        '''


        if end_date is None:
            response = requests.get(cls.TIMELINE_ENDPOINT.format(twitter_id), headers=cls.AUTH_HEADERS)
        else:
            response = requests.get(cls.TIMELINE_ENDPOINT.format(twitter_id) + '&start_time={}'.format(end_date), headers=cls.AUTH_HEADERS)

        tweets = json.loads(response.content.decode('utf-8'))['data']

        return tweets


class DiscordAPI(object):
    '''Container class for all Discord-API related methods.'''

    WEBHOOK_URL = DevConfig.DISC_WEBHOOK_URL

    @classmethod
    def send_message(cls, message):
        data = {
            'content' : message,
        }
        resp = requests.post(cls.WEBHOOK_URL, data=data)
        resp.raise_for_status()
