from abc import ABC

from repositories.catalog.catalog_repository import AsyncCatalogRepository
from repositories.catalog.mysql_catalog_repository import MySQLAsyncCatalogRepository
from services.unit_of_work import MySQLAsyncUnitOfWork, AsyncUnitOfWork


class AbstractCatalogUnitOfWork(ABC):
    catalog: AsyncCatalogRepository


class MySQLAsyncCatalogUnitOfWork(MySQLAsyncUnitOfWork, AbstractCatalogUnitOfWork):

    async def __aenter__(self):
        self.session = await self.session_factory()
        self.catalog = MySQLAsyncCatalogRepository(self.session)
        await super().__aenter__()
