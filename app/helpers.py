from datetime import datetime, timezone, timedelta
import json

from app.actions.twitter import fetch_user_data
from config import config


def read_json():
    '''Reads JSON from the configured JSON_INPUT_FILE path.'''
    with open(config.JSON_INPUT_FILE, 'r') as fo:
        data = json.loads(fo.read())

    return data

def write_json(content):
    '''Writes JSON from the configured JSON_OUTPUT_FILE path.'''
    with open(config.JSON_OUTPUT_FILE, 'w') as fo:
        fo.write(json.dumps(content, indent=4))

def fill_user_data():
    '''Helper function to fill-in user data in the JSON file.  This also writes the acquired user data to the output file specified in the config.
        returns:
            List of dictionaries (Twitter users).
    '''

    data = read_json()
    users = fetch_user_data([user['screen_name'] for user in data])
    write_json(users)

    return users

def convert_timestamp(timestamp):
    '''Helper function to convert a non-aware timestamp to a human-readable timestamp (JST: UTC+9).  
            :timestamp: Timestamp directly from twitter's api.  Example timestamp: `Sat Apr 03 20:58:00 +0000 2021`
            
        returns:
            Human readable string representation of timestamp.
    '''
    dt = datetime.strptime(timestamp, '%a %b %d %H:%M:%S %z %Y') + timedelta(hours=9)

    return dt.strftime('%b %d at %H:%M JST')