from dataclasses import dataclass


@dataclass
class PostgresqlConfig:
    host: str
    port: str
    database: str
    user: str
    password: str
