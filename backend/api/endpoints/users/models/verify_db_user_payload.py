from api.camel_model import CamelModel


class VerifyDbUserPayload(CamelModel):
    username: str
    password: str
