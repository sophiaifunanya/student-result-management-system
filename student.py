from datetime import datetime

class Student:
    def __init__(self, student_id, full_name, student_class, gender, dob):
        self.student_id = student_id
        self.full_name = full_name
        self.student_class = student_class
        self.gender = gender
        self.dob = dob
        #Dictionary to store subject scores, e.g., {'Math': 85, 'English': 78, ...}
        self.scores = {}
        self.date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

    def update_info(self, full_name=None, student_class=None, gender=None, dob=None):
        if full_name:
            self.full_name = full_name
        if student_class:
            self.student_class = student_class
        if gender:
            self.gender = gender
        if dob:
            self.dob = dob

    def to_dict(self):
        """Convert student object to dictionary for JSON serialization."""
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "student_class": self.student_class,
            "gender": self.gender,
            "dob": self.dob,
            "scores": self.scores,
            "date_added": self.date_added
        }

    @classmethod
    def from_dict(cls, data):
        """Create as student object from a dictionary."""
        student = cls(
            data["student_id"],
            data["full_name"],
            data["student_class"],
            data["gender"],
            data["dob"]
        )
        student.scores = data.get("scores", {})
        student.date_added = data.get("date_added", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return student