# Student Management System

A desktop Student Management System built with Python, Tkinter, and MySQL as a course project for Object-Oriented Techniques (2025).

## Features

- Secure login screen with show/hide password toggle
- Connect to a local MySQL database from the UI
- Add, update, delete, and search student records
- View all students in a sortable table
- Export student data to CSV
- Live date/time display and status bar

## Tech Stack

- Language: Python 3
- GUI: Tkinter (ttk)
- Database: MySQL via PyMySQL
- Images: Pillow (PIL)

## Project Structure

    .
    ├── login.py                 # Entry point — login screen
    ├── studentmanagement.py     # Main application (CRUD + DB)
    ├── logo.png
    ├── user.png
    ├── password.png
    ├── show.png
    ├── hide.png
    └── students.png

## Requirements

- Python 3.10+
- MySQL Server (or XAMPP)

Install dependencies: `pip install Pillow PyMySQL`

## Setup & Run

1. Start your MySQL server (e.g. via XAMPP Control Panel).
2. Run the login screen: `python login.py`
3. Log in with Username: `Rafi` and Password: `1234`
4. Click Connect Database and enter your MySQL credentials (default: `localhost` / `root` / empty password). The app will automatically create the `studentmanagementsystem` database and the `students` table on first connect.

## Database Design

The system uses a single MySQL database named `studentmanagementsystem`, which is created automatically by the application on the first successful database connection. All student records are stored in one table called `students`, keeping the schema simple and easy to manage for the scope of this project.

### Table: students

    CREATE TABLE IF NOT EXISTS students(
        id      INT NOT NULL PRIMARY KEY,
        name    VARCHAR(30),
        mobile  VARCHAR(15),
        email   VARCHAR(30),
        address VARCHAR(100),
        gender  VARCHAR(20),
        dob     VARCHAR(20),
        date    VARCHAR(50),
        time    VARCHAR(50)
    );

### Column Description

| Column   | Type          | Constraint            | Purpose                                  |
|----------|---------------|-----------------------|------------------------------------------|
| id       | INT           | PRIMARY KEY, NOT NULL | Unique identifier for each student       |
| name     | VARCHAR(30)   | —                     | Student's full name                      |
| mobile   | VARCHAR(15)   | —                     | Contact phone number                     |
| email    | VARCHAR(30)   | —                     | Email address                            |
| address  | VARCHAR(100)  | —                     | Residential address                      |
| gender   | VARCHAR(20)   | —                     | Male / Female / Other                    |
| dob      | VARCHAR(20)   | —                     | Date of birth (stored as text)           |
| date     | VARCHAR(50)   | —                     | Date the record was added or last updated|
| time     | VARCHAR(50)   | —                     | Time the record was added or last updated|

### Design Notes

- The schema is intentionally flat and denormalized: every student's details live in a single row, with no foreign keys or related tables. This matches the scope of the project and keeps queries simple.
- The `id` field is entered manually by the admin rather than being AUTO_INCREMENT, which allows the institution to assign its own student numbers. Duplicate IDs are rejected by the primary key constraint.
- The `dob`, `date`, and `time` fields are stored as VARCHAR instead of DATE or DATETIME. This simplifies formatting for display in the Tkinter interface, though it limits date-based sorting and querying.
- The `date` and `time` columns act as lightweight audit fields, automatically populated by the application whenever a record is created or updated.

### Entity Relationship Diagram

    STUDENTS
    ────────
    PK  id
        name
        mobile
        email
        address
        gender
        dob
        date
        time

### SQL Operations Used

    -- Create database and table (executed automatically on first connection)
    CREATE DATABASE IF NOT EXISTS studentmanagementsystem;
    USE studentmanagementsystem;
    CREATE TABLE IF NOT EXISTS students (...);

    -- Read all students
    SELECT * FROM students;

    -- Insert a new student
    INSERT INTO students VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);

    -- Update an existing student
    UPDATE students
    SET name=%s, mobile=%s, email=%s, address=%s,
        gender=%s, dob=%s, date=%s, time=%s
    WHERE id=%s;

    -- Delete a student
    DELETE FROM students WHERE id=%s;

    -- Search across multiple fields
    SELECT * FROM students
    WHERE id=%s OR name=%s OR mobile=%s OR email=%s
       OR address=%s OR gender=%s OR dob=%s;

### Future Enhancements

- Migrate `dob`, `date`, and `time` to native DATE and DATETIME types for better querying and sorting.
- Convert `id` to AUTO_INCREMENT or a UUID to avoid manual assignment errors.
- Introduce a `users` table for admin and teacher accounts, replacing the hardcoded login.
- Add `courses` and `departments` tables with a linking table for student enrollment, moving toward a properly normalized design.

## Notes

- Login credentials are hardcoded for demo purposes.
- Database connection details are entered at runtime, not stored.
- The `students` table is created automatically — no manual SQL needed.

## Author

Iftekhar Ibne Masud Rafi
Student ID: 202380090158
Course: Object-Oriented Techniques (2025)