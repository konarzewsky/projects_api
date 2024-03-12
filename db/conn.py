from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.env import DB


def get_postgres_uri(db: dict) -> str:
    return f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['name']}"


DB_URI = get_postgres_uri(DB)
db_engine = create_engine(DB_URI)
db_session = sessionmaker(bind=db_engine)

Base = declarative_base()
