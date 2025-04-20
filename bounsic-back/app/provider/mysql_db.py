from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

class DatabaseFacade:
    def __init__(self, config_path="env/.env.dev"):
        self._load_config(config_path)
        self._create_engine()

    def _load_config(self, config_path):
        dotenv_path = Path(__file__).resolve().parent.parent.parent / config_path
        load_dotenv(dotenv_path=dotenv_path)

        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("PORT_DB", 3306))
        self.database = os.getenv("DB_NAME")

    def _create_engine(self):
        url = f"mysql+asyncmy://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.engine = create_async_engine(url, pool_size=10, echo=False)
        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_session(self) -> AsyncSession:
        async with self.AsyncSessionLocal() as session:
            yield session


    async def execute_query(self, query: str, params=None):
        async for session in self.get_session():
            try:
                stmt = text(query)

                if isinstance(params, dict) or isinstance(params, (list, tuple)):
                    result: Result = await session.execute(stmt, params)
                elif params is None:
                    result: Result = await session.execute(stmt)
                else:
                    raise ValueError("Params must be a dict, list, tuple, or None")

                try:
                    # Intentamos hacer fetchall() para detectar si es SELECT
                    rows = result.fetchall()
                    return [dict(row._mapping) for row in rows]
                except Exception:
                    # Si no es SELECT, se hace commit y se devuelve info útil
                    await session.commit()
                    return {
                        "rowcount": result.rowcount,
                        "message": "Query executed successfully"
                    }

            except Exception as e:
                await session.rollback()
                print(f"Error executing query: {e}")
                raise