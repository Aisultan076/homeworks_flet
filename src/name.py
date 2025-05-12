import flet as ft


def main(page: ft.Page):
    page.title = "Учет расходов"
    page.verical_alignment = ft.MainAxisAlingment.CENTER

    name_input = ft.TextField(label="Название расхода")
    amount_input = ft.TextField(label="Сумма расхода")
    result = ft.Text()

    def add_expense(e):
        if name_input.value and amount_input.value:
            result.value = f"Добавлено: {name_input.value}"
        else:
            result.value = "Заполните оба поля"
        page.update()

    add_button = ft.ElevatedButton(text="Добавить", on_click=add_expense)

    page.add(
        ft.Text("Учет расходов", size=30, weight=ft.FontWeight.BOLD),
        name_input,
        amount_input,
        add_button,
        result
    )

ft.app(target=main)