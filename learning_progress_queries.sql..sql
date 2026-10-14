CREATE DATABASE learning_progress;
USE learning_progress;
CREATE TABLE LEARNER (
    learner_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);
SHOW TABLES;
CREATE TABLE COURSE (
    course_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(150) NOT NULL,
    description VARCHAR(500)
);
CREATE TABLE ENROLMENT (
    enrolment_id INT PRIMARY KEY AUTO_INCREMENT,
    learner_id INT NOT NULL,
    course_id INT NOT NULL,
    enrolment_date DATE DEFAULT (CURRENT_DATE),
    UNIQUE (learner_id, course_id),
    FOREIGN KEY (learner_id) REFERENCES LEARNER(learner_id),
    FOREIGN KEY (course_id) REFERENCES COURSE(course_id)
);
SHOW TABLES;
CREATE TABLE INSTRUCTOR (
    instructor_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE
);
ALTER TABLE COURSE
ADD instructor_id INT,
ADD FOREIGN KEY (instructor_id)
REFERENCES INSTRUCTOR(instructor_id);
SHOW TABLES;
CREATE TABLE MODULE (
    module_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    module_name VARCHAR(150) NOT NULL,
    FOREIGN KEY (course_id) REFERENCES COURSE(course_id)
);
CREATE TABLE LESSON (
    lesson_id INT PRIMARY KEY AUTO_INCREMENT,
    module_id INT NOT NULL,
    lesson_name VARCHAR(150) NOT NULL,
    FOREIGN KEY (module_id) REFERENCES MODULE(module_id)
);
SHOW TABLES;
CREATE TABLE LESSON_PROGRESS (
    progress_id INT PRIMARY KEY AUTO_INCREMENT,
    learner_id INT NOT NULL,
    lesson_id INT NOT NULL,
    progress DECIMAL(5,2) DEFAULT 0.00,
    FOREIGN KEY (learner_id) REFERENCES LEARNER(learner_id),
    FOREIGN KEY (lesson_id) REFERENCES LESSON(lesson_id),
    CHECK (progress >= 0 AND progress <= 100),
    UNIQUE (learner_id, lesson_id)
);
CREATE TABLE QUIZ (
    quiz_id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    FOREIGN KEY (course_id) REFERENCES COURSE(course_id)
);
SHOW TABLES;
CREATE TABLE QUESTION (
    question_id INT PRIMARY KEY AUTO_INCREMENT,
    quiz_id INT NOT NULL,
    question_text VARCHAR(500) NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES QUIZ(quiz_id)
);
CREATE TABLE ATTEMPT (
    attempt_id INT PRIMARY KEY AUTO_INCREMENT,
    learner_id INT NOT NULL,
    quiz_id INT NOT NULL,
    attempt_no INT NOT NULL,
    score DECIMAL(5,2),
    attempt_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (learner_id) REFERENCES LEARNER(learner_id),
    FOREIGN KEY (quiz_id) REFERENCES QUIZ(quiz_id),
    UNIQUE (learner_id, quiz_id, attempt_no),
    CHECK (attempt_no > 0),
    CHECK (score IS NULL OR (score >= 0 AND score <= 100))
);
SHOW TABLES;
USE learning_progress;

-- 1. Add instructors
INSERT INTO INSTRUCTOR (name, email) VALUES
('Rahul Sharma', 'rahul@example.com'),
('Priya Singh', 'priya@example.com');

-- 2. Add learners
INSERT INTO LEARNER (name, email) VALUES
('Aman Kumar', 'aman@example.com'),
('Neha Verma', 'neha@example.com'),
('Rohit Singh', 'rohit@example.com');

-- 3. Add courses
INSERT INTO COURSE (title, description, instructor_id) VALUES
('Python Programming', 'Learn Python from basics', 1),
('Database Management Systems', 'Learn SQL and database concepts', 2);

-- 4. Enrol learners in courses
INSERT INTO ENROLMENT (learner_id, course_id) VALUES
(1, 1),
(1, 2),
(2, 1),
(3, 2);
SELECT * FROM LEARNER;
SELECT * FROM COURSE;
SELECT * FROM ENROLMENT;
SELECT * FROM INSTRUCTOR;
USE learning_progress;

-- Add modules
INSERT INTO MODULE (course_id, module_name) VALUES
(1, 'Python Basics'),
(1, 'Functions and Loops'),
(2, 'Introduction to DBMS'),
(2, 'SQL Fundamentals');

-- Add lessons
INSERT INTO LESSON (module_id, lesson_name) VALUES
(1, 'Python Variables'),
(1, 'Data Types'),
(2, 'Loops in Python'),
(3, 'Database Concepts'),
(4, 'SQL Queries');
INSERT INTO LESSON_PROGRESS (learner_id, lesson_id, progress) VALUES
(1, 1, 100),
(1, 2, 75),
(2, 1, 50),
(3, 4, 80);
INSERT INTO QUIZ (course_id, title) VALUES
(1, 'Python Basics Quiz'),
(2, 'DBMS Fundamentals Quiz');

INSERT INTO QUESTION (quiz_id, question_text) VALUES
(1, 'What is a variable in Python?'),
(1, 'Which keyword defines a function in Python?'),
(2, 'What is a primary key?'),
(2, 'What is a foreign key?');
INSERT INTO ATTEMPT
(learner_id, quiz_id, attempt_no, score) VALUES
(1, 1, 1, 85),
(2, 1, 1, 70),
(1, 2, 1, 90),
(3, 2, 1, 65);
SELECT * FROM MODULE;
SELECT * FROM LESSON;
SELECT * FROM LESSON_PROGRESS;
SELECT * FROM QUIZ;
SELECT * FROM QUESTION;
SELECT * FROM ATTEMPT;
SELECT * FROM LEARNER;
SELECT COURSE.title, INSTRUCTOR.name AS instructor
FROM COURSE
JOIN INSTRUCTOR
ON COURSE.instructor_id = INSTRUCTOR.instructor_id;
SELECT LEARNER.name, COURSE.title
FROM ENROLMENT
JOIN LEARNER
ON ENROLMENT.learner_id = LEARNER.learner_id
JOIN COURSE
ON ENROLMENT.course_id = COURSE.course_id;
SELECT LEARNER.name, LESSON.lesson_name,
       LESSON_PROGRESS.progress
FROM LESSON_PROGRESS
JOIN LEARNER
ON LESSON_PROGRESS.learner_id = LEARNER.learner_id
JOIN LESSON
ON LESSON_PROGRESS.lesson_id = LESSON.lesson_id;
SELECT LEARNER.name, QUIZ.title, ATTEMPT.score
FROM ATTEMPT
JOIN LEARNER
ON ATTEMPT.learner_id = LEARNER.learner_id
JOIN QUIZ
ON ATTEMPT.quiz_id = QUIZ.quiz_id;



