from abc import ABC

from repositories.catalog.catalog_repository import CatalogRepository
from repositories.catalog.mysql_catalog_repository import MySQLCatalogRepository
from services.unit_of_work import MySQLAsyncUnitOfWork, AsyncUnitOfWork


class AbstractCatalogUnitOfWork(ABC):
    catalog: CatalogRepository


class MySQLAsyncCatalogUnitOfWork(MySQLAsyncUnitOfWork, AbstractCatalogUnitOfWork):

    async def __aenter__(self):
        self.session = await self.session_factory()
        self.catalog = MySQLCatalogRepository(self.session)
        await super().__aenter__()
