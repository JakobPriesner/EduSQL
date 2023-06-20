CREATE ROLE sys_admin IN <db_name>;
CREATE ROLE db_admin IN <db_name>;
CREATE ROLE dekan IN <db_name>;
CREATE ROLE professor IN <db_name>;
CREATE ROLE research_assistant IN <db_name>;
CREATE ROLE extern_assistant IN <db_name>;
CREATE ROLE student IN <db_name>;
CREATE ROLE secretary IN <db_name>;
CREATE ROLE enrollement_secretary IN <db_name>;
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