import flet as ft
from database import Database

db = Database()
db.create_tables()

def main(page: ft.Page):
    page.title = "Учет расходов"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    name_input = ft.TextField(label="Название расхода", width=250)
    amount_input = ft.TextField(label="Сумма расхода(сом)", width=200, keyboard_type=ft.KeyboardType.NUMBER)
    add_button = ft.ElevatedButton(text="Добавить")

    total_text = ft.Text()
    history_column = ft.Column()

    def load_expenses():
        expenses = db.get_expenses()
        total = db.get_total()
        total_text.value = f"Общая сумма расходов: {total} сом"
        history_column.controls.clear()
        for item in expenses:
            history_column.controls.append(
                ft.Text(f"Расход: {item[1]}/Сумма: {item[2]} сом")
            )
        page.update()

    def add_expense(e):
        name = name_input.value.strip()
        try:
            amount = float(amount_input.value)
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Введите корректную сумму"))
            page.snack_bar.open = True
            page.update()
            return

        if name and amount > 0:
            db.add_expense(name, amount)
            name_input.value = ""
            amount_input.value = ""
            load_expenses()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Пожалуйста, заполните все поля корректно"))
            page.snack_bar.open = True

        page.update()

    add_button.on_click = add_expense

    page.add(
        ft.Text("Ваши расходы", size=30, weight="bold"),
        ft.Row([name_input, amount_input, add_button]),
        total_text,
        history_column,
    )

    load_expenses()

ft.app(target=main)
