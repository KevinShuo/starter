import os
import unittest
from src.models.startup.startup_db import StartupDB  # 修改为正确的导入路径
import asyncio


async def run():
    db_path = os.path.join(os.path.dirname(__file__), "db", "local.db")
    print(db_path)
    start_db = StartupDB(db_path)
    await start_db.initialize()
    await start_db.close()


if __name__ == "__main__":
    asyncio.run(run())
