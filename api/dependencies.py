from db.conn import db_session


async def get_db_conn():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


# TODO: Add auth token
