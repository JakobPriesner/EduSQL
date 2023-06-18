CREATE TABLE IF NOT EXISTS DailyBusinessHours (
    Id SERIAL PRIMARY KEY,
    StartTime TIME NOT NULL,
    EndTime TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS BusinessHours (
    Id SERIAL PRIMARY KEY,
    MondayId INT,
    TuesdayId INT,
    WednesdayId INT,
    ThursdayId INT,
    FridayId INT,
    SaturdayId INT,
    SundayId INT,
    FeastDayId INT
);

CREATE TABLE IF NOT EXISTS Address (
    Id SERIAL PRIMARY KEY,
    Street VARCHAR(60) NOT NULL,
    HouseNumber VARCHAR(6) NOT NULL,
    AddressAddition VARCHAR(300),
    City VARCHAR(30) NOT NULL,
    Country VARCHAR(60) NOT NULL,
    PostalCode INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Location (
    Id SERIAL PRIMARY KEY,
    AddressId INT,
    BusinessHoursId INT,
    Area VARCHAR(30) NOT NULL,
    LectureRoomCount INT NOT NULL,
    BuildingCount INT NOT NULL,
    Mensa BOOLEAN NOT NULL,
    ParkingSlots INT NOT NULL,
    Library BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS Permission (
    Id SERIAL PRIMARY KEY,
    Alias VARCHAR(255) NOT NULL,
    Description VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Person (
    Id SERIAL PRIMARY KEY,
    AddressId INT,
    FirstName VARCHAR(75) NOT NULL,
    LastName VARCHAR(75) NOT NULL,
    TitleId VARCHAR(15) NOT NULL,
    DateOfBirth DATE NOT NULL,
    Email VARCHAR(255) NOT NULL,
    KNumber VARCHAR(10) NOT NULL,
    PasswordHash VARCHAR(128) NOT NULL,
    Salt VARCHAR(50) NOT NULL,
    SessionToken VARCHAR(264)
);

CREATE TABLE IF NOT EXISTS PersonToPermission (
    PersonId INT,
    PermissionId INT,
    PRIMARY KEY (PersonId, PermissionId)
);

CREATE TABLE IF NOT EXISTS Room (
    RoomName VARCHAR(50) PRIMARY KEY,
    LocationId INT,
    Description VARCHAR(255),
    NumberOfSeats INT NOT NULL
);

CREATE TABLE IF NOT EXISTS RoomRequiredPermission (
    PermissionId INT, -- wegen Delete und primary key schauen
    RoomName VARCHAR(10),
    PRIMARY KEY (PermissionId, RoomName)
);

CREATE TABLE IF NOT EXISTS Restriction (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(30) UNIQUE NOT NULL,
    Description TEXT
);

CREATE TABLE IF NOT EXISTS Lecture (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Description TEXT NOT NULL,
    Modulenumber VARCHAR(20) NOT NULL,
    RequiredEtcs SMALLINT NOT NULL,
    EarnedEtcs SMALLINT NOT NULL,
    Semester INT CHECK ( Semester > 0 AND Semester < 12 ) NOT NULL, -- wie viele Semester? Evtl. Rott fragen
    Type VARCHAR(10) CHECK ( Type IN ('AWPF','FWPM','VL','SU', 'P', 'Exercise') ) NOT NULL -- nochmal mit ERM vergleichen,
);

CREATE TABLE IF NOT EXISTS LectureToRestriction (
    LectureId INT, -- wieder prüfen
    RestrictionId INT,
    PRIMARY KEY (LectureId, RestrictionId)
);

CREATE TABLE IF NOT EXISTS SemesterSpecificLecture (
    LectureId SERIAL,
    SemesterDate VARCHAR(6) NOT NULL,
    RoomName VARCHAR(255),
    StudentCount INT NOT NULL,
    ExamType VARCHAR(255) NOT NULL,
    LectureType VARCHAR(100) NOT NULL,
    PRIMARY KEY (LectureId, SemesterDate)
);

CREATE TABLE IF NOT EXISTS Degree (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(5), -- BIN, WINF
    LocationId INT, -- das ist im ERM ein PK aber würde sagen das ist FK, gibt ja nicht den gleichen Studiengang an unterschiedlichen Locations
    TotalEtc INT NOT NULL,
    DegreeType VARCHAR(50) NOT NULL, -- Bachelor of Engineering
    SemesterCount INT NOT NULL,
    UNIQUE (Name, LocationId)
);

CREATE TABLE IF NOT EXISTS LectureToDegree (
    DegreeId INT,
    LectureId INT,
    PRIMARY KEY (DegreeId, LectureId)
);

CREATE TABLE IF NOT EXISTS Staff (
    Id SERIAL PRIMARY KEY,
    PersonId INT NOT NULL,
    ReportsToId INT,
    RoomName VARCHAR(10),
    StaffType VARCHAR(18) NOT NULL CHECK ( StaffType IN ('Professor','ExternalAssistant','ResearchAssistant','StudentAssistant') ),
    Salary REAL NOT NULL,
    TemporaryTo DATE DEFAULT NULL,
    EmployedSince DATE NOT NULL,
    HoursPerWeek REAL NOT NULL,
    Holidays REAL NOT NULL,
    SocialSecurityId BIGINT NOT NULL,
    Iban VARCHAR(22) NOT NULL,
    Released DATE DEFAULT NULL,
    Paused DATE DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS Student (
    MatriculationNumber INT PRIMARY KEY,
    PersonId INT NOT NULL,
    DegreeId INT NOT NULL,
    EtcsScore SMALLINT NOT NULL DEFAULT 0,
    InStudentCouncil BOOLEAN NOT NULL DEFAULT FALSE,
    EnrolledAt TIMESTAMP NOT NULL DEFAULT now(),
    ExmatriculatedAt DATE DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS LectureToStaff (
    LectureId INT,
    StaffId INT,
    PRIMARY KEY (LectureId, StaffId)
);

CREATE TABLE IF NOT EXISTS VacationSemester (
    Id SERIAL PRIMARY KEY,
    StudentMatriculationNumber INT NOT NULL,
    Justification VARCHAR(255) NOT NULL,
    Approved BOOLEAN NOT NULL DEFAULT false,
    SemesterCount INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Exam (
    Id SERIAL PRIMARY KEY,
    LectureId INT,
    AllowedAttempts INT NOT NULL
);

CREATE TABLE IF NOT EXISTS ExamAttempt (
    Id SERIAL PRIMARY KEY,
    ExamId INT NOT NULL,
    StudentMatriculationnumber INT NOT NULL REFERENCES Student(MatriculationNumber) ON DELETE CASCADE,
    RoomName VARCHAR(50),
    Score REAL DEFAULT NULL,
    Grade REAL DEFAULT NULL,
    WrittenInSemester VARCHAR(6) NOT NULL,
    DurationInMinutes INT NOT NULL,
    StartTimeStamp TIMESTAMP DEFAULT NULL,
    EndTimeStamp TIMESTAMP DEFAULT NULL,
    ExamType VARCHAR(35) CHECK ( ExamType IN ( 'EvaExam','Written','Colloquium','Presentation','Portfolio' ) ),
    ScannedAt TIMESTAMP DEFAULT NULL
);