import flet as ft
import sqlite3


class Database:
    def __init__(self, db_path="expenses.db"):
        self.db_path = db_path
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def create_table(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    amount INTEGER
                )
            """)

    def add_expense(self, category, amount):
        with self.get_connection() as conn:
            conn.execute("INSERT INTO expenses (category, amount) VALUES (?, ?)", (category, amount))

    def delete_expense(self, expense_id: int):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

    def get_all_expenses(self):
        with self.get_connection() as conn:
            return conn.execute("SELECT id, category, amount FROM expenses ORDER BY id DESC").fetchall()



db = Database()


def main(page: ft.Page):
    page.title = "Расходы"
    category_input = ft.TextField(label="Название расхода")
    amount_input = ft.TextField(label="Сумма Расхода", keyboard_type="number")
    add_btn = ft.ElevatedButton(text="Добавить", on_click=lambda e: add_expense())

    expense_column = ft.Column(scroll="always")
    scroll_area = ft.Container(content=expense_column, height=300)

    def add_expense():
        if category_input.value and amount_input.value.isdigit():
            db.add_expense(category_input.value, int(amount_input.value))
            category_input.value = ""
            amount_input.value = ""
            update_expense_list()

    def delete_expense_and_update(expense_id):
        db.delete_expense(expense_id)
        update_expense_list()

    def update_expense_list():
        expense_column.controls.clear()
        for exp_id, cat, amt in db.get_all_expenses():
            expense_column.controls.append(build_expense_row(exp_id, cat, amt))
        page.update()

    def build_expense_row(expense_id, category, amount):
        return ft.Row([
            ft.Text(f"{category}: {amount} ", expand=True),
            ft.IconButton(
                icon=ft.icons.DELETE,
                icon_color="red",
                tooltip="Удалить",
                on_click=lambda e: delete_expense_and_update(expense_id)
            )
        ])

    page.add(
        ft.Text("Ваши расходы", size=30, weight="bold"),
        ft.Row([category_input, amount_input, add_btn]),
        scroll_area
    )

    update_expense_list()


ft.app(target=main)
