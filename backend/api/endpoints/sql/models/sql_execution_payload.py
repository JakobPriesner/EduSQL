from api.camel_model import CamelModel


class SqlExecutionPayload(CamelModel):
    username: str
    password: str
    sql_statement: str
