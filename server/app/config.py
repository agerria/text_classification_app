import os

class Config:
    db_user     = os.environ['POSTGRES_USER']
    db_password = os.environ['POSTGRES_PASSWORD']
    db_host     = os.environ['POSTGRES_HOST']
    db_port     = os.environ['POSTGRES_PORT_DOCKER']
    db_database = os.environ['POSTGRES_DB']

    SECRET_KEY  = os.environ['APP_SECRET']
    SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}'