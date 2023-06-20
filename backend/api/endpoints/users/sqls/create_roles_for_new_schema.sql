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
GRANT SELECT ON <db_name>.Person, <db_name>.Address, <db_name>.Location, <db_name>.BusinessHours, <db_name>.DailyBusinessHours, <db_name>.PersonToPermission, <db_name>.Permission, <db_name>.Staff, <db_name>.Degree, <db_name>.LectureToDegree, <db_name>.Lecture, <db_name>.Exam, <db_name>.SemesterSpecificLecture, <db_name>.Room, <db_name>.LectureToRestriction, <db_name>.Restriction TO student;
-- enrollment_secretary
GRANT SELECT ON <db_name>.Person, <db_name>.Student, <db_name>.Address, <db_name>.Degree TO enrollment_secretary;
GRANT INSERT ON <db_name>.Person, <db_name>.Address, <db_name>.Student TO enrollment_secretary;
-- secretary
GRANT SELECT, INSERT, UPDATE ON <db_name>.Person, <db_name>.Address, <db_name>.Location, <db_name>.BusinessHours, <db_name>.DailyBusinessHours, <db_name>.PersonToPermission, <db_name>.Permission, <db_name>.Room, <db_name>.RoomRequiredPermission, <db_name>.Staff, <db_name>.Student, <db_name>.Degree, <db_name>.LectureToDegree, <db_name>.Lecture, <db_name>.Exam, <db_name>.ExamAttempt, <db_name>.SemesterSpecificLecture, <db_name>.Room, <db_name>.LectureToRestriction, <db_name>.Restriction TO secretary;
-- secretary
GRANT professor, research_assistant, extern_assistant TO secretary WITH ADMIN OPTION;
-- professor, research_assistant, extern_assistant
GRANT SELECT ON <db_name>.Person, <db_name>.Address, <db_name>.Location, <db_name>.BusinessHours, <db_name>.DailyBusinessHours, <db_name>.PersonToPermission, <db_name>.Permission, <db_name>.Staff, <db_name>.Student, <db_name>.Degree, <db_name>.LectureToDegree, <db_name>.Lecture, <db_name>.Exam, <db_name>.ExamAttempt, <db_name>.SemesterSpecificLecture, <db_name>.Room, <db_name>.LectureToRestriction, <db_name>.Restriction TO professor, research_assistant, extern_assistant;
GRANT INSERT, UPDATE ON <db_name>.Exam, <db_name>.ExamAttempt, <db_name>.SemesterSpecificLecture TO professor, research_assistant, extern_assistant;
-- sys_admin, db_admin, dekan
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sys_admin, db_admin, dekan;
GRANT admin TO sys_admin, db_admin, dekan WITH ADMIN OPTION;