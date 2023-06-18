from generator.database.db_handler import DbHandler
from generator.models.business_hours import BusinessHours


class GenerateBusinessHours:
    @staticmethod
    async def store_business_hours(businesshours: BusinessHours) -> int:

        sql: str = f""" 
                    INSERT INTO businessHours
                    (mondayid, tuesdayid, wednesdayid, thursdayid, fridayid, saturdayid, sundayid, feastdayid)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """

        return await DbHandler.query(sql, businesshours.monday_id, businesshours.tuesday_id, businesshours.wednesday_id,
                                        businesshours.thursday_id, businesshours.friday_id, businesshours.saturday_id, businesshours.sunday_id, businesshours.feast_day_id)
