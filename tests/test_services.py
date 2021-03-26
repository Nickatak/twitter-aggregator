import requests

from app.services import DiscordAPI, TwitterAPI

class TestTwitterAPI:
    def test_api_URLs(self):
        '''Tests to make sure USERNAMES_ENDPOINT and TIMELINE_ENDPOINT both are set.'''

        assert getattr(TwitterAPI, 'USERNAMES_ENDPOINT') != None
        assert getattr(TwitterAPI, 'TIMELINE_ENDPOINT') != None

    def test_fetch_ids(self, confirmed_user):
        '''Tests to make sure the correct ID/Name pair is being pulled from twitter's API.'''
        user_data = TwitterAPI.fetch_ids([confirmed_user['username']])

        assert len(user_data) == 1

        retrieved_user = user_data[0]
        assert confirmed_user == retrieved_user
        

class TestDiscordAPI:
    def test_webhook_URL(self):
        '''Tests to make sure the WEBHOOK_URL is set.'''

        assert getattr(DiscordAPI, 'WEBHOOK_URL') != None

    def test_send_message(self):
        '''Tests sending a message (check your discord channel associated with your webhook).'''

        #DiscordAPI.send_message('Test Message from the twitter aggregator Pytest-run.')


