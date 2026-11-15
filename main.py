from student import Student
from storage import load_data, save_data
from results import calculate_total_and_average, assign_grade
from reports import generate_class_statistics, generate_text_report

def main():
    #Load data at startup
    students = load_data()

    while True:
        print("\n==============================================")
        print("   STUDENT RESULT MANAGEMENT SYSTEM (SRMS)    ")
        print("==============================================")
        print("1. Add New Student")
        print("2. View All Registered Students")
        print("3. Search for a Student (ID or Name)")
        print("4. Update Student Information")
        print("5. Delete a Student Record")
        print("6. Record/Update Subject Scores (At least 5)")
        print("7. Display Individual Student Report Card")
        print("8. List Students with Totals, Averages, & Grades")
        print("9. View Class Statistics")
        print("10. Generate and Save Text Report")
        print("11. Exit & Save")
        
        choice = input("\nEnter your choice (1-11): ").strip()
        
        if choice == '1':
            print("\n--- Add New Student ---")
            sid = input("Enter Student ID (e.g., ST001): ").strip()
            if sid in students:
                print("Error: Student ID already exists!")
                continue
            name = input("Enter Full Name: ").strip()
            s_class = input("Enter Class/Form (e.g., SS2): ").strip()
            gender = input("Enter Gender: ").strip()
            dob = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
            
            students[sid] = Student(sid, name, s_class, gender, dob)
            save_data(students)
            print(f"[Success] Student {name} added successfully!")

        elif choice == '2':
            print("\n--- Registered Students ---")
            if not students:
                print("No students found.")
            else:
                for s in students.values():
                    print(f"ID: {s.student_id} | Name: {s.full_name} | Class: {s.student_class} | DOB: {s.dob}")

        elif choice == '3':
            query = input("\nEnter Student ID or Name to search: ").strip().lower()
            found = False
            for s in students.values():
                if query in s.student_id.lower() or query in s.full_name.lower():
                    print(f"\nFound -> ID: {s.student_id}, Name: {s.full_name}, Class: {s.student_class}, Gender: {s.gender}")
                    found = True
            if not found:
                print("No matching student found.")

        elif choice == '4':
            sid = input("\nEnter Student ID to update: ").strip()
            if sid not in students:
                print("Student ID not found.")
                continue
            s = students[sid]
            print(f"Updating details for {s.full_name}. Press Enter to skip a field.")
            new_name = input(f"New Name [{s.full_name}]: ").strip()
            new_class = input(f"New Class [{s.student_class}]: ").strip()
            new_gender = input(f"New Gender [{s.gender}]: ").strip()
            new_dob = input(f"New DOB [{s.dob}]: ").strip()
            
            s.update_info(
                full_name=new_name if new_name else None,
                student_class=new_class if new_class else None,
                gender=new_gender if new_gender else None,
                dob=new_dob if new_dob else None
            )
            save_data(students)
            print("[Success] Student information updated!")

        elif choice == '5':
            sid = input("\nEnter Student ID to delete: ").strip()
            if sid in students:
                del students[sid]
                save_data(students)
                print("[Success] Student record deleted.")
            else:
                print("Student ID not found.")

        elif choice == '6':
            sid = input("\nEnter Student ID to record/update scores: ").strip()
            if sid not in students:
                print("Student ID not found.")
                continue
            s = students[sid]
            print(f"Recording scores for {s.full_name} (Requirement: at least 5 subjects).")
            print("Type 'done' when finished entering subjects.")
            
            while True:
                subj = input("Enter Subject Name: ").strip()
                if subj.lower() == 'done':
                    break
                try:
                    score = float(input(f"Enter score for {subj} (0-100): "))
                    if 0 <= score <= 100:
                        s.scores[subj] = score
                        print(f"Recorded {subj}: {score}")
                    else:
                        print("Score must be between 0 and 100.")
                except ValueError:
                    print("Invalid input. Please enter a valid number for the score.")
            save_data(students)
            print("[Success] Scores saved!")

        elif choice == '7':
            sid = input("\nEnter Student ID for Report Card: ").strip()
            if sid not in students:
                print("Student ID not found.")
                continue
            s = students[sid]
            total, avg = calculate_total_and_average(s.scores)
            grade = assign_grade(avg) if s.scores else "N/A"
            
            print("\n" + "="*40)
            print(f"       STUDENT REPORT CARD - {s.student_class}")
            print("="*40)
            print(f"ID: {s.student_id} | Name: {s.full_name}")
            print(f"Gender: {s.gender} | DOB: {s.dob}")
            print("-" * 40)
            print(f"{'Subject':<20} | {'Score':<10}")
            print("-" * 40)
            for subj, scr in s.scores.items():
                print(f"{subj:<20} | {scr:<10}")
            print("-" * 40)
            print(f"Total Score: {total}")
            print(f"Average Score: {avg}")
            print(f"Overall Grade: {grade}")
            print("="*40)

        elif choice == '8':
            print("\n--- Student Performance List (Sorted by Average) ---")
            if not students:
                print("No students registered.")
                continue
            
            # Sort students by average score (highest to lowest)
            sorted_students = sorted(
                students.values.item() if hasattr(students.values, '__iter__') else list(students.values()),
                key=lambda x: calculate_total_and_average(x.scores)[1],
                reverse=True
            )
            
            print(f"{'ID':<10} | {'Name':<20} | {'Total':<8} | {'Average':<8} | {'Grade':<5}")
            print("-" * 60)
            for s in sorted_students:
                total, avg = calculate_total_and_average(s.scores)
                grade = assign_grade(avg) if s.scores else "N/A"
                print(f"{s.student_id:<10} | {s.full_name:<20} | {total:<8} | {avg:<8} | {grade:<5}")

        elif choice == '9':
            print("\n--- Class Statistics ---")
            stats = generate_class_statistics(students)
            if not stats:
                print("Not enough data to calculate statistics.")
            else:
                print(f"Total Students: {stats['total_students']}")
                print(f"Class Average Score: {stats['class_average']}")
                print(f"Highest Average: {stats['highest_average']}")
                print(f"Lowest Average: {stats['lowest_average']}")

        elif choice == '10':
            generate_text_report(students)

        elif choice == '11':
            save_data(students)
            print("\nData saved successfully. Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose between 1 and 11.")

if __name__ == "__main__":
    import sys
    print("Select Interface:")
    print("1. Console Mode (Terminal)")
    print("2. Graphical Mode (GUI Tkinter)")
    mode = input("Enter choice (1 or 2): ").strip()
    
    if mode == '2':
        import tkinter as tk
        from gui import StudentResultApp
        root = tk.Tk()
        app = StudentResultApp(root)
        root.mainloop()
    else:
        main()