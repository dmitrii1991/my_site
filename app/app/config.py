import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'dfswgsrgadsgldfjkgv494rt34iorjet4gtf'
    DATABASE = {
        "host": os.environ["HOST"],
        "dbname": os.environ["DBNAME"],
        "user": os.environ["USER"],
        "password": os.environ["PASSWORD"]
                }
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}/{dbname}'.format(**DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
