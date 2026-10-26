import mysql.connector

# Connect to MySQL
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="daksh1507"
)

cur = con.cursor()

# Create database and table
cur.execute("CREATE DATABASE IF NOT EXISTS student_result")
cur.execute("USE student_result")

cur.execute("""
CREATE TABLE IF NOT EXISTS results (
    roll_no INT PRIMARY KEY,
    name VARCHAR(100),
    marks FLOAT,
    grade VARCHAR(5)
)
""")

# Function to calculate grade
def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "F"

# Function to add student result
def add_result():
    try:
        roll = int(input("Enter Roll Number: "))
        name = input("Enter Student Name: ").strip()
        marks = float(input("Enter Marks (0-100): "))

        if not name or not 0 <= marks <= 100:
            print("Invalid name or marks!")
            return

        grade = calculate_grade(marks)

        cur.execute(
            "INSERT INTO results VALUES (%s, %s, %s, %s)",
            (roll, name, marks, grade)
        )
        con.commit()

        print("Student result added successfully!")

    except ValueError:
        print("Please enter valid numeric values.")
    except mysql.connector.IntegrityError:
        print("This roll number already exists.")

# Function to display all results
def view_results():
    cur.execute("SELECT * FROM results")
    records = cur.fetchall()

    if not records:
        print("No student results found.")
        return

    print("\n--- STUDENT RESULTS ---")
    for record in records:
        print(
            "Roll No:", record[0],
            "| Name:", record[1],
            "| Marks:", record[2],
            "| Grade:", record[3]
        )

# Function to search for a student
def search_result():
    try:
        roll = int(input("Enter Roll Number to search: "))

        cur.execute(
            "SELECT * FROM results WHERE roll_no = %s",
            (roll,)
        )
        record = cur.fetchone()

        if record:
            print("\nStudent Found!")
            print("Roll Number:", record[0])
            print("Name:", record[1])
            print("Marks:", record[2])
            print("Grade:", record[3])
        else:
            print("Student not found.")

    except ValueError:
        print("Enter a valid roll number.")

# Function to update student marks
def update_result():
    try:
        roll = int(input("Enter Roll Number: "))
        marks = float(input("Enter New Marks (0-100): "))

        if not 0 <= marks <= 100:
            print("Marks must be between 0 and 100.")
            return

        grade = calculate_grade(marks)

        cur.execute(
            "UPDATE results SET marks=%s, grade=%s WHERE roll_no=%s",
            (marks, grade, roll)
        )
        con.commit()

        if cur.rowcount > 0:
            print("Result updated successfully!")
        else:
            print("Student not found.")

    except ValueError:
        print("Please enter valid numeric values.")

# Main menu
while True:
    print("\n===== STUDENT RESULT MANAGEMENT SYSTEM =====")
    print("1. Add Student Result")
    print("2. View All Results")
    print("3. Search Student Result")
    print("4. Update Student Result")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_result()
    elif choice == "2":
        view_results()
    elif choice == "3":
        search_result()
    elif choice == "4":
        update_result()
    elif choice == "5":
        print("Thank you for using the system!")
        break
    else:
        print("Invalid choice. Please try again.")

cur.close()
con.close()
