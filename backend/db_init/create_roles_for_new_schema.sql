CREATE ROLE sys_admin;
CREATE ROLE db_admin;
CREATE ROLE dekan;
CREATE ROLE professor;
CREATE ROLE research_assistant;
CREATE ROLE extern_assistant;
CREATE ROLE student;
CREATE ROLE secretary;
CREATE ROLE enrollment_secretary;
-- student
GRANT SELECT ON Person, Address, Location, BusinessHours, DailyBusinessHours, PersonToPermission, Permission, Staff, Degree, LectureToDegree, Lecture, Exam, SemesterSpecificLecture, Room, LectureToRestriction, Restriction TO student;
-- enrollment_secretary
GRANT SELECT ON Person, Student, Address, Degree TO enrollment_secretary;
GRANT INSERT ON Person, Address, Student TO enrollment_secretary;
-- secretary
GRANT SELECT, INSERT, UPDATE ON Person, Address, Location, BusinessHours, DailyBusinessHours, PersonToPermission, Permission, Room, RoomRequiredPermission, Staff, Student, Degree, LectureToDegree, Lecture, Exam, ExamAttempt, SemesterSpecificLecture, Room, LectureToRestriction, Restriction TO secretary;
-- secretary
GRANT professor, research_assistant, extern_assistant TO secretary WITH ADMIN OPTION;
-- professor, research_assistant, extern_assistant
GRANT SELECT ON Person, Address, Location, BusinessHours, DailyBusinessHours, PersonToPermission, Permission, Staff, Student, Degree, LectureToDegree, Lecture, Exam, ExamAttempt, SemesterSpecificLecture, Room, LectureToRestriction, Restriction TO professor, research_assistant, extern_assistant;
GRANT INSERT, UPDATE ON Exam, ExamAttempt, SemesterSpecificLecture TO professor, research_assistant, extern_assistant;
-- sys_admin, db_admin, dekan
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sys_admin, db_admin, dekan;
GRANT admin TO sys_admin, db_admin, dekan WITH ADMIN OPTION;