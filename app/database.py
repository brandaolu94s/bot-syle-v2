from config import Config
from models import GuiaExame
import asyncio

e = Config()

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse
from contextlib import asynccontextmanager

# Database Configuration
DB_DRIVER = Config.DB_DRIVER
DB_SERVER = Config.DB_HOST
DB_PORT = int(Config.DB_PORT)
DB_DATABASE = Config.DB_NAME
DB_USERNAME = Config.DB_USER
DB_PASSWORD = Config.DB_PASSWORD

# Connection String with ODBC 17
CONNECTION_STRING = (
    f"DRIVER={DB_DRIVER};"
    f"SERVER={DB_SERVER},{DB_PORT};"
    f"DATABASE={DB_DATABASE};"
    f"UID={DB_USERNAME};PWD={DB_PASSWORD};"
    "Encrypt=yes;TrustServerCertificate=yes;"
)

# Async Engine and Session
DATABASE_URL = f"mssql+aioodbc:///?odbc_connect={urllib.parse.quote_plus(CONNECTION_STRING)}"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_size=10,        # Maximum number of connections
    max_overflow=5,      # Allow up to 5 extra connections if pool is full
    pool_timeout=30,     # Timeout before failing a new connection attempt
    pool_recycle=1800,   # Recycle connections every 30 minutes to prevent idle timeouts
)

# Async Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

# Context Manager for Lifespan Events
@asynccontextmanager
async def lifespan():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

from sqlalchemy.future import select
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

async def fetch_data(query: str, db: AsyncSession):
    """
    Fetch data from the database using a managed session.
    """
    async with db as session:
        try:
            result = await session.execute(text(query))
            rows = result.fetchall()
            field_names = result.keys()
            return [dict(zip(field_names, row)) for row in rows]
        except Exception as e:
            print(f"⚠️ Database query error: {e}")
            return []


async def get_pending_records(db, table_name=e.DB_TABLE, instances=e.INSTANCES, query=None):
    try:
        query = f"""
            SELECT TOP {instances} * FROM {table_name} where status_fila = 0;
        """
        data = await fetch_data(query=query, db=db)
        treated_data = [dict(item) for item in data]
        return {
            "data": treated_data,
            "status": "success",
            "message": "Records fetched successfully"
        }
    except Exception as e:
        return {
            "data": [],
            "status": "error",
            "message": str(e)
        }