# Miscellaneous helpers
import json

from services import fetch_ids


def load_idols_from_json():
    # Loads idols from JSON and fetches all associated twitter_ids.
    with open('idols.json', 'r') as fo:
        data = json.loads(fo.read())

    # Tag the id's onto each idol object.
    idols = fetch_ids(idol['username'] for idol in data)
    # Convert ids to integers.
    for idol in idols:
        idol['id'] = int(idol['id'])

    with open('idols.json', 'w') as fo:
        fo.write(json.dumps(idols, indent=4))

    return idols
