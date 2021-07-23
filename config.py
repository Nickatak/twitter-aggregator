import os
import sys

PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 3:
    import urllib.parse
else:
    import urlparse

basedir = os.path.abspath(os.path.dirname(__file__))

if os.path.exists('config.env'):
    print('Importing environment from .env file')
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")


class Config:

    NECESSARY_KEYS = (
        'DISC_ORIG_CHANNEL_WEBHOOK_URL',
        'DISC_TRANS_CHANNEL_WEBHOOK_URL',
        'JSON_INPUT_FILE',
        'JSON_OUTPUT_FILE',
        'MICROSOFT_API_KEY',
        'MICROSOFT_REGION',
        'SECRET_KEY',
        'TW_BEARER_TOKEN',
    )

    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
        print('SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION')

    if os.environ.get('TW_BEARER_TOKEN'):
        TW_BEARER_TOKEN = os.environ.get('TW_BEARER_TOKEN')
    else:
        raise ValueError("Check config.py: Need Twitter Bearer Token.")

    JSON_INPUT_FILE = os.environ.get('JSON_INPUT_FILE', 'tracked_users.json')
    JSON_OUTPUT_FILE = os.environ.get('JSON_OUTPUT_FILE', 'tracked_users.json')

    if os.environ.get('MICROSOFT_API_KEY'):
        MICROSOFT_API_KEY = os.environ.get('MICROSOFT_API_KEY')
    else: 
        raise ValueError("Check config.py: Need Microsoft API key.")

    if os.environ.get('MICROSOFT_REGION'):
        MICROSOFT_REGION = os.environ.get('MICROSOFT_REGION')
    else:
        raise ValueError("Check config.py: Need Microsoft Region.")

    DISC_SERVER_ID = os.environ.get('DISC_SERVER_ID')
    DISC_ORIG_CHANNEL_WEBHOOK_URL = os.environ.get('DISC_ORIG_CHANNEL_WEBHOOK_URL')
    DISC_TRANS_CHANNEL_WEBHOOK_URL = os.environ.get('DISC_TRANS_CHANNEL_WEBHOOK_URL')



class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite'))
    WTF_CSRF_ENABLED = False

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN TESTING MODE.  \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class ProductionConfig(Config):
    DEBUG = False
    USE_RELOADER = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'data.sqlite'))
    SSL_DISABLE = (os.environ.get('SSL_DISABLE', 'True') == 'True')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert os.environ.get('SECRET_KEY'), 'SECRET_KEY IS NOT SET!'

        flask_raygun.Provider(app, app.config['RAYGUN_APIKEY']).attach()


config_options = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

# Set exportable so we can use it throughout our application.
config = config_options[os.getenv('FLASK_CONFIG') or 'default']

