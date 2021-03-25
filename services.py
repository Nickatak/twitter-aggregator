# Twitter API python wrappers.

import json

import requests

from config import DevConfig

def fetch_ids(usernames):
    '''This function fetches the matching twitter ID's for all the twitter usernames.'''

    # The maximum for doing it this way is 100 usernames in a single request. (https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by)
    API_ENDPOINT = 'https://api.twitter.com/2/users/by?usernames={}'.format(','.join(usernames))
    AUTH_HEADERS = {
        'Authorization' : 'Bearer {}'.format(DevConfig.TW_BEARER_TOKEN),
    }

    response = requests.get(API_ENDPOINT, headers=AUTH_HEADERS)
    return json.loads(response.content.decode('utf-8'))['data']

def fetch_tweets(twitter_id, end_date=None, pagination_token=None):
    '''This function fetches tweets off the timeline for a twitter_id.
        If you don't supply an end_date, then it only returns the first tweet of the timeline (for intiial population of the DB).
    '''

    # Returns 100 at a time max
    if end_date is None:
        API_ENDPOINT = 'https://api.twitter.com/2/users/{}/tweets?tweet.fields=created_at'.format(twitter_id)
    else:
        API_ENDPOINT= 'https://api.twitter.com/2/users/{}/tweets?tweet.fields=created_at&start_time={}'.format(twitter_id, end_date)
    AUTH_HEADERS = {
        'Authorization' : 'Bearer {}'.format(DevConfig.TW_BEARER_TOKEN),
    }

    response = requests.get(API_ENDPOINT, headers=AUTH_HEADERS)
    tweets = json.loads(response.content.decode('utf-8'))['data']

    if end_date is None:
        # just the top (most recent).
        return tweets[0]
    else:
        return tweets[:-1]


