from typing import Optional

from api.camel_model import CamelModel


class SelectAllSqlResult(CamelModel):
    operation: str = "selectAll"
    result: Optional[list[dict]]
    errors: str = ""
