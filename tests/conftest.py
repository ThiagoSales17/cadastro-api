import multiprocessing
import os
import time

import pytest
import pytest_asyncio
from httpx import AsyncClient

os.environ["DATABASE_URL"] = "postgresql+asyncpg://usuario:senha@localhost:5432/cadastro_db"
os.environ["REDIS_URL"] = "redis://localhost:6379/0"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["AUTH_USERNAME"] = "admin"
os.environ["AUTH_PASSWORD"] = "admin"

from app.auth import create_token


def _start_server():
    import uvicorn
    from app.main import app
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="warning")


@pytest.fixture(scope="session")
def server():
    proc = multiprocessing.Process(target=_start_server, daemon=True)
    proc.start()
    time.sleep(3)
    yield
    proc.kill()


@pytest_asyncio.fixture
async def client(server):
    async with AsyncClient(base_url="http://127.0.0.1:8001") as ac:
        yield ac


@pytest_asyncio.fixture
async def auth_headers():
    token = create_token("admin")
    return {"Authorization": f"Bearer {token}"}
