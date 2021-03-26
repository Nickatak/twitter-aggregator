# Miscellaneous helpers.
from datetime import datetime, timezone, timedelta
import json

from app.services import TwitterAPI


def load_idols_from_json():
    '''Helper function to read in the data from idols.JSON.
        returns:
            List of dictionaries.
    '''
    with open('idols.json', 'r') as fo:
        return json.loads(fo.read())

def fill_idol_data():
    '''Helper function to fill idol data in the JSON file.
        The JSON file should consist of a list of objects, with each object having a username key at minimum.  This function reads in the JSON file, fetches all the associated data with each username key for each object, and then re-writes the JSON file with the new data.
    '''
    # Loads idols from JSON and fetches all associated twitter_ids.
    with open('idols.json', 'r') as fo:
        data = json.loads(fo.read())

    # Tag the id's onto each idol object.
    idols = TwitterAPI.fetch_ids([idol['username'] for idol in data])
    # Convert ids to integers.
    for idol in idols:
        idol['id'] = int(idol['id'])

    with open('idols.json', 'w') as fo:
        fo.write(json.dumps(idols, indent=4))

def convert_timestamp(timestamp):
    '''Helper function to convert a non-aware timestamp to a human-readable timestamp (JST: UTC+9).
        returns:
            Human readable string representation of timestamp.
    '''
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=9)

    return dt.strftime('%b %d at %H:%M JST')