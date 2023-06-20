from injector import inject

from api.endpoints.levels.logic.validation.strategies.concrete_validation_interface import IConcreteValidation
from api.endpoints.levels.models.level_validation_result import LevelValidationResult
from database.db_user_handler import DbUserHandler
from database.models.db_user import DbUser
from database.postgresql_connection_interface import IPostgresqlConnection


class LevelOneTaskFourValidator(IConcreteValidation):
    @inject
    def __init__(self, db: IPostgresqlConnection, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._db_user_handler: DbUserHandler = db_user_handler
        self._admin_user: DbUser = self._db_user_handler.get_user_by_username("admin")
        self.expected_street: str = "Münzstraße"
        self.expected_house_number: str = "16"
        self.expected_postal_code: str = "97071"
        self.expected_city: str = "Würzburg"
        self.expected_country: str = "Deutschland"

    async def handle(self, user_uuid: str, **kwargs) -> LevelValidationResult:
        statement: str = "SELECT * FROM address WHERE Street = %s AND HouseNumber = %s AND City = %s AND Country = %s AND PostalCode = %s;"
        address_in_db: dict = await self._db.load_single_by_sql(self._admin_user, user_uuid, statement,
                                                                (self.expected_street, self.expected_house_number,
                                                                 self.expected_city, self.expected_country,
                                                                 self.expected_postal_code))
        if not address_in_db:
            return LevelValidationResult(level="1.4",
                                         is_valid=False,
                                         message=f"Address \"{self.expected_street} {self.expected_house_number}, {self.expected_postal_code} {self.expected_city} in {self.expected_country}\" does not exist in the Table \"Address\".")
        return LevelValidationResult(level="1.4", is_valid=True, message="")

    @classmethod
    def can_handle(cls, level_number: int, task_number: int) -> bool:
        return level_number == 1 and task_number == 4
