import asyncio
import platform
import random
from collections import defaultdict
from dataclasses import fields
from datetime import datetime, timedelta
from typing import Optional

import psycopg

# from generator.data.csv_loader import load_csv_file_as_generator
from generator.database.connection_string import get_connection_string
from generator.models.enums.exam_type_enum import ExamType
from generator.models.exam import Exam
from generator.models.exam_attempt import ExamAttempt
from generator.models.lecture import Lecture
from generator.models.room import Room
from generator.models.student import Student


class GenerateExamAttempt:
    def __init__(self, students: list[Student]):
        self.exam_attempts: list[ExamAttempt] = []
        self.students: list[Student] = students

    async def __async_init__(self):
        self.exams: list[Exam] = await self.__load_all_exams_async()
        self.rooms: list[Room] = await self.__load_all_rooms_async()
        self.lectures: list[Lecture] = await self.__load_all_lectures_async()
        # self.module_number_to_minimum_semester: dict[str, int] = await self.__load_all_module_number_to_minimum_semester()

    async def generate_all_exam_attempts_async(self) -> None:
        for student in self.students:
            exams = await self.__load_exams_for_student(student.degree_id)
            await asyncio.gather(*(self.__generate_exam_attempts_for_single_exam_for_single_student_async(student, exam) for exam in exams))
            await self.__cleanup_generated_exam_attempts_async()
            await self.__store_all_exam_attempts()

    async def __generate_exam_attempts_for_single_exam_for_single_student_async(self, student: Student,
                                                                                exam: Exam) -> None:
        first_exam_attempt_semester: str = self.__get_first_exam_attempt_semester(student, exam)

        last_exam_attempt: ExamAttempt = await self.__generate_random_exam_attempt_async(student, exam,
                                                                                         first_exam_attempt_semester)
        self.exam_attempts.append(last_exam_attempt)

        for _ in range(exam.allowed_attempts - 1):
            if last_exam_attempt.grade < 5:
                break
            written_in_semester: str = self.__get_written_in_semester(self.__semester_to_date(last_exam_attempt.written_in_semester), 1)
            last_exam_attempt = await self.__generate_random_exam_attempt_async(student, exam, written_in_semester)
            self.exam_attempts.append(last_exam_attempt)

    async def __generate_random_exam_attempt_async(self, student: Student, exam: Exam, written_in_minimum_semester: str) -> ExamAttempt:
        score: float = self.__get_random_score()
        semester_offset: int = 0 if random.uniform(0, 1) <= 0.9 else 1
        written_in_semester = self.__get_written_in_semester(self.__semester_to_date(written_in_minimum_semester), semester_offset)
        duration_in_minutes = random.randint(9, 15) * 10
        start_time_stamp: datetime = self.__get_exam_start_time(written_in_semester)
        scanned_at: datetime = start_time_stamp - timedelta(seconds=random.randint(0, 30 * 60))
        grade: float = (100 - score) / 100 * 5 + 1

        return ExamAttempt(
            exam_id=exam.id,
            student_matriculation_number=student.matriculation_number,
            room_name="",  # wird im clean_up gemacht
            score=round(score, 0),
            grade=5 if grade > 5 else round(grade, 1),
            written_in_semester=written_in_semester,
            duration_in_minutes=duration_in_minutes,
            start_time_stamp=start_time_stamp,
            end_time_stamp=start_time_stamp + timedelta(minutes=duration_in_minutes),
            exam_type=self.__get_exam_type(),
            scanned_at=scanned_at
        )

    def __get_first_exam_attempt_semester(self, student: Student, exam: Exam) -> Optional[str]:
        min_semester: int = next(le.semester for le in self.lectures if exam.lecture_id == le.id)
        return self.__get_written_in_semester(student.enrolled_at, min_semester)

    # @staticmethod
    # async def __get_exam_semester_by_lecture_async(exam_id: int) -> int:
    #     sql: str = f"""
    #                 SELECT semester FROM exam
    #                 LEFT JOIN lecture l on exam.lectureid = l.id
    #                 WHERE exam.id = ?
    #                 """
    #     async with await psycopg.AsyncConnection.connect(get_connection_string()) as conn:
    #         async with conn.cursor() as cur:
    #             await cur.execute(sql, (exam_id,))
    #             _id, = await cur.fetchone()
    #             return _id

    def __semester_to_date(self, semester: str) -> datetime:
        if len(semester) == 4:
            semester = f"20{semester}"
        month: int = 11 if semester[5:] == "ws" else 4  # todo: testen mit 11 und 4
        return datetime(year=int(semester[:4]), month=month, day=1)

    @staticmethod
    def __get_written_in_semester(old_semester: datetime, offset: int) -> str:
        min_date_written_in: datetime = old_semester + timedelta(days=offset * 3 * 61)
        # 6 Monate / 2 = 3 Monate -> * 2 Monate was 61 Tage entspricht und nochmal * 2 damit der Prüfungsversuch erst im nächsten Semester ist
        if min_date_written_in.month < 10:  # todo: testen ob 11 passt -> müsste das nicht 9 sein?
            return f"{str(min_date_written_in.year)}ss"
        else:
            return f"{str(min_date_written_in.year)}ws"
        # todo: testen ob das klappt und passt

    def __get_exam_start_time(self, written_in_semester: str) -> datetime:
        written_in_as_date: datetime = self.__semester_to_date(written_in_semester)
        day_choices: list[int] = [i for i in range(1, 28)]
        random.shuffle(day_choices)
        days = [day_choices.pop() for _ in range(10)]

        # Use a list comprehension to find the first weekday in the month
        weekdays = [datetime(written_in_as_date.year, written_in_as_date.month+3, day, random.randint(8, 15), random.choice([0, 15, 30, 45]), 0)
                    for day in days
                    if datetime(written_in_as_date.year, written_in_as_date.month+3, day).weekday() < 5]
        return random.choice(weekdays)

    @staticmethod
    def __get_exam_type() -> ExamType:
        rand_num = random.randint(0, 100)
        if rand_num <= 5:
            return ExamType.Presentation
        elif rand_num <= 20:
            return ExamType.EvaExam
        elif rand_num <= 30:
            return ExamType.Colloquium
        elif rand_num <= 80:
            return ExamType.Written
        else:
            return ExamType.Portfolio

    @staticmethod
    def __get_random_score(max_score: int = 100, failure_rate: float = 0.25) -> float:
        rand_num = random.uniform(0, 1)
        if rand_num <= failure_rate:
            sub_rand_num = random.uniform(0, 1)
            if sub_rand_num <= 0.25:
                return random.uniform(0, 0.2 * max_score)
            else:
                return random.uniform(0.21 * max_score, 0.49 * max_score)
        else:
            return random.uniform(0.5 * max_score, max_score)

    def __get_room_with_at_least_x_seats(self, seat_count: int) -> Room:
        return next(room for room in self.rooms if room.number_of_seats >= seat_count)

    async def __cleanup_generated_exam_attempts_async(self) -> None:
        #  1. bestimmen der RoomNames
        self.__set_room_for_each_exam_attempt()

        #  2. exam_attempts löschen sobald eine Person bei einer Prüfung die exam.allowedAttempts nicht bestanden hat
        self.__clear_exam_attempts()

        #  3.setzen des etcScores aller Studenten
        await self.__update_all_student_etc_score_async()

        #  4. alle exam_attempts über datetime.now() löschen
        current_semester: str = self.__get_written_in_semester(datetime.now(), 0)
        self.exam_attempts = [ea for ea in self.exam_attempts if ea.written_in_semester <= current_semester]

    def __set_room_for_each_exam_attempt(self) -> None:
        exam_attempts_by_semester: dict[str, int] = defaultdict(int)
        for attempt in self.exam_attempts:
            exam_attempts_by_semester[attempt.written_in_semester] += 1

        room_by_capacity = {room.number_of_seats: room.room_name for room in self.rooms}

        for semester, count in exam_attempts_by_semester.items():
            room_capacity: int = next((capacity for capacity in room_by_capacity if capacity >= count), None)
            room_name: str = room_by_capacity.get(room_capacity, "H.1.1")
            for attempt in [at for at in self.exam_attempts if at.written_in_semester == semester]:
                attempt.room_name = room_name

    def __clear_exam_attempts(self) -> None:
        exam_attempts_by_student: dict[int, list] = defaultdict(list)

        for attempt in self.exam_attempts:
            exam_attempts_by_student[attempt.student_matriculation_number].append(attempt)

        for attempts in exam_attempts_by_student.values():
            attempts.sort(key=lambda x: x.written_in_semester)

        for student_attempts in exam_attempts_by_student.values():
            for exam in self.exams:
                exam_attempts_for_exam: list[ExamAttempt] = [att for att in student_attempts if att.exam_id == exam.id]
                if len(exam_attempts_for_exam) == exam.allowed_attempts and exam_attempts_for_exam[-1].grade > 4:
                    semester_to_remove: str = exam_attempts_for_exam[-1].written_in_semester
                    attempts_to_remove: list[ExamAttempt] = [att for att in student_attempts if att.written_in_semester > semester_to_remove]
                    self.exam_attempts = [att for att in self.exam_attempts if att not in attempts_to_remove]

    async def __store_all_exam_attempts(self) -> None:
        print(f"Store {len(self.exam_attempts)} ExamAttempts")
        if len(self.exam_attempts) == 0:
            return
        sql: str = f"""
                    INSERT INTO examattempt
                    (ExamId, StudentMatriculationnumber, RoomName, Score, Grade, WrittenInSemester, DurationInMinutes, StartTimestamp, EndTimestamp, ExamType, ScannedAt)
                    VALUES {', '.join('(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' for _ in self.exam_attempts)};
                    """

        async with await psycopg.AsyncConnection.connect(get_connection_string()) as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, tuple(item for item in tuple(
                    getattr(entry, field.name) for entry in self.exam_attempts for field in fields(entry) if
                    field.name != "id")))
                await conn.commit()

    async def __update_all_student_etc_score_async(self) -> None:
        for student in self.students:
            student_passed_exam_attempts = [ea for ea in self.exam_attempts
                                            if ea.student_matriculation_number == student.matriculation_number
                                            and ea.grade < 5]
            passed_lecture_ids = [exam.lecture_id for ea in student_passed_exam_attempts for exam in self.exams if exam.id == ea.exam_id]
            student.etc_score = sum(le.earned_etcs for le in self.lectures if le.id in passed_lecture_ids)
        # todo: test

    async def __load_all_exams_async(self) -> list[Exam]:
        sql: str = "SELECT * from exam"
        async with await psycopg.AsyncConnection.connect(get_connection_string()) as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                results: list[tuple] = await cur.fetchall()
                return [
                    Exam(lecture_id, allowed_attempts, id)
                    for id, lecture_id, allowed_attempts in results
                ]

    async def __load_all_rooms_async(self) -> list[Room]:
        sql: str = "SELECT * from room"
        async with await psycopg.AsyncConnection.connect(get_connection_string()) as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                results: list[tuple] = await cur.fetchall()
                return [
                    Room(room_name, location_id, description, number_of_seats)
                    for room_name, location_id, description, number_of_seats in results
                ]

    async def __load_all_lectures_async(self) -> list[Lecture]:
        sql: str = "SELECT * from lecture"
        async with await psycopg.AsyncConnection.connect(get_connection_string()) as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql)
                results: list[tuple] = await cur.fetchall()
                return [
                    Lecture(name, description, modulenumber, required_etcs, earned_etcs, semester, type, id)
                    for id, name, description, modulenumber, required_etcs, earned_etcs, semester, type in results
                ]

    async def __update_student_ect(self, student_mat_number: int, ect_score: int) -> None:
        sql: str = "UPDATE student SET etcsscore = %s where matriculationnumber = %s"
        async with await psycopg.AsyncConnection.connect(get_connection_string()) as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, (ect_score, student_mat_number))
                await conn.commit()

    @staticmethod
    async def __load_exams_for_student(degree_id: int) -> list[Exam]:
        sql: str = """
                   SELECT e.* from Exam as e
                   INNER JOIN Lecture as l ON e.LectureId = l.Id
                   INNER JOIN LectureToDegree as ltd ON ltd.LectureId = l.Id
                   WHERE ltd.DegreeId = %s;
                   """
        async with await psycopg.AsyncConnection.connect(get_connection_string()) as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, (degree_id,))
                results: list[tuple] = await cur.fetchall()
                return [
                    Exam(id=_id, lecture_id=lecture_id, allowed_attempts=allowed_attempts)
                    for _id, lecture_id, allowed_attempts in results
                ]

    # async def __load_all_module_number_to_minimum_semester(self) -> dict:
    #     # todo: test
    #     module_number_to_minimum_semester: dict[str, int] = {}
    #
    #     for module_description in load_csv_file_as_generator("moduledescription.csv"):
    #         _, _, _, _, _, _, _, _, _, lpsemester, _, _, _, _, modulenumber, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _ = module_description
    #         for module_number in [mn.strip() for mn in modulenumber.replace(" ", "").split(",")]:
    #             module_number_to_minimum_semester[module_number] = int(lpsemester)
    #
    #     return module_number_to_minimum_semester


async def __load_all_stundents_async() -> list[Student]:
    sql: str = "SELECT * from student"
    async with await psycopg.AsyncConnection.connect(get_connection_string()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql)
            results: list[tuple] = await cur.fetchall()
            return [
                Student(matriculation_number, person_id, degree_id, etc_score, in_student_council, enrolled_at,
                        exmatriculated_at)
                for
                matriculation_number, person_id, degree_id, etc_score, in_student_council, enrolled_at, exmatriculated_at
                in results
            ]


async def create_exam_attempts() -> None:
    students: list[Student] = await __load_all_stundents_async()
    batch_size: int = 5
    counter: int = 0
    for batch in [students[i:i+batch_size] for i in range(0, len(students), batch_size)]:
        counter += 1
        print(f"Create batch for {counter}. Batch.")
        exam_attempts: GenerateExamAttempt = GenerateExamAttempt(batch)
        await exam_attempts.__async_init__()
        await exam_attempts.generate_all_exam_attempts_async()
    # do some cool stuff

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_exam_attempts())
