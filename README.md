# OSRMS - Online Student Results Management System

A Python-based GUI application for managing student results, built with Tkinter and SQLite.

## Features

- **User Authentication**: Secure login with admin credentials
- **Student Management**: Add and view student records with matric numbers
- **Course Management**: Add and manage course information
- **Results Tracking**: Record and view student scores for courses
- **Grade Calculation**: Automatic grade assignment based on scores
- **Student Transcripts**: View individual student results with statistics
- **Modern UI**: Clean, professional interface with color-coded elements

## Requirements

- Python 3.x
- tkinter (usually included with Python)
- sqlite3 (included with Python)

## Installation

1. Clone or download this repository
2. Ensure Python 3.x is installed on your system
3. No additional packages need to be installed

## Usage

### Running the Application

```bash
python osrms.py
```

### Login Credentials

Default admin credentials:

- **Username**: `admin`
- **Password**: `admin123`

### Main Features

#### Dashboard Menu

- **👥 Students**: View all registered students
- **📚 Courses**: View all available courses
- **📊 All Results**: View all student results with grades
- **🎓 Student Results**: View detailed results for a specific student
- **➕ Add Student**: Add a new student to the system
- **➕ Add Course**: Add a new course to the system
- **➕ Add Result**: Record a student's score for a course
- **🚪 Logout**: Exit and return to login screen

## Grade Scale

| Score Range | Grade |
| ----------- | ----- |
| 70 - 100    | A     |
| 60 - 69     | B     |
| 50 - 59     | C     |
| 45 - 49     | D     |
| Below 45    | F     |

## Database

The application uses SQLite with the following tables:

- **users**: Admin credentials
- **students**: Student information (matric_no, name)
- **courses**: Course details (code, title)
- **results**: Student scores (student_id, course_id, score)

## Sample Data

The application comes pre-populated with:

- 7 sample students
- 9 sample courses
- Random scores for all student-course combinations

## File Structure

```
osrms.py                 # Main application file
osrms_full.db           # SQLite database (created on first run)
README.md               # This file
```

## Author

Excel Jones
24/14574
Cyber Security
200L

## License

Open source - feel free to modify and distribute
