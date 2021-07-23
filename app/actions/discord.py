import json
import requests

from config import config

DISC_SERVER_ID = config.DISC_SERVER_ID
ORIG_WEBHOOK_URL = config.DISC_ORIG_CHANNEL_WEBHOOK_URL
TRANS_WEBHOOK_URL = config.DISC_TRANS_CHANNEL_WEBHOOK_URL


def __create_message_link(server_id, channel_id, message_id):
    return 'https://discord.com/channels/{}/{}/{}'.format(server_id, channel_id, message_id)


def send_msg_to_orig_channel(message):
    '''Sends a message to the original (untranslated) channel.  Waits until Discord responds with confirmation information for the newly created message by the webhook.
            :message: Message body (String).
        returns:
            URL to the new message (String).
    '''

    data = {
        'content' : message,
    }

    resp = requests.post(f"{ORIG_WEBHOOK_URL}?wait=true", data=data)
    resp.raise_for_status()

    new_message = json.loads(resp.content.decode('utf-8'))

    return __create_message_link(DISC_SERVER_ID, new_message['channel_id'], new_message['id'])


def send_msg_to_trans_channel(message):
    '''Sends a message to the translation channel.  Fire-and-forget method, does not return/process anything.
        returns:
            None.
    '''

    data = {
        'content' : message,
    }

    resp = requests.post(TRANS_WEBHOOK_URL, data=data)
