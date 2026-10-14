import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector


# ============================================================
# DATABASE CONNECTION
# Set MYSQL_PASSWORD in your terminal before running the app.
# ============================================================

def connect_db():
    password = os.environ.get("MYSQL_PASSWORD")
    if password is None:
        raise mysql.connector.Error(
            "MYSQL_PASSWORD is not set. In the VS Code PowerShell terminal, run:\n"
            '$env:MYSQL_PASSWORD="your MySQL password"\n'
            "Then run: python app.py"
        )

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="learning_progress",
    )


def run_query(query, values=None, fetch=True):
    connection = None
    cursor = None
    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute(query, values or ())

        if fetch:
            return cursor.fetchall()

        connection.commit()
        return True

    except mysql.connector.Error as error:
        if connection and not fetch:
            connection.rollback()
        messagebox.showerror("Database Error", str(error), parent=root)
        return None

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# ============================================================
# APP THEME
# ============================================================

BG = "#0B1120"          # Main window
SIDEBAR = "#101827"     # Navigation panel
PANEL = "#172338"       # Cards and tables
PANEL_LIGHT = "#1E2D45"  # Subtle highlight
ACCENT = "#6366F1"       # Indigo
ACCENT_HOVER = "#818CF8"
TEAL = "#2DD4BF"
CYAN = "#38BDF8"
GREEN = "#34D399"
AMBER = "#FBBF24"
WHITE = "#F8FAFC"
MUTED = "#9AAAC0"
BORDER = "#2B3A52"
ROW_ALT = "#1B2A40"

root = tk.Tk()
root.title("Learning Progress Management System")
root.geometry("1380x850")
root.minsize(1120, 700)
root.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background=BG)
style.configure("TLabel", background=BG, foreground=WHITE, font=("Segoe UI", 10))

style.configure(
    "Treeview",
    background=PANEL,
    foreground=WHITE,
    fieldbackground=PANEL,
    rowheight=35,
    borderwidth=0,
    font=("Segoe UI", 10),
)
style.configure(
    "Treeview.Heading",
    background=ACCENT,
    foreground=WHITE,
    padding=(10, 11),
    font=("Segoe UI", 10, "bold"),
    relief="flat",
)
style.map(
    "Treeview",
    background=[("selected", "#4546A8")],
    foreground=[("selected", WHITE)],
)
style.map("Treeview.Heading", background=[("active", ACCENT_HOVER)])

style.configure(
    "Accent.TButton",
    background=ACCENT,
    foreground=WHITE,
    padding=(15, 10),
    font=("Segoe UI", 9, "bold"),
    borderwidth=0,
    focuscolor=ACCENT,
)
style.map(
    "Accent.TButton",
    background=[("pressed", "#4F46E5"), ("active", ACCENT_HOVER)],
    foreground=[("disabled", MUTED)],
)

style.configure(
    "Secondary.TButton",
    background=PANEL_LIGHT,
    foreground=WHITE,
    padding=(14, 10),
    font=("Segoe UI", 9, "bold"),
    borderwidth=0,
    focuscolor=PANEL_LIGHT,
)
style.map(
    "Secondary.TButton",
    background=[("pressed", BORDER), ("active", "#30415C")],
)

style.configure(
    "Nav.TButton",
    background=SIDEBAR,
    foreground=MUTED,
    padding=(15, 13),
    anchor="w",
    font=("Segoe UI", 10, "bold"),
    borderwidth=0,
    focuscolor=SIDEBAR,
)
style.map(
    "Nav.TButton",
    background=[("pressed", PANEL_LIGHT), ("active", PANEL_LIGHT)],
    foreground=[("active", WHITE)],
)
style.configure(
    "NavActive.TButton",
    background=ACCENT,
    foreground=WHITE,
    padding=(15, 13),
    anchor="w",
    font=("Segoe UI", 10, "bold"),
    borderwidth=0,
    focuscolor=ACCENT,
)
style.map(
    "NavActive.TButton",
    background=[("pressed", ACCENT), ("active", ACCENT_HOVER)],
    foreground=[("active", WHITE)],
)

style.configure(
    "Vertical.TScrollbar",
    background=PANEL_LIGHT,
    troughcolor=BG,
    borderwidth=0,
    arrowsize=12,
)
style.configure(
    "Horizontal.TScrollbar",
    background=PANEL_LIGHT,
    troughcolor=BG,
    borderwidth=0,
    arrowsize=12,
)


# ============================================================
# GENERAL UI HELPERS
# ============================================================

def ui_label(parent, text, size=10, bold=False, fg=WHITE, bg=BG, **kwargs):
    font = ("Segoe UI", size, "bold" if bold else "normal")
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kwargs)


def ask_integer(title, prompt, minimum=1):
    return simpledialog.askinteger(title, prompt, parent=root, minvalue=minimum)


def ask_text(title, prompt):
    value = simpledialog.askstring(title, prompt, parent=root)
    if value is None:
        return None
    value = value.strip()
    if not value:
        messagebox.showwarning("Invalid Input", "This field cannot be empty.", parent=root)
        return None
    return value


def create_table(parent, columns, headings=None, widths=None, height=12):
    """Create a dark, striped data table with vertical and horizontal scrolling."""
    outer = tk.Frame(
        parent,
        bg=PANEL,
        highlightbackground=BORDER,
        highlightthickness=1,
    )
    outer.pack(fill="both", expand=True, padx=24, pady=(0, 22))

    table_wrap = tk.Frame(outer, bg=PANEL)
    table_wrap.pack(fill="both", expand=True, padx=1, pady=1)

    table = ttk.Treeview(
        table_wrap,
        columns=columns,
        show="headings",
        height=height,
    )

    for index, column in enumerate(columns):
        heading = headings[index] if headings else str(column).replace("_", " ").title()
        width = widths[index] if widths and index < len(widths) else 150
        table.heading(column, text=heading)
        table.column(column, width=width, minwidth=75, anchor="center", stretch=True)

    table.tag_configure("even", background=PANEL, foreground=WHITE)
    table.tag_configure("odd", background=ROW_ALT, foreground=WHITE)

    y_scroll = ttk.Scrollbar(table_wrap, orient="vertical", command=table.yview)
    x_scroll = ttk.Scrollbar(outer, orient="horizontal", command=table.xview)
    table.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

    table.grid(row=0, column=0, sticky="nsew")
    y_scroll.grid(row=0, column=1, sticky="ns")
    table_wrap.grid_rowconfigure(0, weight=1)
    table_wrap.grid_columnconfigure(0, weight=1)
    x_scroll.pack(fill="x", side="bottom")
    return table


def fill_table(table, records):
    for item in table.get_children():
        table.delete(item)
    if not records:
        return
    for index, record in enumerate(records):
        table.insert("", tk.END, values=record, tags=("even" if index % 2 == 0 else "odd",))


def make_action_bar(parent):
    bar = tk.Frame(parent, bg=BG)
    bar.pack(fill="x", padx=24, pady=(20, 14))
    return bar


def add_action_button(parent, text, command, primary=False):
    return ttk.Button(
        parent,
        text=text,
        command=command,
        style="Accent.TButton" if primary else "Secondary.TButton",
    )


# ============================================================
# MAIN SHELL: SIDEBAR + CONTENT AREA
# ============================================================

shell = tk.Frame(root, bg=BG)
shell.pack(fill="both", expand=True)

sidebar = tk.Frame(shell, bg=SIDEBAR, width=245)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

brand = tk.Frame(sidebar, bg=SIDEBAR)
brand.pack(fill="x", padx=20, pady=(25, 30))

logo = tk.Frame(brand, bg=ACCENT, width=48, height=48)
logo.pack(side="left", padx=(0, 12))
logo.pack_propagate(False)
ui_label(logo, "LP", size=16, bold=True, fg=WHITE, bg=ACCENT).place(relx=0.5, rely=0.5, anchor="center")

brand_text = tk.Frame(brand, bg=SIDEBAR)
brand_text.pack(side="left", fill="x", expand=True)
ui_label(brand_text, "LEARNFLOW", size=14, bold=True, fg=WHITE, bg=SIDEBAR).pack(anchor="w")
ui_label(brand_text, "PROGRESS MANAGER", size=8, bold=True, fg=TEAL, bg=SIDEBAR).pack(anchor="w", pady=(3, 0))

ui_label(sidebar, "WORKSPACE", size=8, bold=True, fg="#64748B", bg=SIDEBAR).pack(anchor="w", padx=23, pady=(0, 10))

main_area = tk.Frame(shell, bg=BG)
main_area.pack(side="left", fill="both", expand=True)

# Main header
header = tk.Frame(main_area, bg=BG, height=92)
header.pack(fill="x", padx=30, pady=(22, 8))
header.pack_propagate(False)

header_left = tk.Frame(header, bg=BG)
header_left.pack(side="left", fill="y")
current_title = ui_label(header_left, "Dashboard", size=22, bold=True, fg=WHITE, bg=BG)
current_title.pack(anchor="w")
current_subtitle = ui_label(
    header_left,
    "A clear overview of your online learning data.",
    size=10,
    fg=MUTED,
    bg=BG,
)
current_subtitle.pack(anchor="w", pady=(5, 0))

header_right = tk.Frame(header, bg=BG)
header_right.pack(side="right", anchor="ne", pady=4)
ui_label(header_right, "DBMS PROJECT", size=9, bold=True, fg=TEAL, bg=BG).pack(anchor="e")
ui_label(header_right, "ONLINE COURSE LEARNING", size=8, fg=MUTED, bg=BG).pack(anchor="e", pady=(4, 0))

separator = tk.Frame(main_area, bg=BORDER, height=1)
separator.pack(fill="x", padx=30, pady=(0, 2))

content = tk.Frame(main_area, bg=BG)
content.pack(fill="both", expand=True)

page_frames = {}
nav_buttons = {}
page_subtitles = {
    "Dashboard": "A clear overview of your online learning data.",
    "Learners": "Register learners and review their details.",
    "Courses": "Explore courses and their assigned instructors.",
    "Enrolments": "Manage learner registrations for courses.",
    "Lesson Progress": "Track completion of individual lessons.",
    "Quizzes": "Browse quizzes and inspect their questions.",
    "Quiz Attempts": "Record assessment attempts and scores.",
    "Reports": "Review learning activity and performance summaries.",
}


def open_page(name):
    if name not in page_frames:
        return
    page_frames[name].tkraise()
    current_title.config(text=name)
    current_subtitle.config(text=page_subtitles.get(name, "Learning Progress Management System"))
    for button_name, button in nav_buttons.items():
        button.configure(style="NavActive.TButton" if button_name == name else "Nav.TButton")


nav_items = [
    ("Dashboard", "01   Dashboard"),
    ("Learners", "02   Learners"),
    ("Courses", "03   Courses"),
    ("Enrolments", "04   Enrolments"),
    ("Lesson Progress", "05   Lesson Progress"),
    ("Quizzes", "06   Quizzes"),
    ("Quiz Attempts", "07   Quiz Attempts"),
    ("Reports", "08   Reports"),
]

for page_name, button_text in nav_items:
    button = ttk.Button(
        sidebar,
        text=button_text,
        style="Nav.TButton",
        command=lambda name=page_name: open_page(name),
    )
    button.pack(fill="x", padx=12, pady=3)
    nav_buttons[page_name] = button

sidebar_spacer = tk.Frame(sidebar, bg=SIDEBAR)
sidebar_spacer.pack(fill="both", expand=True)

sidebar_footer = tk.Frame(sidebar, bg=SIDEBAR)
sidebar_footer.pack(fill="x", padx=20, pady=20)
tk.Frame(sidebar_footer, bg=BORDER, height=1).pack(fill="x", pady=(0, 14))
ui_label(sidebar_footer, "LEARNING PROGRESS", size=8, bold=True, fg=MUTED, bg=SIDEBAR).pack(anchor="w")
ui_label(sidebar_footer, "Management System  •  v1.0", size=8, fg="#64748B", bg=SIDEBAR).pack(anchor="w", pady=(5, 0))


def new_page(name):
    frame = tk.Frame(content, bg=BG)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    page_frames[name] = frame
    return frame


# ============================================================
# DASHBOARD
# ============================================================

dashboard_page = new_page("Dashboard")

welcome_card = tk.Frame(
    dashboard_page,
    bg=PANEL,
    highlightbackground=BORDER,
    highlightthickness=1,
)
welcome_card.pack(fill="x", padx=24, pady=(22, 18))
welcome_inner = tk.Frame(welcome_card, bg=PANEL)
welcome_inner.pack(fill="x", padx=24, pady=21)
ui_label(welcome_inner, "Your learning workspace", size=17, bold=True, fg=WHITE, bg=PANEL).pack(anchor="w")
ui_label(
    welcome_inner,
    "Manage learners, courses, lesson completion and quiz performance from one place.",
    size=10,
    fg=MUTED,
    bg=PANEL,
).pack(anchor="w", pady=(7, 0))

stats_grid = tk.Frame(dashboard_page, bg=BG)
stats_grid.pack(fill="x", padx=18, pady=(0, 18))
stat_values = {}

stat_specs = [
    ("Learners", "Total registered learners", CYAN),
    ("Courses", "Available courses", ACCENT_HOVER),
    ("Enrolments", "Course registrations", TEAL),
    ("Quiz Attempts", "Assessment records", AMBER),
]

for index, (label, description, color) in enumerate(stat_specs):
    card = tk.Frame(stats_grid, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
    card.grid(row=0, column=index, sticky="nsew", padx=6, pady=4)
    stats_grid.grid_columnconfigure(index, weight=1, uniform="stats")
    tk.Frame(card, bg=color, height=4).pack(fill="x")
    inner = tk.Frame(card, bg=PANEL)
    inner.pack(fill="both", expand=True, padx=16, pady=14)
    ui_label(inner, label.upper(), size=8, bold=True, fg=MUTED, bg=PANEL).pack(anchor="w")
    value_label = ui_label(inner, "—", size=25, bold=True, fg=WHITE, bg=PANEL)
    value_label.pack(anchor="w", pady=(7, 2))
    stat_values[label] = value_label
    ui_label(inner, description, size=8, fg=MUTED, bg=PANEL).pack(anchor="w")

bottom_grid = tk.Frame(dashboard_page, bg=BG)
bottom_grid.pack(fill="both", expand=True, padx=24, pady=(0, 20))

quick_card = tk.Frame(bottom_grid, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
quick_card.pack(side="left", fill="both", expand=True, padx=(0, 8))
quick_inner = tk.Frame(quick_card, bg=PANEL)
quick_inner.pack(fill="both", expand=True, padx=20, pady=18)
ui_label(quick_inner, "Quick actions", size=13, bold=True, fg=WHITE, bg=PANEL).pack(anchor="w")
ui_label(quick_inner, "Jump directly to a common task.", size=9, fg=MUTED, bg=PANEL).pack(anchor="w", pady=(5, 15))
quick_buttons = tk.Frame(quick_inner, bg=PANEL)
quick_buttons.pack(anchor="w")
add_action_button(quick_buttons, "+  Register learner", lambda: open_page("Learners"), primary=True).grid(row=0, column=0, padx=(0, 8), pady=5, sticky="w")
add_action_button(quick_buttons, "Update lesson progress", lambda: open_page("Lesson Progress")).grid(row=0, column=1, padx=5, pady=5, sticky="w")
add_action_button(quick_buttons, "Record quiz attempt", lambda: open_page("Quiz Attempts")).grid(row=1, column=0, padx=(0, 8), pady=5, sticky="w")
add_action_button(quick_buttons, "Open reports", lambda: open_page("Reports")).grid(row=1, column=1, padx=5, pady=5, sticky="w")

about_card = tk.Frame(bottom_grid, bg=PANEL, highlightbackground=BORDER, highlightthickness=1, width=265)
about_card.pack(side="right", fill="y", padx=(8, 0))
about_card.pack_propagate(False)
about_inner = tk.Frame(about_card, bg=PANEL)
about_inner.pack(fill="both", expand=True, padx=19, pady=18)
ui_label(about_inner, "Project modules", size=13, bold=True, fg=WHITE, bg=PANEL).pack(anchor="w")
for module in ["Learner management", "Course enrolment", "Lesson progress tracking", "Quiz and question bank", "Attempts and reporting"]:
    row = tk.Frame(about_inner, bg=PANEL)
    row.pack(fill="x", pady=(11, 0))
    ui_label(row, "●", size=9, bold=True, fg=TEAL, bg=PANEL).pack(side="left", padx=(0, 8))
    ui_label(row, module, size=9, fg=MUTED, bg=PANEL).pack(side="left", anchor="w")


# ============================================================
# LEARNERS
# ============================================================

learner_page = new_page("Learners")
learner_bar = make_action_bar(learner_page)
learner_table = create_table(
    learner_page,
    ("ID", "Name", "Email"),
    ("Learner ID", "Learner Name", "Email Address"),
    (100, 300, 340),
)


def refresh_learners():
    records = run_query("SELECT learner_id, name, email FROM LEARNER ORDER BY learner_id")
    if records is not None:
        fill_table(learner_table, records)


def add_learner():
    name = ask_text("Register Learner", "Enter learner name:")
    if name is None:
        return

    email = simpledialog.askstring(
        "Register Learner",
        "Enter email address (leave blank if unavailable):",
        parent=root,
    )
    if email is None:
        return
    email = email.strip() or None

    result = run_query(
        "INSERT INTO LEARNER (name, email) VALUES (%s, %s)",
        (name, email),
        fetch=False,
    )
    if result:
        messagebox.showinfo("Success", "Learner registered successfully.", parent=root)
        refresh_learners()
        refresh_dashboard_stats()
        refresh_reports()


add_action_button(learner_bar, "Refresh learners", refresh_learners).pack(side="left", padx=(0, 8))
add_action_button(learner_bar, "+  Register learner", add_learner, primary=True).pack(side="left")


# ============================================================
# COURSES
# ============================================================

course_page = new_page("Courses")
course_bar = make_action_bar(course_page)
course_table = create_table(
    course_page,
    ("Course ID", "Course Name", "Instructor"),
    ("Course ID", "Course Name", "Instructor Name"),
    (120, 400, 320),
)


def refresh_courses():
    records = run_query(
        """
        SELECT C.course_id, C.title, COALESCE(I.name, 'Not Assigned')
        FROM COURSE C
        LEFT JOIN INSTRUCTOR I ON C.instructor_id = I.instructor_id
        ORDER BY C.course_id
        """
    )
    if records is not None:
        fill_table(course_table, records)


add_action_button(course_bar, "Refresh courses", refresh_courses, primary=True).pack(side="left")


# ============================================================
# ENROLMENTS
# ============================================================

enrolment_page = new_page("Enrolments")
enrolment_bar = make_action_bar(enrolment_page)
enrolment_table = create_table(
    enrolment_page,
    ("ID", "Learner", "Course", "Date"),
    ("Enrolment ID", "Learner Name", "Course Name", "Enrolment Date"),
    (120, 260, 350, 180),
)


def refresh_enrolments():
    records = run_query(
        """
        SELECT E.enrolment_id, L.name, C.title, E.enrolment_date
        FROM ENROLMENT E
        JOIN LEARNER L ON E.learner_id = L.learner_id
        JOIN COURSE C ON E.course_id = C.course_id
        ORDER BY E.enrolment_id
        """
    )
    if records is not None:
        fill_table(enrolment_table, records)


def add_enrolment():
    learner_id = ask_integer("New Enrolment", "Enter an existing Learner ID:")
    if learner_id is None:
        return
    course_id = ask_integer("New Enrolment", "Enter an existing Course ID:")
    if course_id is None:
        return

    result = run_query(
        "INSERT INTO ENROLMENT (learner_id, course_id) VALUES (%s, %s)",
        (learner_id, course_id),
        fetch=False,
    )
    if result:
        messagebox.showinfo("Success", "Learner enrolled successfully.", parent=root)
        refresh_enrolments()
        refresh_dashboard_stats()
        refresh_reports()


add_action_button(enrolment_bar, "Refresh enrolments", refresh_enrolments).pack(side="left", padx=(0, 8))
add_action_button(enrolment_bar, "+  Enrol learner", add_enrolment, primary=True).pack(side="left")


# ============================================================
# LESSON PROGRESS
# ============================================================

progress_page = new_page("Lesson Progress")
progress_bar = make_action_bar(progress_page)
progress_table = create_table(
    progress_page,
    ("Learner", "Lesson", "Progress"),
    ("Learner Name", "Lesson Name", "Completion (%)"),
    (260, 430, 180),
)


def refresh_progress():
    records = run_query(
        """
        SELECT L.name, LS.lesson_name, LP.progress
        FROM LESSON_PROGRESS LP
        JOIN LEARNER L ON LP.learner_id = L.learner_id
        JOIN LESSON LS ON LP.lesson_id = LS.lesson_id
        ORDER BY L.name, LS.lesson_name
        """
    )
    if records is not None:
        fill_table(progress_table, records)


def add_progress():
    learner_id = ask_integer("Lesson Progress", "Enter an existing Learner ID:")
    if learner_id is None:
        return
    lesson_id = ask_integer("Lesson Progress", "Enter an existing Lesson ID:")
    if lesson_id is None:
        return
    progress = simpledialog.askfloat(
        "Lesson Progress",
        "Enter completion percentage (0–100):",
        parent=root,
        minvalue=0,
        maxvalue=100,
    )
    if progress is None:
        return

    result = run_query(
        """
        INSERT INTO LESSON_PROGRESS (learner_id, lesson_id, progress)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE progress = VALUES(progress)
        """,
        (learner_id, lesson_id, progress),
        fetch=False,
    )
    if result:
        messagebox.showinfo("Success", "Lesson progress saved successfully.", parent=root)
        refresh_progress()
        refresh_dashboard_stats()
        refresh_reports()


add_action_button(progress_bar, "Refresh progress", refresh_progress).pack(side="left", padx=(0, 8))
add_action_button(progress_bar, "+  Add / update progress", add_progress, primary=True).pack(side="left")


# ============================================================
# QUIZZES AND QUESTIONS
# ============================================================

quiz_page = new_page("Quizzes")
quiz_bar = make_action_bar(quiz_page)
quiz_table = create_table(
    quiz_page,
    ("Quiz ID", "Course", "Quiz Title", "Question Count"),
    ("Quiz ID", "Course Name", "Quiz Title", "Number of Questions"),
    (100, 300, 340, 180),
)


def refresh_quizzes():
    records = run_query(
        """
        SELECT Q.quiz_id, C.title, Q.title, COUNT(QU.question_id)
        FROM QUIZ Q
        JOIN COURSE C ON Q.course_id = C.course_id
        LEFT JOIN QUESTION QU ON Q.quiz_id = QU.quiz_id
        GROUP BY Q.quiz_id, C.title, Q.title
        ORDER BY Q.quiz_id
        """
    )
    if records is not None:
        fill_table(quiz_table, records)


def show_questions():
    quiz_id = ask_integer("Quiz Questions", "Enter an existing Quiz ID:")
    if quiz_id is None:
        return

    records = run_query(
        "SELECT question_id, question_text FROM QUESTION WHERE quiz_id = %s ORDER BY question_id",
        (quiz_id,),
    )
    if records is None:
        return

    window = tk.Toplevel(root)
    window.title(f"Questions — Quiz {quiz_id}")
    window.geometry("850x480")
    window.minsize(650, 360)
    window.configure(bg=BG)

    ui_label(window, f"Questions for Quiz {quiz_id}", size=16, bold=True, fg=WHITE, bg=BG).pack(anchor="w", padx=24, pady=(22, 4))
    ui_label(window, f"{len(records)} question(s) found", size=9, fg=MUTED, bg=BG).pack(anchor="w", padx=24, pady=(0, 14))
    question_table = create_table(
        window,
        ("Question ID", "Question"),
        ("Question ID", "Question Text"),
        (120, 650),
        height=10,
    )
    fill_table(question_table, records)


add_action_button(quiz_bar, "Refresh quizzes", refresh_quizzes).pack(side="left", padx=(0, 8))
add_action_button(quiz_bar, "View questions", show_questions, primary=True).pack(side="left")


# ============================================================
# QUIZ ATTEMPTS
# ============================================================

attempt_page = new_page("Quiz Attempts")
attempt_bar = make_action_bar(attempt_page)
attempt_table = create_table(
    attempt_page,
    ("Attempt ID", "Learner", "Quiz", "Attempt", "Score", "Date"),
    ("Attempt ID", "Learner Name", "Quiz Title", "Attempt Number", "Score (%)", "Attempt Date"),
    (105, 220, 260, 130, 130, 220),
)


def refresh_attempts():
    records = run_query(
        """
        SELECT A.attempt_id, L.name, Q.title, A.attempt_no, A.score, A.attempt_date
        FROM ATTEMPT A
        JOIN LEARNER L ON A.learner_id = L.learner_id
        JOIN QUIZ Q ON A.quiz_id = Q.quiz_id
        ORDER BY A.attempt_date DESC
        """
    )
    if records is not None:
        fill_table(attempt_table, records)


def add_attempt():
    learner_id = ask_integer("Record Quiz Attempt", "Enter an existing Learner ID:")
    if learner_id is None:
        return
    quiz_id = ask_integer("Record Quiz Attempt", "Enter an existing Quiz ID:")
    if quiz_id is None:
        return
    attempt_no = ask_integer("Record Quiz Attempt", "Enter the attempt number:")
    if attempt_no is None:
        return
    score = simpledialog.askfloat(
        "Record Quiz Attempt",
        "Enter score out of 100:",
        parent=root,
        minvalue=0,
        maxvalue=100,
    )
    if score is None:
        return

    result = run_query(
        "INSERT INTO ATTEMPT (learner_id, quiz_id, attempt_no, score) VALUES (%s, %s, %s, %s)",
        (learner_id, quiz_id, attempt_no, score),
        fetch=False,
    )
    if result:
        messagebox.showinfo("Success", "Quiz attempt recorded successfully.", parent=root)
        refresh_attempts()
        refresh_dashboard_stats()
        refresh_reports()


add_action_button(attempt_bar, "Refresh attempts", refresh_attempts).pack(side="left", padx=(0, 8))
add_action_button(attempt_bar, "+  Record attempt", add_attempt, primary=True).pack(side="left")


# ============================================================
# REPORTS
# ============================================================

report_page = new_page("Reports")
report_bar = make_action_bar(report_page)
report_table = create_table(
    report_page,
    ("Learner", "Courses", "Lessons", "Average Progress", "Average Score"),
    ("Learner Name", "Courses Enrolled", "Lessons Tracked", "Average Progress (%)", "Average Quiz Score"),
    (240, 160, 160, 210, 210),
)


def refresh_reports():
    records = run_query(
        """
        SELECT
            L.name,
            (SELECT COUNT(*) FROM ENROLMENT E WHERE E.learner_id = L.learner_id) AS courses_enrolled,
            (SELECT COUNT(*) FROM LESSON_PROGRESS LP WHERE LP.learner_id = L.learner_id) AS lessons_tracked,
            (SELECT ROUND(AVG(LP.progress), 2) FROM LESSON_PROGRESS LP WHERE LP.learner_id = L.learner_id) AS average_progress,
            (SELECT ROUND(AVG(A.score), 2) FROM ATTEMPT A WHERE A.learner_id = L.learner_id) AS average_score
        FROM LEARNER L
        ORDER BY L.name
        """
    )
    if records is not None:
        fill_table(report_table, records)


add_action_button(report_bar, "Generate learning reports", refresh_reports, primary=True).pack(side="left")


# ============================================================
# DASHBOARD DATA + INITIAL LOAD
# ============================================================

def get_count(table_name):
    allowed_tables = {
        "LEARNER",
        "COURSE",
        "ENROLMENT",
        "ATTEMPT",
        "LESSON_PROGRESS",
    }
    if table_name not in allowed_tables:
        return 0
    result = run_query(f"SELECT COUNT(*) FROM {table_name}")
    if result and result[0]:
        return result[0][0]
    return 0


def refresh_dashboard_stats():
    count_map = {
        "Learners": "LEARNER",
        "Courses": "COURSE",
        "Enrolments": "ENROLMENT",
        "Quiz Attempts": "ATTEMPT",
    }
    for label, table_name in count_map.items():
        value = get_count(table_name)
        if label in stat_values:
            stat_values[label].config(text=str(value))


def refresh_all():
    refresh_learners()
    refresh_courses()
    refresh_enrolments()
    refresh_progress()
    refresh_quizzes()
    refresh_attempts()
    refresh_reports()
    refresh_dashboard_stats()


# A small refresh control on the dashboard
refresh_dashboard_button = add_action_button(
    header_right,
    "Refresh all data",
    refresh_all,
    primary=True,
)
refresh_dashboard_button.pack(anchor="e", pady=(10, 0))

open_page("Dashboard")
refresh_all()

root.mainloop()
