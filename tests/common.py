from sqlalchemy import orm

from db.conn import db_engine

dbSession = orm.scoped_session(orm.sessionmaker())
dbSession.configure(bind=db_engine)
