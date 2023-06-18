from api.camel_model import CamelModel


class GetUserResponse(CamelModel):
    exists: bool = False
