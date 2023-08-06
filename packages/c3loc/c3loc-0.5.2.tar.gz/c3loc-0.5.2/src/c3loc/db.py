import asyncpg

from .config import CONFIG


async def init_db_pool():
    db_url = f"postgres://{CONFIG['DB_USER']}:{CONFIG['DB_PASSWORD']}@{CONFIG['DB_HOST']}/{CONFIG['DB_NAME']}"
    db_url_redacted = f"postgres://{CONFIG['DB_USER']}:*****@{CONFIG['DB_HOST']}"
    print(f"Connecting to {db_url_redacted}")
    pool = await asyncpg.create_pool(dsn=db_url, min_size=2, max_size=4)
    return pool
