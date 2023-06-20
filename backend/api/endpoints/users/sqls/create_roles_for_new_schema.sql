CREATE ROLE sys_admin;
CREATE ROLE db_admin;
CREATE ROLE dekan;
CREATE ROLE professor;
CREATE ROLE research_assistant;
CREATE ROLE extern_assistant;
CREATE ROLE student;
CREATE ROLE secretary;
CREATE ROLE enrollement_secretary
-- student
GTANT SELECT ON Person, Address, Location, BusinessHours, DailyBusinessHours, PersonToPermission, Permission, Staff, Degree, LectureToDegree, Lecture, Exam, SemesterSpecificLecture, LecturePlan, Room, LectureToRestriction, Restriction TO student;
-- enrollment_secretary
GRANT SELECT ON Person, Student, Address, Degree TO enrollement_secretary;
GRANT INSERT ON Person, Address, Student TO enrollement_secretary;
-- secretary
GRANT SELECT, INSERT, UPDATE ON Person, Address, Location, BusinessHours, DailyBusinessHours, PersonToPermission, Permission, Room, RoomRequiredPermission, Staff, Student, Degree, LectureToDegree, Lecture, Exam, ExamAttempt, SemesterSpecificLecture, LecturePlan, Room, LectureToRestriction, Restriction TO secretary;
GRANT professor, research_assistant, extern_assistant, student, door TO secretary WITH ADMIN OPTION;
-- professor, research_assistant, extern_assistant
GRANT SELECT ON Person, Address, Location, BusinessHours, DailyBusinessHours, PersonToPermission, Permission, Staff, Student, Degree, LectureToDegree, Lecture, Exam, ExamAttempt, SemesterSpecificLecture, LecturePlan, Room, LectureToRestriction, Restriction TO professor, research_assistant, extern_assistant;
GRANT INSERT, UPDATE ON Exam, ExamAttempt, SemesterSpecificLecture,
-- sys_admin, db_admin, dekan
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sys_admin, db_admin, dekan;
GRANT admin TO sys_admin, db_admin, dekan WITH ADMIN OPTION;