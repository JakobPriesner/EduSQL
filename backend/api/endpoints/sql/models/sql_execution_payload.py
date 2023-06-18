from api.camel_model import CamelModel


class SqlExecutionPayload(CamelModel):
    user_name: str
    password: str
    sql_statement: str
