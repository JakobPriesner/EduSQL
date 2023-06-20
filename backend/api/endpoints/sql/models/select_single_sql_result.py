from typing import Optional

from api.camel_model import CamelModel


class SelectSingleSqlResult(CamelModel):
    operation: str = "selectSingle"
    result: Optional[dict]
    errors: str = ""
