import sys, os

import pytest

sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))


@pytest.fixture
def route_name():
    return 'Mattapan'

@pytest.fixture
def beg_stop():
    return 'place-cedgr'

@pytest.fixture
def end_stop():
    return 'place-valrd'

