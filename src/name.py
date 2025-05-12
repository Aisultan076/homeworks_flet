import flet as ft

def main(page: ft.Page):
    page.title = "Ваши расходы"
    page.data = 0


    name_input = ft.TextField(label="Название расхода")
    amount_input = ft.TextField(label="Сумма расхода(сом)", keyboard_type="number")


    total_text = ft.Text(value="Общая сумма: 0 сом", size=20, weight="bold")


    expenses_list = ft.Column()


    def add_expense(e):
        name = name_input.value
        try:
            amount = float(amount_input.value)
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Введите корректную сумму!"))
            page.snack_bar.open = True
            page.update()
            return


        expenses_list.controls.append(ft.Text(f"{name}: {amount}"))


        page.data += amount
        total_text.value = f"Общая сумма расходов: {page.data} сом"


        name_input.value = ""
        amount_input.value = ""


        page.update()


    add_button = ft.ElevatedButton(text="Добавить", on_click=add_expense)


    page.add(
        name_input,
        amount_input,
        add_button,
        total_text,
        ft.Text("Список расходов:"),
        expenses_list,
    )

ft.app(target=main)
