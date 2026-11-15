import os
from results import calculate_total_and_average, assign_grade

def generate_class_statistics(students_dict):
    """"Calculate highest, lowest, and class average scores."""
    if not students_dict:
        return None

    averages = []
    for student in students_dict.values():
        _, avg = calculate_total_and_average(student.scores)
        if student.scores:
            averages.append(avg)

    if not averages:
        return None

    highest_avg = max(averages) 
    lowest_avg = min(averages)
    class_avg = round(sum(averages) / len(averages), 2)

    return{
        "highest_average": highest_avg,
        "lowest_average": lowest_avg,
        "class_average": class_avg,
        "total_students": len(students_dict)
    }

def generate_text_report(students_dict, filename="class_performance_report.txt"):
    """Generate a formatted text report of all students and class statistics and save to file."""
    stats = generate_class_statistics(students_dict)

    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("         STUDENT RESULT MANAGEMENT REPORT        ")
    report_lines.append("=" * 60)

    if stats:
        report_lines.append(f"Total Students: {stats['total_students']}")
        report_lines.append(f"Class Average Score: {stats['class_average']}")
        report_lines.append(f"Highest Average: {stats['highest_average']}")
        report_lines.append(f"Lowest Average: {stats['lowest_average']}")
    else:
        report_lines.append("No student record or scores available for statistics.")

    report_lines.append("-" * 60)
    report_lines.append(f"{'ID':<10} | {'Full Name':<20} | {'Total': <8} | {'Average':<8} | {'Grade':<5}")
    report_lines.append("-" * 60)

    for sid, student in students_dict.items():
        total, avg = calculate_total_and_average(student.scores)
        grade = assign_grade(avg) if student.scores else "N/A"
        report_lines.append(f"{'ID':<10} | {'Full Name':<20} | {'Total': <8} | {'Average':<8} | {'Grade':<5}")

    report_lines.append("=" * 60)

    report_content = "\n".join(report_lines)

    try:
        with open(filename,'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"\n[Success] Report successfully saved to '{filename}'!")
    except Exception as e:
        print(f"Error saving report file: {e}")

    return report_content