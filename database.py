import sqlite3

def init_db():
    conn = sqlite3.connect("assistant.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task_text TEXT,
            reminder_time TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()

def add_task(user_id, task_text, reminder_time):
    conn = sqlite3.connect("assistant.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (user_id, task_text, reminder_time) VALUES (?, ?, ?)", 
                   (user_id, task_text, reminder_time))
    conn.commit()
    conn.close()