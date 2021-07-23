import peewee as pw
import pytest

from app.errors import UserDataIntegrityError
from app.models import TwitterUser


def test_twitter_user_table_name_should_exist():
    assert TwitterUser._meta.table_name == 'twitter_users'


@pytest.mark.parametrize(
    'field_name, field_type',
    (
        ('id', pw.BigIntegerField),
        ('name', pw.CharField),
        ('screen_name', pw.CharField),
    )
)
def test_twitter_user_field_should_be_specific_type(field_name, field_type):
    assert isinstance(getattr(TwitterUser, field_name), field_type)


@pytest.mark.parametrize(
    'invalid_user, missing_field',
    (
        (
            {
                'name': 'tester123',
                'screen_name': 'tester123'
            },
            'id'
        ),
        (
            {
                'id': 20,
                'screen_name': 'tester123'
            },
            'name'
        ),
        (
            {
                'id': 20,
                'name': 'tester123'
            },
            'screen_name'
        )
    )
)
def test_twitter_user_sync_should_fail_with_bad_data(invalid_user, missing_field):
    with pytest.raises(UserDataIntegrityError) as e:
        TwitterUser.sync_users([invalid_user])
