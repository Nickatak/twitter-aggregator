import json
import requests

from config import config

AUTH_HEADERS = {
    'Ocp-Apim-Subscription-Key' : config.MICROSOFT_API_KEY,
    'Ocp-Apim-Subscription-Region' : config.MICROSOFT_REGION,
    'Content-Type' : 'application/json; charset=UTF-8',
}

TRANSLATOR_ENDPOINT = 'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=en'


def translate_text(message):
    # This data structure is required by their API.
    data = [{
        'Text' : message,
    }]

    resp = requests.post(TRANSLATOR_ENDPOINT, headers=AUTH_HEADERS, json=data)
    translated_text = json.loads(resp.content.decode('utf-8'))[0]['translations'][0]['text']

    return translated_text