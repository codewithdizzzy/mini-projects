# Student Grade Management System
# This program stores student information and grades using lists and dictionaries.

students = []


def create_student(student_id, name, class_name):
    """Add a new student to the list."""
    for student in students:
        if student["student_id"] == student_id:
            print("A student with this ID already exists.")
            return False

    students.append({
        "student_id": student_id,
        "name": name,
        "class_name": class_name,
        "grades": []
    })
    print(f"Student {name} was added successfully.")
    return True


def find_student(student_id):
    """Return the matching student dictionary, or None."""
    for student in students:
        if student["student_id"] == student_id:
            return student
    return None


def add_grade(student_id, subject, grade):
    """Add a grade to a student's grade list."""
    student = find_student(student_id)
    if student is None:
        print("Student not found.")
        return

    if not 0 <= grade <= 100:
        print("Grade must be between 0 and 100.")
        return

    student["grades"].append({"subject": subject, "grade": grade})
    print(f"Grade {grade} added for {subject}.")


def calculate_average(student_id):
    """Calculate the average of all grades for a student."""
    student = find_student(student_id)
    if student is None:
        print("Student not found.")
        return

    if not student["grades"]:
        print("No grades have been entered for this student.")
        return

    total = sum(item["grade"] for item in student["grades"])
    average = total / len(student["grades"])
    print(f"Average grade: {average:.2f}")


def show_student_report(student_id):
    """Display a student's details and all of their grades."""
    student = find_student(student_id)
    if student is None:
        print("Student not found.")
        return

    print(f"\nStudent ID: {student['student_id']}")
    print(f"Name: {student['name']}")
    print(f"Class: {student['class_name']}")
    print("Grades:")

    if not student["grades"]:
        print("  No grades entered.")
        return

    for item in student["grades"]:
        print(f"  - {item['subject']}: {item['grade']}%)")

    total = sum(item["grade"] for item in student["grades"])
    average = total / len(student["grades"])
    print(f"Average: {average:.2f}%")


def list_students():
    """Display all students currently stored in the system."""
    if not students:
        print("No students have been added.")
        return

    print("\nStudent List")
    for student in students:
        print(f"- {student['student_id']} | {student['name']} | {student['class_name']}")


def remove_student(student_id):
    """Remove a student from the list."""
    for index, student in enumerate(students):
        if student["student_id"] == student_id:
            students.pop(index)
            print("Student removed.")
            return
    print("Student not found.")


def remove_grade(student_id, subject):
    """Remove a grade from a student's records."""
    student = find_student(student_id)
    if student is None:
        print("Student not found.")
        return

    for index, item in enumerate(student["grades"]):
        if item["subject"].lower() == subject.lower():
            student["grades"].pop(index)
            print("Grade removed.")
            return
    print("No grade was found for that subject.")


def get_user_input(prompt, default=None):
    """Ask for input and return the entered value."""
    if default is not None:
        answer = input(f"{prompt} [{default}]: ")
        return answer if answer.strip() else default
    return input(f"{prompt}: ").strip()


def main():
    print("========================================")
    print("Student Grade Management System")
    print("========================================")

    while True:
        print("\n1. Add student")
        print("2. Add grade")
        print("3. View student report")
        print("4. Calculate average")
        print("5. List students")
        print("6. Remove grade")
        print("7. Remove student")
        print("8. Exit")

        choice = get_user_input("Choose an option")

        if choice == "1":
            student_id = get_user_input("Student ID")
            name = get_user_input("Student name")
            class_name = get_user_input("Class")
            if student_id and name and class_name:
                create_student(student_id, name, class_name)

        elif choice == "2":
            student_id = get_user_input("Student ID")
            subject = get_user_input("Subject")
            grade_text = get_user_input("Grade from 0 to 100")
            try:
                grade = float(grade_text)
                add_grade(student_id, subject, grade)
            except ValueError:
                print("Grade must be a number.")

        elif choice == "3":
            student_id = get_user_input("Student ID")
            show_student_report(student_id)

        elif choice == "4":
            student_id = get_user_input("Student ID")
            calculate_average(student_id)

        elif choice == "5":
            list_students()

        elif choice == "6":
            student_id = get_user_input("Student ID")
            subject = get_user_input("Subject to remove")
            remove_grade(student_id, subject)

        elif choice == "7":
            student_id = get_user_input("Student ID")
            remove_student(student_id)

        elif choice == "8":
            print("Thank you for using the Student Grade Management System.")
            break

        else:
            print("Invalid option. Please choose a number from 1 to 8.")


if __name__ == "__main__":
    main()
