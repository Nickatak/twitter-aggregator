# Twitter API python wrappers.

import json
import time

import requests

from config import DevConfig


class TwitterAPI(object):
    '''Container class for all Twitter-API (Standard v1.1) related methods.'''

    # URL for getting users via usernames.  The maximum for doing it this way is 100 usernames in a single request. (https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by)
    USERNAMES_ENDPOINT = 'https://api.twitter.com/1.1/users/lookup.json?screen_name={}'
    # Base URL for getting tweets via a user's ID.  Maximum for doing it this way is 100 messages in a single request.
    TIMELINE_ENDPOINT = 'https://api.twitter.com/1.1/statuses/user_timeline.json?user_id={}&trim_user=1'
    # App-based authentication headers for twitter's API.
    AUTH_HEADERS = {
        'Authorization' : 'Bearer {}'.format(DevConfig.TW_BEARER_TOKEN),
    }

    @classmethod
    def fetch_data(cls, usernames):
        '''Fetches ids and names given twitter-usernames.
                :usernames: List of usernames (strings).

            returns: 
                List of dictionaries (users).
        '''

        response = requests.get(cls.USERNAMES_ENDPOINT.format(','.join(usernames)), headers=cls.AUTH_HEADERS)
        users = json.loads(response.content.decode('utf-8'))

        return users

    @classmethod
    def fetch_tweets(cls, user_id, last_tweet_id):
        '''Fetches tweets given a user's ID.  
                :user_id: Integer ID of the twitter user.
                :last_tweet_id: ID of the most recent tweet from the last fetch.

            returns:
                List of dictionaries (tweets).
        '''

        response = requests.get(cls.TIMELINE_ENDPOINT.format(user_id) + '&since_id={}'.format(last_tweet_id), headers=cls.AUTH_HEADERS)
        tweets = json.loads(response.content.decode('utf-8'))

        return tweets

    @classmethod
    def fetch_most_recent_tweet(cls, user_id):
        '''Fetches the most-recent tweet given a user's ID.
                :user_id: Integer ID of the twitter user.

            returns:
                Dictionary (a singular tweet).
        '''

        response = requests.get(cls.TIMELINE_ENDPOINT.format(user_id) + '&limit=1', headers=cls.AUTH_HEADERS)
        raw_data = response.content.decode('utf-8')
        try:
            return json.loads(raw_data)[0]
        except IndexError:
            return []


class DiscordAPI(object):
    '''Container class for all Discord-API related methods.'''

    ORIG_WEBHOOK_URL = DevConfig.DISC_ORIG_CHANNEL_WEBHOOK_URL
    TRANS_WEBHOOK_URL = DevConfig.DISC_TRANS_CHANNEL_WEBHOOK_URL

    @classmethod
    def send_message_to_orig_channel(cls, message):
        '''Sends a message to the original (untranslated) channel.  Waits until discord responds with confirmation information for the newly created message by the webhook.
                :message: Message body (String).

            returns:
                URL to the new message (String).
        '''
        data = {
            'content' : message,
        }

        resp = requests.post(cls.ORIG_WEBHOOK_URL, data=data)
        resp.raise_for_status()

        new_message = json.loads(resp.content.decode('utf-8'))

        return cls.__create_message_link(DevConfig.DISC_SERVER_ID, new_message['channel_id'], new_message['id'])

    @classmethod
    def send_message_to_trans_channel(cls, message):
        '''Sends a message to the translation channel.  Fire-and-forget method, does not return/process anything.
            returns:
                None.
        '''
        data = {
            'content' : message,
        }

        resp = requests.post(cls.TRANS_WEBHOOK_URL, data=data)

    @classmethod
    def __create_message_link(cls, server_id, channel_id, message_id):
        return 'https://discord.com/channels/{}/{}/{}'.format(server_id, channel_id, message_id)


class MicrosoftAPI(object):
    '''Container class for all Google Trnaslate-API related methods.'''

    AUTH_HEADERS = {
        'Ocp-Apim-Subscription-Key' : DevConfig.MICROSOFT_API_KEY,
        'Ocp-Apim-Subscription-Region' : DevConfig.MICROSOFT_REGION,
        'Content-Type' : 'application/json',
    }
    TRANSLATOR_ENDPOINT = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=en'

    @classmethod
    def translate_text(cls, message):
        # Yes this is purposely a singular dict in a list.
        data = [{
            'Text' : message,
        }]

        resp = requests.post(cls.TRANSLATOR_ENDPOINT, headers=cls.AUTH_HEADERS, json=data)
        translated_text = json.loads(resp.content.decode('utf-8'))[0]['translations'][0]['text']

        return translated_text
