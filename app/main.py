from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import settings
from app.database import engine
from app.redis_client import close_redis, get_redis
from app.routes.cep import router as cep_router
from app.routes.cnpj import router as cnpj_router
from app.routes.clientes import router as clientes_router
from app.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()
    await close_redis()


app = FastAPI(title="API de Cadastro Inteligente", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(cep_router)
app.include_router(cnpj_router)
app.include_router(clientes_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "app": "cadastro-api",
        "debug": settings.debug,
    }


@app.get("/db-check")
async def db_check():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.get("/redis-check")
async def redis_check():
    r = await get_redis()
    await r.ping()
    return {"status": "ok"}
