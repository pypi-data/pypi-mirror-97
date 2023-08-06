import asyncio
import pytest

from windyquery import DB


@pytest.fixture(scope="module")
def config():
    class Config:
        DB_HOST = "localhost"
        DB_PORT = "5432"
        DB_TEST = "xli"
        DB_USER = "xli"
        DB_PASS = "xliadmin"
    yield Config


@pytest.fixture(scope="module")
def db(config):
    app_db = DB()

    async def init_db():
        return await app_db.connect('db_test', {
            'host': config.DB_HOST,
            'port': config.DB_PORT,
            'database': config.DB_TEST,
            'username': config.DB_USER,
            'password': config.DB_PASS
        }, default=True)
    asyncio.get_event_loop().run_until_complete(init_db())
    yield app_db
    asyncio.get_event_loop().run_until_complete(app_db.stop())
