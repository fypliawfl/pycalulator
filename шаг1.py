import tkinter
from tkinter import messagebox
from typing import List

AUTHOR = "Гельманов Артур Русланович"
EDUCATED_YEAR = 4
YEAR = 2022
GROUP = 4

ERROR_OUT_OF_RANGE = 1
ERROR_INCORRECT_NUMBER = 2
NO_ERROR = 0


def handle_operation(event, operation: str) -> None:
    first_number = preprocess_number(first_number_entry.get())
    second_number = preprocess_number(second_number_entry.get())
    first_number_code = check_number(first_number)
    second_number_code = check_number(second_number)
    if first_number_code:
        if first_number_code == ERROR_OUT_OF_RANGE:
            messagebox.showwarning("", "Первое число не входит в допустимый диапозон")
        elif first_number_code == ERROR_INCORRECT_NUMBER:
            messagebox.showwarning("Неверный ввод", "В первое поле введено не число")
    elif second_number_code:
        if second_number_code == ERROR_OUT_OF_RANGE:
            messagebox.showwarning("", "Второе число не входит в допустимый диапозон")
        elif second_number_code == ERROR_INCORRECT_NUMBER:
            messagebox.showwarning("Неверный ввод", "Во второе число введено не число")
    else:
        if operation == "+":
            answer_value = float(first_number) + float(second_number)
            if not (
                (answer_value >= -1_000_000_000_000.0)
                and (answer_value <= 1_000_000_000_000.0)
            ):
                messagebox.showwarning(
                    "Операция невозможна", "Результат не входит в допустимый диапазон"
                )
            else:
                answer.set(str(answer_value))
        elif operation == "-":
            answer_value = float(first_number) - float(second_number)
            if not (
                (answer_value >= -1_000_000_000_000.0)
                and (answer_value <= 1_000_000_000_000.0)
            ):
                messagebox.showwarning(
                    "Операция невозможна", "Результат не входит в допустимый диапазон"
                )
            else:
                answer.set(str(answer_value))


def clear(event, entries: List[tkinter.StringVar]) -> None:
    for entry in entries:
        entry.set("")


def preprocess_number(number: str):
    dot_count = number.count(".")
    comma_count = number.count(",")
    if dot_count > 1:
        number = number.replace(".", "")
    if comma_count > 1:
        number = number.replace(",", "")
    chars = " "
    for c in chars:
        number = number.replace(c, "")
    number = number.replace("e", "так нельзя")
    return number.replace(",", ".")


def check_number(number: str) -> int:
    try:
        number = float(number)
    except Exception:
        return ERROR_INCORRECT_NUMBER
    if not ((number >= -1_000_000_000_000.0) and (number <= 1_000_000_000_000.0)):
        return ERROR_OUT_OF_RANGE
    else:
        return NO_ERROR


if __name__ == "__main__":
    app = tkinter.Tk()
    app.minsize(800, 600)
    app.resizable(False, False)
    app.title("Калькулятор")
    answer = tkinter.StringVar()
    first_number = tkinter.StringVar()
    second_number = tkinter.StringVar()

    # buttons
    plus_button = tkinter.Button(
        app,
        text="+",
        width=10,
        height=2,
        bg="blue",
        fg="black",
        font=("Helvatical bold", 15),
    )
    minus_button = tkinter.Button(
        app,
        text="-",
        width=10,
        height=2,
        bg="blue",
        fg="black",
        font=("Helvatical bold", 15),
    )
    clear_button = tkinter.Button(
        app,
        text="Очистить",
        width=10,
        height=2,
        bg="blue",
        fg="black",
        font=("Helvatical bold", 15),
    )

    # labels
    author_label = tkinter.Label(app, text=f"{AUTHOR}")
    curs_label = tkinter.Label(app, text=f"{EDUCATED_YEAR} курс, {GROUP} группа")
    year_label = tkinter.Label(app, text=f"{YEAR} год")
    first_number_label = tkinter.Label(
        app, text="Первое число:", font=("Helvatical bold", 20)
    )
    second_number_label = tkinter.Label(
        app, text="Второе число:", font=("Helvatical bold", 20)
    )
    answer_label = tkinter.Label(app, text="ОТВЕТ:", font=("Helvatical bold", 20))

    # entries
    first_number_entry = tkinter.Entry(
        app,
        justify=tkinter.LEFT,
        textvariable=first_number,
        font=("Helvatical bold", 15),
    )
    second_number_entry = tkinter.Entry(
        app, textvariable=second_number, font=("Helvatical bold", 15)
    )
    answer_entry = tkinter.Entry(app, textvariable=answer, font=("Helvatical bold", 15))

    # placing
    year_label.pack(side=tkinter.BOTTOM)
    curs_label.pack(side=tkinter.BOTTOM)
    author_label.pack(side=tkinter.BOTTOM)
    first_number_label.place(relx=0.1, rely=0.05)
    second_number_label.place(relx=0.55, rely=0.05)
    answer_label.place(relx=0.3, rely=0.25)

    plus_button.place(relx=0.25, rely=0.5, relwidth=0.2, relheight=0.13)
    minus_button.place(relx=0.55, rely=0.5, relwidth=0.2, relheight=0.13)
    clear_button.place(relx=0.4, rely=0.65, relwidth=0.2, relheight=0.13)

    first_number_entry.place(relx=0.1, rely=0.1, relwidth=0.35, relheight=0.1)
    second_number_entry.place(relx=0.55, rely=0.1, relwidth=0.35, relheight=0.1)
    answer_entry.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.1)

    # commands
    plus_button.bind("<Button-1>", lambda event: handle_operation(event, "+"))
    minus_button.bind("<Button-1>", lambda event: handle_operation(event, "-"))
    clear_button.bind(
        "<Button-1>", lambda event: clear(event, [first_number, second_number, answer])
    )

    app.mainloop()
