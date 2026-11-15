import os
import json
from student import Student

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "students.json")

def save_data(students_dict):
    """Save all student records to a JSON file."""
    try:
        if not  os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        data_to_save = {sid: student.to_dict() for sid, student in students_dict.items()}
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

def load_data():
    """"Load student records from JSON file. Returns a dictionary of Student objects."""
    students_dict = {}
    if not os.path.exists(DATA_FILE):
        return students_dict

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for sid, s_data in data.items():
                students_dict[sid] = Student.from_dict(s_data)
    except Exception as e:
        print(f"Error loading data: {e}")

    return students_dict