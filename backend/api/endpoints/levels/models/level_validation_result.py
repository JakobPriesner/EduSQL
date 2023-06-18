from api.camel_model import CamelModel


class LevelValidationResult(CamelModel):
    level: str
    is_valid: bool
    message: str
