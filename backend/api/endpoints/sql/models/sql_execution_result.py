from typing import Optional

from api.camel_model import CamelModel


class SqlExecutionResult(CamelModel):
    result_as_dict: Optional[dict | list]
    errors: str
    