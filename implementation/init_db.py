import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite')

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cohort TEXT NOT NULL,
        score REAL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        credits INTEGER NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_id INTEGER,
        status TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(course_id) REFERENCES courses(id)
    )
    ''')
    
    # Seed data
    students = [
        ('Alice Smith', 'A1', 95.5),
        ('Bob Jones', 'A1', 88.0),
        ('Charlie Brown', 'B2', 72.5),
        ('Diana Prince', 'A1', 98.0)
    ]
    cursor.executemany("INSERT INTO students (name, cohort, score) VALUES (?, ?, ?)", students)
    
    courses = [
        ('Database Systems', 4),
        ('Machine Learning', 4),
        ('Web Development', 3)
    ]
    cursor.executemany("INSERT INTO courses (title, credits) VALUES (?, ?)", courses)
    
    enrollments = [
        (1, 1, 'active'),
        (1, 2, 'active'),
        (2, 1, 'completed'),
        (3, 3, 'active'),
        (4, 2, 'completed')
    ]
    cursor.executemany("INSERT INTO enrollments (student_id, course_id, status) VALUES (?, ?, ?)", enrollments)
    
    conn.commit()
    conn.close()
    print("Database initialized with seed data.")

if __name__ == '__main__':
    init_db()
