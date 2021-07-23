import json
import requests

from config import config


# URL for getting users via usernames.  The maximum for doing it this way is 100 usernames in a single request. (https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by)
USERNAMES_ENDPOINT = 'https://api.twitter.com/1.1/users/lookup.json?screen_name={}'
# Base URL for getting tweets via a user's ID.  Maximum for doing it this way is 100 messages in a single request.
TIMELINE_ENDPOINT = 'https://api.twitter.com/1.1/statuses/user_timeline.json?user_id={}&trim_user=1&tweet_mode=extended'
# BASE URL for getting a singular tweet by the tweet's ID.
TWEET_ENDPOINT = 'https://api.twitter.com/1.1/statuses/show.json?id={}&tweet_mode=extended'

# App-based authentication headers for Twitter's API.
AUTH_HEADERS = {
    'Authorization' : 'Bearer {}'.format(config.TW_BEARER_TOKEN),
}


def fetch_user_data(usernames):
    '''Fetches ids and names given twitter-usernames.
            :usernames: List of usernames (strings).
        returns: 
            List of dictionaries (users).
    '''

    resp = requests.get(USERNAMES_ENDPOINT.format(','.join(usernames)), headers=AUTH_HEADERS)
    users = json.loads(resp.content.decode('utf-8'))

    return users


def fetch_most_recent_tweet(user_id):
    '''Fetches the most-recent tweet given a user's ID.
            :user_id: Integer ID of the twitter user.
        returns:
            Dictionary (a singular tweet).
    '''

    resp = requests.get(TIMELINE_ENDPOINT.format(user_id) + '&limit=1', headers=AUTH_HEADERS)
    raw_data = resp.content.decode('utf-8')
    try:
        singular_tweet = json.loads(raw_data)[0]

        return singular_tweet
    except IndexError:
        return None


def fetch_new_tweets(user_id, last_tweet_id):
    '''Fetches new tweets given a user's ID and the last-seen tweet ID.  
            :user_id: Integer ID of the twitter user.
            :last_tweet_id: ID of the most recent tweet from the last fetch.
        returns:
            List of dictionaries (tweets).
    '''

    resp = requests.get(TIMELINE_ENDPOINT.format(user_id) + '&since_id={}'.format(last_tweet_id), headers=AUTH_HEADERS)
    tweets = json.loads(resp.content.decode('utf-8'))

    return tweets