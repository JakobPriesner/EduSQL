from abc import ABC, abstractmethod
from typing import Optional

from database.models.db_user import DbUser


class IPostgresqlConnection(ABC):
    @abstractmethod
    async def create_database(self, user: DbUser, db: str, new_db_name: str) -> None:
        ...

    @abstractmethod
    async def create_by_sql(self, user: DbUser, db: str, sql: str, args: tuple = ()) -> int:
        ...

    @abstractmethod
    async def create_many_by_sql(self, user: DbUser, db: str, sql: str, args: list[tuple]) -> list[int]:
        ...

    @abstractmethod
    async def load_all_by_sql(self, user: DbUser, db: str, sql: str, args: tuple = ()) -> list[dict]:
        ...

    @abstractmethod
    async def load_single_by_sql(self, user: DbUser, db: str, sql: str, args: tuple = ()) -> Optional[dict]:
        ...

    @abstractmethod
    async def update_by_sql(self, user: DbUser, db: str, sql: str, args: tuple = ()) -> int:
        ...

    @abstractmethod
    async def delete_by_sql(self, user: DbUser, db: str, sql: str, args: tuple = ()) -> int:
        ...

    @abstractmethod
    async def execute_query(self, user, db, sql: str, args: Optional[tuple] = None) -> list[dict]:
        ...
