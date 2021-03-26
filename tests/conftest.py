import sys, os

import pytest

sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))


@pytest.fixture
def confirmed_user():
    '''This fixture is manually validated data.'''

    return {
            'username' : 'nickatak',
            'name' : 'Nickatak',
            'id' : 1319269425522958336,
    }