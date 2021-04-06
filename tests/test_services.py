import requests

from app.services import DiscordAPI, TwitterAPI

class TestTwitterAPI:
    def test_api_URLs(self):
        '''Tests to make sure USERNAMES_ENDPOINT and TIMELINE_ENDPOINT both are set.'''

        assert getattr(TwitterAPI, 'USERNAMES_ENDPOINT') is not None
        assert getattr(TwitterAPI, 'TIMELINE_ENDPOINT') is not None

    def test_api_bearer_token(self):
        '''Tests to make sure a bearer token has been set.'''

        assert getattr(TwitterAPI, 'AUTH_HEADERS') is not None
        assert len(TwitterAPI.AUTH_HEADERS['Authorization']) > 8

    def test_fetch_data(self, confirmed_user):
        '''Tests to make sure the correct data is being pulled from Twitter's API.'''
        user_data = TwitterAPI.fetch_data([confirmed_user['screen_name']])

        assert len(user_data) == 1

        retrieved_user = user_data[0]
        assert confirmed_user == retrieved_user

    def test_fetch_tweets(self, confirmed_user, confirmed_timeline):
        '''Tests to make sure the correct tweets are being pulled from Twitter's API.'''
        most_recent_tweet = confirmed_timeline[0]

        # If we filter by the the most recent tweet, we should get back an empty list.
        test_timeline = TwitterAPI.fetch_tweets(confirmed_user['id'], most_recent_tweet['id'])

        assert test_timeline == []

        # If we filter by the second-most recent tweet, we should get back one tweet, which should be the most recent.
        second_most_recent_tweet = confirmed_timeline[1]

        test_timeline = TwitterAPI.fetch_tweets(confirmed_user['id'], second_most_recent_tweet['id'])

        assert len(test_timeline) == 1
        # We can assure that they're the same tweet if they have the same ID.
        assert test_timeline[0]['id'] == most_recent_tweet['id']

    def test_fetch_most_recent_tweet(self, confirmed_user, confirmed_timeline, truncated_retweet_of_tracked_user):
        '''Tests to make sure the most-recent tweet is being returned from Twitter's API.'''
        test_recent = TwitterAPI.fetch_most_recent_tweet(confirmed_user['id'])

        assert isinstance(test_recent, dict)
        assert test_recent['id'] == confirmed_timeline[0]['id']

        