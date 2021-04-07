'''Tests for app/helpers.py AND all JSON-related integrity'''
import json
from pathlib import Path

import pytest

from app.helpers import read_json, write_json
from config import DevConfig


class TestPrefetchJSON:
    '''JSON integrity tests.'''

    def test_length(self):
        '''Tests how many objects are in the JSON file.  Should have 55 idols (Last updated with OokamiMio/Achan).'''

        raw_data = read_json()

        assert len(raw_data) == 55

    def test_screen_name(self):
        '''Tests to make sure each object in the JSON file has a "screen_name" key.'''

        raw_data = read_json()

        for idol in raw_data:
            assert "screen_name" in idol


class TestHelpers:
    '''Helper function tests.'''

    ORIGINAL_INPUT_FILE = ''
    ORIGINAL_OUTPUT_FILE = ''


    @classmethod
    def setup_class(cls):
        cls.ORIGINAL_INPUT_FILE = DevConfig.JSON_INPUT_FILE
        cls.ORIGINAL_OUTPUT_FILE = DevConfig.JSON_OUTPUT_FILE

        DevConfig.JSON_INPUT_FILE = Path('.').joinpath('tests', 'testing.json')
        DevConfig.JSON_INPUT_FILE = Path('.').joinpath('tests', 'testing.json')

        test_data = [
            {"screen_name" : "nickatak"},
            {"screen_name" : "ookamimio"},
            {"screen_name" : "cocokiryu"},
        ]

        # Populate the input file with verified data.
        with open(DevConfig.JSON_INPUT_FILE, 'w') as fo:
            fo.write(json.dumps(test_data, indent=4))


    @classmethod
    def teardown_class(cls):
        DevConfig.JSON_INPUT_FILE = cls.ORIGINAL_INPUT_FILE
        DevConfig.JSON_OUTPUT_FILE = cls.ORIGINAL_OUTPUT_FILE
