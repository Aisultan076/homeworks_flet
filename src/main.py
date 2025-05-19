import flet as ft
from database import Database

db = Database()

def main(page: ft.Page):
    page.title = "Expanses"
    page.scroll = True

    title_field = ft.TextField(label="Название расхода", width=300, expand=True)
    amount_field = ft.TextField(label="Сумма расхода", width=150, expand=True, keyboard_type=ft.KeyboardType.NUMBER)

    total_text = ft.Text(value=f"Общая сумма расходов: {db.get_total_amount()} ", size=20, weight=ft.FontWeight.BOLD)

    expenses_list = ft.Column()

    def update_expenses_list():
        expenses_list.controls.clear()
        for title, amount in db.get_all_expenses():
            expenses_list.controls.append(ft.Text(f"{title}: {amount:.2f} "))
        total_text.value = f"Общая сумма расходов: {db.get_total_amount():.2f} "
        page.update()

    def add_expense_clicked(e):
        title = title_field.value.strip()
        try:
            amount = float(amount_field.value.strip())
        except ValueError:
            amount_field.error_text = "Введите число"
            page.update()
            return

        if not title:
            title_field.error_text = "Поле обязательно"
            page.update()
            return

        title_field.error_text = ""
        amount_field.error_text = ""

        db.add_expense(title, amount)
        title_field.value = ""
        amount_field.value = ""
        update_expenses_list()

    add_button = ft.ElevatedButton("Добавить", on_click=add_expense_clicked)

    page.add(
        ft.Text("Ваши расходы", size=30, weight="bold"),
        ft.Row([title_field, amount_field, add_button]),
        total_text,
        expenses_list,
    )

    update_expenses_list()

ft.app(target=main)
