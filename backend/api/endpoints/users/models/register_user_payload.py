from api.camel_model import CamelModel


class RegisterUserPayload(CamelModel):
    first_name: str
    last_name: str
