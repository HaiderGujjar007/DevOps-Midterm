CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    registration_number VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    subject_name VARCHAR(150) NOT NULL,
    credit_hours INT DEFAULT 3,
    grade VARCHAR(5),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS transcripts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNIQUE,
    cgpa DECIMAL(4,2),
    semester VARCHAR(20),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- Insert Haider Rasheed's data
INSERT INTO students (first_name, last_name, registration_number)
VALUES ('Haider', 'Rasheed', 'FA23-BCS-058');

SET @sid = LAST_INSERT_ID();

INSERT INTO subjects (student_id, subject_name, credit_hours, grade) VALUES
(@sid, 'Database Management Systems', 3, 'A'),
(@sid, 'Operating Systems', 3, 'A-'),
(@sid, 'Web Technologies', 3, 'B+'),
(@sid, 'Data Structures & Algorithms', 3, 'A'),
(@sid, 'Software Engineering', 3, 'B+');

INSERT INTO transcripts (student_id, cgpa, semester)
VALUES (@sid, 3.72, 'Fall 2024');
