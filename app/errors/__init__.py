from abc import ABC


class AppBaseException(ABC, Exception):
    '''Abstract Base Exception for all of our application's errors.'''

    pass


class UserDataIntegrityError(AppBaseException):
    '''Concrete exception raised when User data does not have the required fields.'''

    def __init__(self, field):
        self.field = field

        super().__init__(self.message)


    @property
    def message(self):
        return f'User is missing the following field: {self.field}'


class TweetDataIntegrityError(AppBaseException):
    '''Concrete exception raised when Tweet data doe snot have the required fields.'''
    pass