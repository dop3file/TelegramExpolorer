from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DBSession:
    def __init__(self, db_url: str, echo: bool = False) -> None:
        logger.info("Create session handler")
        self._engine = create_async_engine(
            db_url,
            echo=echo,
            pool_size=20,
            max_overflow=2,
        )
        self._async_session = async_sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )

    async def disconnect(self) -> None:
        await self._engine.dispose()

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def async_session(self) -> async_sessionmaker[AsyncSession]:
        return self._async_session
