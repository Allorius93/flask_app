BASE_TYPE = "postgresql+psycopg2"
POSTGRES_URL = "localhost:5432"
POSTGRES_USER = "postgres"
POSTGRES_PW = "12345"


class Config(object):
    POSTGRES_DB = "bookBase"
    SQLALCHEMY_DATABASE_URI = '{type}://{user}:{pw}@{url}/{db}'.format(type=BASE_TYPE ,user=POSTGRES_USER,
                                                pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # silence the deprecation warning

class TestingConfig(Config):
    POSTGRES_DB = "bookTest"
    SQLALCHEMY_DATABASE_URI = '{type}://{user}:{pw}@{url}/{db}'.format(type=BASE_TYPE ,user=POSTGRES_USER,
                                                pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)
    TESTING = True
    WTF_CSRF_ENABLED = False