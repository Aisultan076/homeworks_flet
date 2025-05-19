import sqlite3

class Database:
    def __init__(self, db_name="expenses.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL
        )
        """)
        self.conn.commit()

    def add_expense(self, title, amount):
        self.cursor.execute("INSERT INTO expenses (title, amount) VALUES (?, ?)", (title, amount))
        self.conn.commit()

    def get_total_amount(self):
        self.cursor.execute("SELECT SUM(amount) FROM expenses")
        result = self.cursor.fetchone()
        return result[0] if result[0] is not None else 0.0

    def get_all_expenses(self):
        self.cursor.execute("SELECT title, amount FROM expenses ORDER BY id DESC")
        return self.cursor.fetchall()
