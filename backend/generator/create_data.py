import asyncio
import time
import traceback

from dotenv import load_dotenv
from injector import inject, Injector

from generator.data_generator import *
from generator.data_generator.crate_semester_specific_lecture import create_sslecture
from generator.data_generator.create_daily_business_hours import create_daily_business_hours
from generator.data_generator.create_lecture_to_degree import create_lecture_to_degrees
from generator.data_generator.create_room import create_room
from generator.database.db_handler import DbHandler
from generator.processing.process_handler import ProcessHandler

from database.db_user_handler import DbUserHandler
from database.postgresql_connection_interface import IPostgresqlConnection
from log.logger_interface import ILogger


class DataGenerator:
    @inject
    def __init__(self, db: IPostgresqlConnection, logger: ILogger, db_user_handler: DbUserHandler):
        self._db: IPostgresqlConnection = db
        self._logger: ILogger = logger
        self.db_user_handler: DbUserHandler = db_user_handler

    async def create_data_if_not_exist(self) -> None:
        sql: str = "SELECT COUNT(*) FROM Person;"
        count, = await self._db.load_single_by_sql(
            user=self.db_user_handler.get_user_by_username("admin"),
            db="template",
            sql=sql)

        if count == 0:
            self._logger.info("No data found, creating data...")
            await self.create_data_async()
        else:
            self._logger.info("Data already exists, skipping data generation.")

    async def create_data_async(self):
        await DbHandler.__async_init__()
        tasks = [
            create_addresses,
            create_daily_business_hours,
            create_locations,
            create_degrees,
            create_room,
            create_lectures,
            create_persons,
            create_staffs,
            create_students,
            create_lecture_to_degrees,
            create_sslecture,
            create_exams,
            create_permissions,
            create_person_to_permissions,
            create_exam_attempts,
            create_lecture_plan,
            create_vacation_semesters
        ]

        total_tasks = len(tasks)
        progress = 0

        print("Data generation in progress:")

        start_time = time.time()

        for task in tasks:
            progress += 1
            percentage = (progress / total_tasks) * 100
            progress_str = f"[{progress}/{total_tasks}]"
            task_name = task.__name__
            percentage_str = f"{percentage:.2f}%"

            start_task_time = time.time()
            await task()
            end_task_time = time.time()
            elapsed_time = end_task_time - start_task_time
            time_str = f"completed within {elapsed_time:.2f} seconds."

            print(f"{progress_str: <8} {task_name: <35} {percentage_str: <8} {time_str}")

        end_time = time.time()
        total_elapsed_time = end_time - start_time
        print(f"\nData generation completed. Total time: {total_elapsed_time:.2f} seconds.")

        await DbHandler.close()
        ProcessHandler.close()

    async def create_data_async_old(self):
        load_dotenv()
        await DbHandler.__async_init__()
        try:
            create_address_task = create_addresses()
            create_daily_business_hours_task = create_daily_business_hours()
            create_locations_task = self.__create_locations(create_daily_business_hours_task)
            create_degrees_task = self.__create_degrees_and_rooms(create_locations_task)
            create_lectures_task = create_lectures()
            await self.__create_persons_and_lecture_to_degrees(create_address_task, create_degrees_task,
                                                          create_lectures_task)
            create_permissions_task = create_permissions()
            create_person_to_permissions_task = self.__create_person_to_permission(create_permissions_task)
            create_exam_attempts_task = self.__create_exam_attempts()
            create_lecture_plan_task = self.__create_lecture_plan()
            create_vacation_semesters_task = create_vacation_semesters()

            await asyncio.gather(
                create_person_to_permissions_task, create_exam_attempts_task, create_lecture_plan_task,
                create_vacation_semesters_task
            )
        except Exception as e:
            traceback.print_exc()
        finally:
            await asyncio.sleep(10)
            await DbHandler.close()
            ProcessHandler.close()

    async def __create_persons_and_lecture_to_degrees(self, create_address_task, create_degrees_task,
                                                      create_lectures_task):
        await asyncio.gather(
            create_address_task,
            create_degrees_task,
            create_lectures_task
        )
        await create_persons()
        await asyncio.gather(
            create_staffs(),
            create_students(),
            create_lecture_to_degrees(),
            create_sslecture(),
            create_exams()
        )

    async def __create_degrees_and_rooms(self, create_locations_task):
        await create_locations_task
        create_degrees_task = create_degrees()
        create_room_task = create_room()
        await create_degrees_task
        await create_room_task

    async def __create_person_to_permission(self, create_permissions_task):
        await create_permissions_task
        await create_person_to_permissions()

    async def __create_exam_attempts(self):
        await create_exam_attempts()

    async def __create_lecture_plan(self):
        await create_lecture_plan()

    async def __create_locations(self, create_daily_business_hours_task):
        await create_daily_business_hours_task
        await create_locations()
