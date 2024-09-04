import os


def get_database_uri():
    db_host = os.getenv("DB_HOST")
    db_password = os.getenv("DB_PASSWORD")
    db_username = os.getenv("DB_USERNAME")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    return f'postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'


class Config:
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_recycle': 1800,
    }
