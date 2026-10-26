# STUDENT-RESULT-MANAGEMENT-SYSTEM
PYTHON MINI PROJECT
# Student Result Management System

## 1. Project Overview

The **Student Result Management System** is a Python-based mini project designed to manage student academic results efficiently using a MySQL database. It allows users to add student results, view all stored records, search for a particular student, and update marks when required.

The system automatically calculates grades based on the marks entered and stores the information in a database. It provides a simple menu-driven interface through which users can perform different operations.

## 2. Objectives

- To maintain student result records digitally.
- To reduce manual work in calculating grades.
- To store student information in a MySQL database.
- To provide options for adding, viewing, searching, and updating results.
- To improve the accuracy and efficiency of result management.

## 3. Technologies Used

- **Programming Language:** Python
- **Database:** MySQL
- **Database Connector:** MySQL Connector/Python
- **Code Editor:** Visual Studio Code
- **Interface:** Command-Line Interface (CLI)

## 4. Features

### Add Student Result
Allows the user to enter a student's roll number, name, and marks. The system calculates the grade automatically and saves the result in the database.

### View All Results
Displays all student records stored in the database, including roll number, name, marks, and grade.

### Search Student Result
Allows the user to search for a student's result using their roll number.

### Update Student Result
Enables the user to update a student's marks. The grade is recalculated automatically according to the new marks.

### Automatic Grade Calculation
The system calculates grades according to the following criteria:

| Marks | Grade |
|---|---|
| 90–100 | A+ |
| 80–89.99 | A |
| 70–79.99 | B |
| 60–69.99 | C |
| 40–59.99 | D |
| Below 40 | F |

### Data Storage
Student records are stored in a MySQL database, allowing the data to remain available after the program is closed.

## 5. Database Design

The project automatically creates a database named `student_result` and a table named `results`.

The table contains the following fields:

| Field Name | Data Type | Description |
|---|---|---|
| roll_no | INT | Unique roll number of the student |
| name | VARCHAR(100) | Student's name |
| marks | FLOAT | Marks obtained out of 100 |
| grade | VARCHAR(5) | Automatically calculated grade |

The `roll_no` field is the primary key, which prevents duplicate roll numbers.

## 6. Project Structure

```text
StudentResultManagement/
│
├── main.py
├── test.py
└── README.md
```

- `main.py` — Contains the main Student Result Management System.
- `test.py` — Used to test the connection between Python and MySQL.
- `README.md` — Contains project documentation and setup instructions.

## 7. Installation Requirements

Before running the project, install the following software:

1. Python 3
2. MySQL Server
3. Visual Studio Code
4. MySQL Connector/Python

Install the Python connector using the following command:

```bash
python -m pip install mysql-connector-python
```

## 8. Configuration

Open `main
