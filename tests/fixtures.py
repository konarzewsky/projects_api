import pytest

from db.conn import Base
from tests import common


@pytest.fixture(autouse=True, scope="session")
def db():
    Base.metadata.drop_all(common.dbSession.bind)
    Base.metadata.create_all(common.dbSession.bind)
    try:
        yield common.dbSession
    finally:
        common.dbSession.rollback()
        common.dbSession.close()
