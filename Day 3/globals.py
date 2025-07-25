import json
import os
STUDENT_FILE = "students.json"
def load_students():
    """Load students from file"""
    if os.path.exists(STUDENT_FILE):
        try:
            with open(STUDENT_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}
def save_students(student_dict):
    """Save students to file"""
    with open(STUDENT_FILE, 'w') as f:
        json.dump(student_dict, f, indent=2)
# Load existing data
student = load_students()