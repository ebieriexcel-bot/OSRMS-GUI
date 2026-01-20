# OSRMS GUI Version - Enhanced UI
# Author: Excel Jones


import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import random

DATABASE = "osrms_full.db"

# Color Scheme
PRIMARY_COLOR = "#2C3E50"
SECONDARY_COLOR = "#3498DB"
SUCCESS_COLOR = "#27AE60"
ACCENT_COLOR = "#E74C3C"
BG_COLOR = "#ECF0F1"
TEXT_COLOR = "#2C3E50"

# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matric_no TEXT,
        name TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT,
        title TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_id INTEGER,
        score INTEGER
    )
    """)

    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchall():
        cur.execute("INSERT INTO users (username, password) VALUES ('admin','admin123')")

        students = [
            ('CSC001','John Doe'),
            ('CSC002','Mary Smith'),
            ('CSC003','Alice Johnson'),
            ('CSC004','Bob Williams'),
            ('CSC005','Carol Davis'),
            ('CSC006','David Brown'),
            ('CSC007','Eva Wilson')
        ]
        for s in students:
            cur.execute("INSERT INTO students (matric_no, name) VALUES (?,?)", s)

        courses = [
            ('CSC101','Intro to Computing'),
            ('CSC102','Data Structures'),
            ('CSC103','Algorithms'),
            ('CSC104','Databases'),
            ('CSC105','Computer Networks'),
            ('CSC106','Operating Systems'),
            ('CSC107','Software Engineering'),
            ('CSC108','Artificial Intelligence'),
            ('CSC109','Web Development')
        ]
        for c in courses:
            cur.execute("INSERT INTO courses (code, title) VALUES (?,?)", c)

        cur.execute("SELECT id FROM students")
        student_ids = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT id FROM courses")
        course_ids = [row[0] for row in cur.fetchall()]

        for sid in student_ids:
            for cid in course_ids:
                score = random.randint(40,100)
                cur.execute("INSERT INTO results (student_id, course_id, score) VALUES (?,?,?)", (sid, cid, score))

    conn.commit()
    conn.close()

def calculate_grade(score):
    if score >= 70:
        return 'A'
    elif score >= 60:
        return 'B'
    elif score >= 50:
        return 'C'
    elif score >= 45:
        return 'D'
    else:
        return 'F'

# --------------- GUI APPLICATION ---------------
class OSRMSAPP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OSRMS - Student Results Management")
        self.geometry("1000x700")
        self.configure(bg=BG_COLOR)
        self.resizable(True, True)
        
        # Configure styles
        self.setup_styles()
        init_db()
        self.show_login_screen()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Login button style
        style.configure('Login.TButton', font=('Segoe UI', 11, 'bold'), padding=10)
        style.map('Login.TButton',
                  background=[('active', SECONDARY_COLOR)],
                  foreground=[('active', 'white')])
        
        # Menu button style
        style.configure('Menu.TButton', font=('Segoe UI', 10), padding=8)
        style.map('Menu.TButton',
                  background=[('active', SECONDARY_COLOR)],
                  foreground=[('active', 'white')])
        
        # Action button style
        style.configure('Action.TButton', font=('Segoe UI', 9), padding=6)
        
        # Label style
        style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), background=BG_COLOR, foreground=PRIMARY_COLOR)
        style.configure('Heading.TLabel', font=('Segoe UI', 16, 'bold'), background=BG_COLOR, foreground=PRIMARY_COLOR)
        style.configure('TLabel', font=('Segoe UI', 10), background=BG_COLOR, foreground=TEXT_COLOR)
        
        # Entry style
        style.configure('TEntry', font=('Segoe UI', 10), padding=8)

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_window()
        
        # Header
        header = tk.Frame(self, bg=PRIMARY_COLOR, height=120)
        header.pack(fill=tk.X)
        
        ttk.Label(header, text="OSRMS", font=('Segoe UI', 32, 'bold'), 
                 background=PRIMARY_COLOR, foreground='white').pack(pady=20)
        ttk.Label(header, text="Online Student Results Management System", 
                 font=('Segoe UI', 11), background=PRIMARY_COLOR, foreground='#BDC3C7').pack()

        # Main content
        main_frame = ttk.Frame(self, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Center login box
        login_box = ttk.Frame(main_frame)
        login_box.pack(expand=True)

        ttk.Label(login_box, text="Admin Login", style='Heading.TLabel').pack(pady=20)

        # Username
        ttk.Label(login_box, text="Username").pack(anchor=tk.W, pady=(10, 0))
        username_entry = ttk.Entry(login_box, width=40)
        username_entry.pack(pady=5, fill=tk.X, ipady=8)

        # Password
        ttk.Label(login_box, text="Password").pack(anchor=tk.W, pady=(10, 0))
        password_entry = ttk.Entry(login_box, width=40, show="•")
        password_entry.pack(pady=5, fill=tk.X, ipady=8)

        def login():
            username = username_entry.get()
            password = password_entry.get()

            if not username or not password:
                messagebox.showwarning("Warning", "Please enter username and password!")
                return

            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cur.fetchone()
            conn.close()

            if user:
                self.show_main_menu()
            else:
                messagebox.showerror("Error", "Invalid credentials!")
                password_entry.delete(0, tk.END)

        btn_frame = ttk.Frame(login_box)
        btn_frame.pack(pady=30, fill=tk.X)
        ttk.Button(btn_frame, text="Login", command=login, style='Login.TButton', width=20).pack()

    def show_main_menu(self):
        self.clear_window()
        
        # Header
        header = tk.Frame(self, bg=SECONDARY_COLOR, height=80)
        header.pack(fill=tk.X)
        
        ttk.Label(header, text="Dashboard", font=('Segoe UI', 28, 'bold'), 
                 background=SECONDARY_COLOR, foreground='white').pack(pady=15)

        # Sidebar + Content
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        sidebar = tk.Frame(container, bg=PRIMARY_COLOR, width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(sidebar, text="Menu", font=('Segoe UI', 14, 'bold'), 
                 background=PRIMARY_COLOR, foreground='white').pack(pady=20, padx=10, anchor=tk.W)

        # Menu buttons
        menu_buttons = [
            ("👥 Students", self.view_students),
            ("📚 Courses", self.view_courses),
            ("📊 All Results", self.view_results),
            ("🎓 Student Results", self.view_individual_student),
            ("➕ Add Student", self.add_student),
            ("➕ Add Course", self.add_course),
            ("➕ Add Result", self.add_result),
            ("🚪 Logout", self.show_login_screen),
        ]

        for btn_text, cmd in menu_buttons:
            btn = tk.Button(sidebar, text=btn_text, command=cmd, 
                           bg=PRIMARY_COLOR, fg='white', font=('Segoe UI', 10),
                           relief=tk.FLAT, anchor=tk.W, padx=20, pady=12,
                           activebackground=SECONDARY_COLOR, activeforeground='white',
                           cursor='hand2', bd=0)
            btn.pack(fill=tk.X, padx=5, pady=3)

        # Content area
        content = ttk.Frame(container)
        content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(content, text="Welcome to OSRMS", style='Heading.TLabel').pack(pady=20)
        
        info_text = """
        📋 Quick Stats:
        
        • Manage student records
        • Track course information  
        • View and update results
        • Generate student transcripts
        
        Select an option from the menu to get started.
        """
        
        ttk.Label(content, text=info_text, justify=tk.LEFT, 
                 font=('Segoe UI', 11)).pack(anchor=tk.W, pady=20)

    def view_students(self):
        self.clear_window()
        self._show_table_screen("All Students", "students", 
                               ["ID", "Matric No", "Name"],
                               ["ID", "Matric No", "Name"])

    def view_courses(self):
        self.clear_window()
        self._show_table_screen("All Courses", "courses",
                               ["ID", "Code", "Title"],
                               ["ID", "Code", "Title"])

    def view_results(self):
        self.clear_window()
        
        # Header
        header = tk.Frame(self, bg=SECONDARY_COLOR, height=80)
        header.pack(fill=tk.X)
        ttk.Label(header, text="All Results", font=('Segoe UI', 28, 'bold'), 
                 background=SECONDARY_COLOR, foreground='white').pack(pady=15)

        # Content
        content = ttk.Frame(self, padding="20")
        content.pack(fill=tk.BOTH, expand=True)

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("""
        SELECT students.matric_no, students.name, courses.code, courses.title, results.score
        FROM results
        JOIN students ON results.student_id = students.id
        JOIN courses ON results.course_id = courses.id
        ORDER BY students.id, courses.id
        """)
        results = cur.fetchall()
        conn.close()

        # Treeview
        tree = ttk.Treeview(content, columns=("Matric", "Name", "Code", "Title", "Score", "Grade"), 
                           height=20, show='tree headings')
        tree.column("#0", width=0)
        tree.column("Matric", width=100)
        tree.column("Name", width=150)
        tree.column("Code", width=100)
        tree.column("Title", width=200)
        tree.column("Score", width=80)
        tree.column("Grade", width=80)

        tree.heading("Matric", text="Matric No")
        tree.heading("Name", text="Name")
        tree.heading("Code", text="Code")
        tree.heading("Title", text="Title")
        tree.heading("Score", text="Score")
        tree.heading("Grade", text="Grade")

        for r in results:
            grade = calculate_grade(r[4])
            tree.insert("", tk.END, values=(r[0], r[1], r[2], r[3], r[4], grade))

        # Scrollbar
        scrollbar = ttk.Scrollbar(content, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        # Back button
        ttk.Button(self, text="← Back to Menu", command=self.show_main_menu).pack(pady=10)

    def _show_table_screen(self, title, table_name, columns, headings):
        # Header
        header = tk.Frame(self, bg=SECONDARY_COLOR, height=80)
        header.pack(fill=tk.X)
        ttk.Label(header, text=title, font=('Segoe UI', 28, 'bold'), 
                 background=SECONDARY_COLOR, foreground='white').pack(pady=15)

        # Content
        content = ttk.Frame(self, padding="20")
        content.pack(fill=tk.BOTH, expand=True)

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        data = cur.fetchall()
        conn.close()

        # Treeview
        tree = ttk.Treeview(content, columns=columns, height=20, show='tree headings')
        tree.column("#0", width=0)
        
        col_width = 300 // len(columns)
        for col in columns:
            tree.column(col, width=col_width)
            tree.heading(col, text=col)

        for row in data:
            tree.insert("", tk.END, values=row)

        scrollbar = ttk.Scrollbar(content, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        ttk.Button(self, text="← Back to Menu", command=self.show_main_menu).pack(pady=10)

    def view_individual_student(self):
        self.clear_window()
        
        # Header
        header = tk.Frame(self, bg=SECONDARY_COLOR, height=80)
        header.pack(fill=tk.X)
        ttk.Label(header, text="Student Results", font=('Segoe UI', 28, 'bold'), 
                 background=SECONDARY_COLOR, foreground='white').pack(pady=15)

        # Content
        content = ttk.Frame(self, padding="30")
        content.pack(fill=tk.BOTH, expand=True)

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT id, matric_no, name FROM students ORDER BY name")
        students = cur.fetchall()
        conn.close()

        # Selection
        select_frame = ttk.Frame(content)
        select_frame.pack(fill=tk.X, pady=15)

        ttk.Label(select_frame, text="Select Student:", style='Heading.TLabel').pack(anchor=tk.W)
        
        student_var = tk.StringVar()
        student_combo = ttk.Combobox(select_frame, textvariable=student_var, width=50, 
                                     font=('Segoe UI', 11), state='readonly')
        student_combo['values'] = [f"{s[1]} - {s[2]}" for s in students]
        student_combo.pack(pady=10, fill=tk.X, ipady=8)

        # Results frame
        results_frame = ttk.Frame(content)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        def show_results():
            selected = student_var.get()
            if not selected:
                messagebox.showwarning("Warning", "Please select a student!")
                return

            student_id = None
            for s in students:
                if f"{s[1]} - {s[2]}" == selected:
                    student_id = s[0]
                    break

            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("""
            SELECT courses.code, courses.title, results.score
            FROM results
            JOIN courses ON results.course_id = courses.id
            WHERE results.student_id=?
            ORDER BY courses.code
            """, (student_id,))
            results = cur.fetchall()
            conn.close()

            for widget in results_frame.winfo_children():
                widget.destroy()

            if not results:
                ttk.Label(results_frame, text="No results found!", style='Heading.TLabel').pack(pady=20)
                return

            tree = ttk.Treeview(results_frame, columns=("Code", "Title", "Score", "Grade"), 
                               height=15, show='tree headings')
            tree.column("#0", width=0)
            tree.column("Code", width=100)
            tree.column("Title", width=250)
            tree.column("Score", width=100)
            tree.column("Grade", width=100)

            tree.heading("Code", text="Code")
            tree.heading("Title", text="Title")
            tree.heading("Score", text="Score")
            tree.heading("Grade", text="Grade")

            total = 0
            for r in results:
                grade = calculate_grade(r[2])
                tree.insert("", tk.END, values=(r[0], r[1], r[2], grade))
                total += r[2]

            tree.pack(fill=tk.BOTH, expand=True)

            average = total / len(results)
            stats_frame = ttk.Frame(results_frame)
            stats_frame.pack(fill=tk.X, pady=15)
            
            ttk.Label(stats_frame, text=f"Total Score: {total}  |  Average: {average:.2f}  |  Courses: {len(results)}", 
                     font=('Segoe UI', 11, 'bold'), foreground=SECONDARY_COLOR).pack()

        ttk.Button(content, text="Show Results", command=show_results, width=20).pack(pady=10)
        ttk.Button(self, text="← Back to Menu", command=self.show_main_menu).pack(pady=10)

    def add_student(self):
        self._show_add_form("Add Student", [
            ("Matric No", "matric_no"),
            ("Student Name", "name")
        ], "students", self._add_student_db)

    def add_course(self):
        self._show_add_form("Add Course", [
            ("Course Code", "code"),
            ("Course Title", "title")
        ], "courses", self._add_course_db)

    def _show_add_form(self, title, fields, table, callback):
        self.clear_window()
        
        # Header
        header = tk.Frame(self, bg=SECONDARY_COLOR, height=80)
        header.pack(fill=tk.X)
        ttk.Label(header, text=title, font=('Segoe UI', 28, 'bold'), 
                 background=SECONDARY_COLOR, foreground='white').pack(pady=15)

        # Content
        content = ttk.Frame(self, padding="40")
        content.pack(fill=tk.BOTH, expand=True)

        # Form
        form_frame = ttk.Frame(content)
        form_frame.pack(expand=True)

        entries = {}
        for label, field_name in fields:
            ttk.Label(form_frame, text=label, style='Heading.TLabel').pack(anchor=tk.W, pady=(15, 5))
            entry = ttk.Entry(form_frame, width=40)
            entry.pack(pady=5, fill=tk.X, ipady=10)
            entries[field_name] = entry

        def save():
            data = {k: v.get() for k, v in entries.items()}
            
            if not all(data.values()):
                messagebox.showwarning("Warning", "All fields are required!")
                return
            
            callback(data)

        button_frame = ttk.Frame(content)
        button_frame.pack(pady=30)
        
        ttk.Button(button_frame, text="Save", command=save, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.show_main_menu, width=15).pack(side=tk.LEFT, padx=5)

    def _add_student_db(self, data):
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("INSERT INTO students (matric_no, name) VALUES (?,?)", 
                   (data['matric_no'], data['name']))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student added successfully!")
        self.show_main_menu()

    def _add_course_db(self, data):
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("INSERT INTO courses (code, title) VALUES (?,?)", 
                   (data['code'], data['title']))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Course added successfully!")
        self.show_main_menu()

    def add_result(self):
        self.clear_window()
        
        # Header
        header = tk.Frame(self, bg=SECONDARY_COLOR, height=80)
        header.pack(fill=tk.X)
        ttk.Label(header, text="Add Result", font=('Segoe UI', 28, 'bold'), 
                 background=SECONDARY_COLOR, foreground='white').pack(pady=15)

        # Content
        content = ttk.Frame(self, padding="40")
        content.pack(fill=tk.BOTH, expand=True)

        form_frame = ttk.Frame(content)
        form_frame.pack(expand=True, fill=tk.BOTH)

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT id, matric_no, name FROM students ORDER BY name")
        students = cur.fetchall()
        cur.execute("SELECT id, code, title FROM courses ORDER BY code")
        courses = cur.fetchall()
        conn.close()

        ttk.Label(form_frame, text="Select Student", style='Heading.TLabel').pack(anchor=tk.W, pady=(10, 5))
        student_var = tk.StringVar()
        student_combo = ttk.Combobox(form_frame, textvariable=student_var, width=50, state='readonly')
        student_combo['values'] = [f"{s[1]} - {s[2]}" for s in students]
        student_combo.pack(pady=10, fill=tk.X, ipady=8)

        ttk.Label(form_frame, text="Select Course", style='Heading.TLabel').pack(anchor=tk.W, pady=(15, 5))
        course_var = tk.StringVar()
        course_combo = ttk.Combobox(form_frame, textvariable=course_var, width=50, state='readonly')
        course_combo['values'] = [f"{c[1]} - {c[2]}" for c in courses]
        course_combo.pack(pady=10, fill=tk.X, ipady=8)

        ttk.Label(form_frame, text="Score (0-100)", style='Heading.TLabel').pack(anchor=tk.W, pady=(15, 5))
        score_entry = ttk.Entry(form_frame, width=50)
        score_entry.pack(pady=10, fill=tk.X, ipady=8)

        def save_result():
            if not student_var.get() or not course_var.get() or not score_entry.get():
                messagebox.showwarning("Warning", "All fields are required!")
                return

            try:
                score = int(score_entry.get())
                if score < 0 or score > 100:
                    messagebox.showerror("Error", "Score must be between 0 and 100!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Score must be a number!")
                return

            student_id = None
            for s in students:
                if f"{s[1]} - {s[2]}" == student_var.get():
                    student_id = s[0]
                    break

            course_id = None
            for c in courses:
                if f"{c[1]} - {c[2]}" == course_var.get():
                    course_id = c[0]
                    break

            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("INSERT INTO results (student_id, course_id, score) VALUES (?,?,?)", 
                       (student_id, course_id, score))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Result added successfully!")
            self.show_main_menu()

        button_frame = ttk.Frame(content)
        button_frame.pack(pady=30)
        
        ttk.Button(button_frame, text="Save", command=save_result, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.show_main_menu, width=15).pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    app = OSRMSAPP()
    app.mainloop()
