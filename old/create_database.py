import aiosqlite
import datetime

DATABASE = "/home/toyhugs/gitlab/rika-bot/database_first.db"

async def create_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, money INTEGER, last_work INTEGER, PRIMARY KEY (id))")
        await db.commit()

if __name__ == "__main__":
    import asyncio
    print(datetime.datetime.now().timestamp())
    asyncio.run(create_db())
