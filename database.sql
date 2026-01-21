CREATE DATABASE student_task_db;
USE student_task_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    role ENUM('admin','student')
);

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200),
    description TEXT,
    due_date DATE,
    student_id INT,
    status VARCHAR(20) DEFAULT 'In Progress',
    FOREIGN KEY (student_id) REFERENCES users(id)
);
