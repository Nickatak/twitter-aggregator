import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def valid_users():
    return (
        {
            'id': 880317891249188864,
            'name': '\u3068\u304d\u306e\u305d\u3089\ud83d\udc3b\ud83d\udcbf3/24\u30e9\u30a4\u30d6BD\u767a\u58f2\uff01',
            'screen_name': 'tokino_sora',
        },
        {
            'id': 880317891249188864,
            'name': '\u3068\u304d\u306e\u305d\u3089\ud83d\udc3b\ud83d\udcbf3/24\u30e9\u30a4\u30d6BD\u767a\u58f2\uff01',
            'screen_name': 'tokino_sora',
        },
        {
            'id': 880317891249188864,
            'name': '\u3068\u304d\u306e\u305d\u3089\ud83d\udc3b\ud83d\udcbf3/24\u30e9\u30a4\u30d6BD\u767a\u58f2\uff01',
            'screen_name': 'tokino_sora',
        },
    )
