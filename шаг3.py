import tkinter
from tkinter import messagebox
from typing import List
from decimal import Decimal
import decimal

AUTHER = "Гельманов Артур Русланович"
EDUCATED_YEAR = 4
YEAR = 2022
GROUP = 4

ERROR_OUT_OF_RANGE = 1
ERROR_INCORRECT_NUMBER = 2
ERROR_ZERO_DIVISION = 3
ERROR_INCORRECT_SPACES = 4
NO_ERROR = 0

OPERATION_ID = 0


def handle_operation(event, operation: str) -> None:
    global OPERATION_ID
    entry = OPERATIONS_ENTRIES[OPERATION_ID]
    entry.set(operation)
    OPERATION_ID = (OPERATION_ID + 1) if OPERATION_ID < 2 else 0


def clear(event, entries: List[tkinter.StringVar], operations) -> None:
    for entry in entries:
        entry.set("0")
    for operation in operations:
        operation.set("+")


def preprocess_number(number: str) -> str:
    dot_count = number.count(".")
    comma_count = number.count(",")
    if dot_count > 1:
        number = number.replace(".", "")
    if comma_count > 1:
        number = number.replace(",", "")
    number = number.replace("e", "так нельзя")
    return number.replace(",", ".")


def preprocess_spaces(number: str) -> str:
    number = number.replace(" ", "")
    return number


def error_handler(error_code: int, index: int) -> int:
    res = 0
    if error_code == ERROR_OUT_OF_RANGE:
        messagebox.showwarning(
            "Неверный ввод", f"{index}-е число не входит в допустимый диапозон"
        )
        res = 1
    elif error_code == ERROR_INCORRECT_NUMBER:
        messagebox.showwarning("Неверный ввод", f"В {index}-е поле введено не число")
        res = 1
    elif error_code == ERROR_INCORRECT_SPACES:
        messagebox.showwarning(
            "Неверный ввод", f"В {index}-е поле введено число в неправильном формате"
        )
        res = 1
    return res


def check_number(number: str) -> int:
    add_number = 0
    try:
        add_number = float(number)
    except Exception:
        return ERROR_INCORRECT_NUMBER
    if not (
        (float(number) > -1_000_000_000_000.0) and (float(number) < 1_000_000_000_000.0)
    ):
        return ERROR_OUT_OF_RANGE
    if not check_spaces(number):
        return ERROR_INCORRECT_SPACES
    else:
        return NO_ERROR


def focus_out(event, value: tkinter.StringVar) -> None:
    if value.get() == "0" or value.get() == "":
        value.set("0")


def focus_in(event, value: tkinter.StringVar) -> None:
    if value.get() == "0":
        value.set("")


def check_spaces(number: str) -> bool:
    ind_lst = []
    if number.find(" ") != -1:
        parts = number.split(".")
        int_part = parts[0]
        len_int_part = len(int_part)
        for ind in range(len_int_part, 0, -4):
            if ind == len_int_part:
                continue
            else:
                ind_lst.append(ind)
                if int_part[ind] != " ":
                    return False
        for ind in range(0, len_int_part):
            if not (ind in ind_lst):
                if int_part[ind] == " ":
                    return False

    return True


def get_instruction(event) -> None:
    messagebox.showinfo(
        "Инструкция",
        "В числовых полях приведите значения. \n Затем три раза выберите операции."
        "Операции будут задаваться последовательно: от1 до 2 до 3 до 1 ...)\n "
        "После чего выберите тип округления. \n"
        "Затем нажмите на кнопку = .",
    )


def bank_rounding(number: Decimal) -> int:
    int_part = int(number)
    str_number = str(number)
    parts = str_number.split(".")
    if len(parts) == 2:
        if parts[1][0] == "5" and int_part % 2 != 0:
            return int_part + 1
        elif parts[1][0] == "5" and int_part % 2 == 0:
            return int_part
    return int_part


def math_rounding(number: Decimal) -> int:
    str_number = str(number)
    parts = str_number.split(".")

    if len(parts) == 2:
        if int(parts[1][0]) == 5:
            return round(number + Decimal(0.1))
    return round(number)


def show_computing_res(ans: Decimal):
    if computing.get() == "1":
        computing_answer_value.set(f"{math_rounding(ans):,}".replace(",", " "))
    elif computing.get() == "2":
        computing_answer_value.set(f"{bank_rounding(ans):,}".replace(",", " "))
    elif computing.get() == "3":
        computing_answer_value.set(f"{int(ans):,}".replace(",", " "))
    # computing_answer_value.set(f"{int(ans):,}".replace(",", " "))


def equal(event) -> None:
    global NUMBER_ENTRIES
    global OPERATIONS_ENTRIES
    global RESULT_OUTPUTS

    first_number = preprocess_number(NUMBER_ENTRIES[0].get())
    second_number = preprocess_number(NUMBER_ENTRIES[1].get())
    third_number = preprocess_number(NUMBER_ENTRIES[2].get())
    fourth_number = preprocess_number(NUMBER_ENTRIES[3].get())
    numbers = [first_number, second_number, third_number, fourth_number]

    for ind, number in enumerate(numbers):
        if not check_spaces(number):
            messagebox.showwarning(
                "Неверный ввод",
                f"В {ind + 1}-е поле введено число в неправильном формате",
            )
            return None

    first_number = preprocess_spaces(first_number)
    second_number = preprocess_spaces(second_number)
    third_number = preprocess_spaces(third_number)
    fourth_number = preprocess_spaces(fourth_number)

    number_codes = [
        check_number(first_number),
        check_number(second_number),
        check_number(third_number),
        check_number(fourth_number),
    ]
    res = 0
    for ind, error_code in enumerate(number_codes):
        res = error_handler(error_code, ind + 1)
        if res:
            break

    first_operation = OPERATIONS_ENTRIES[0].get()
    second_operation = OPERATIONS_ENTRIES[1].get()
    third_operation = OPERATIONS_ENTRIES[2].get()
    if not res:
        try:
            answer = eval(
                f"round(Decimal(second_number) {second_operation} Decimal(third_number), 10)"
            )
            if (first_operation in "*/") or (second_operation in "+-"):
                answer = eval(
                    f"round(Decimal(first_number) {first_operation} Decimal({answer}), 10)"
                )
                answer = eval(
                    f"round(Decimal({answer}) {third_operation} Decimal(fourth_number), 6)"
                )
            else:
                answer = eval(
                    f"round(Decimal({answer}) {third_operation} Decimal(fourth_number), 10)"
                )
                answer = eval(
                    f"round(Decimal(first_number) {first_operation} Decimal({answer}), 6)"
                )
            answer = answer.normalize()
            show_computing_res(answer)
            answer = f"{answer:,}".replace(",", " ")
            answer_value.set(answer)
        except decimal.InvalidOperation as err:
            messagebox.showwarning(
                "Неверный ввод", f"Проверьте правильность введенных чисел"
            )
            clear(0, entry_values, operation_values)


if __name__ == "__main__":
    app = tkinter.Tk()
    app.minsize(1200, 600)
    app.resizable(False, False)
    app.title("Калькулятор")
    answer_value = tkinter.StringVar(app, "0")
    computing_answer_value = tkinter.StringVar(app, "0")
    first_number_value = tkinter.StringVar(app, "0")
    second_number_value = tkinter.StringVar(app, "0")
    third_number_value = tkinter.StringVar(app, "0")
    fourth_number_value = tkinter.StringVar(app, "0")
    first_operation_value = tkinter.StringVar(app, "+")
    second_operation_value = tkinter.StringVar(app, "+")
    third_operation_value = tkinter.StringVar(app, "+")

    entry_values = [
        first_number_value,
        second_number_value,
        third_number_value,
        fourth_number_value,
        answer_value,
        computing_answer_value,
    ]
    operation_values = [
        first_operation_value,
        second_operation_value,
        third_operation_value,
    ]

    computing = tkinter.StringVar(app, "1")

    computing_options = {
        "математическое": "1",
        "бухгалтерское": "2",
        "усечение": "3",
    }

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
        bg="red",
        fg="black",
        font=("Helvatical bold", 15),
    )
    multiplication_button = tkinter.Button(
        app,
        text="*",
        width=10,
        height=2,
        bg="blue",
        fg="black",
        font=("Helvatical bold", 15),
    )
    division_button = tkinter.Button(
        app,
        text="/",
        width=10,
        height=2,
        bg="blue",
        fg="black",
        font=("Helvatical bold", 15),
    )
    equal_button = tkinter.Button(
        app,
        text="=",
        width=10,
        height=2,
        bg="blue",
        fg="black",
        font=("Helvatical bold", 15),
    )

    instruction_button = tkinter.Button(
        app,
        text="Инструкция",
        width=10,
        height=2,
        bg="pink",
        fg="yellow",
        font=("Helvatical bold", 15),
    )

    # labels
    author_label = tkinter.Label(app, text=f"{AUTHER}")
    curs_label = tkinter.Label(app, text=f"{EDUCATED_YEAR} курс, {GROUP} группа")
    year_label = tkinter.Label(app, text=f"{YEAR} год")
    first_number_label = tkinter.Label(
        app, text="Первое число:", font=("Helvatical bold", 15)
    )
    second_number_label = tkinter.Label(
        app, text="Второе число:", font=("Helvatical bold", 15)
    )
    third_number_label = tkinter.Label(
        app, text="Третье число:", font=("Helvatical bold", 15)
    )
    fourth_number_label = tkinter.Label(
        app, text="Четвертое число:", font=("Helvatical bold", 15)
    )
    answer_label = tkinter.Label(app, text="ОТВЕТ:", font=("Helvatical bold", 20))
    computing_answer_label = tkinter.Label(
        app, text="Округленный результат:", font=("Helvatical bold", 20)
    )
    left_bracket = tkinter.Label(app, text="(", font=("Helvatical bold", 40))
    right_bracket = tkinter.Label(app, text=")", font=("Helvatical bold", 40))
    computing_question_label = tkinter.Label(
        app, text="Тип округления:", font=("Helvatical bold", 20)
    )

    # entries
    first_number_entry = tkinter.Entry(
        app,
        justify=tkinter.LEFT,
        textvariable=first_number_value,
        font=("Helvatical bold", 15),
    )
    second_number_entry = tkinter.Entry(
        app, textvariable=second_number_value, font=("Helvatical bold", 15)
    )
    third_number_entry = tkinter.Entry(
        app, textvariable=third_number_value, font=("Helvatical bold", 15)
    )
    fourth_number_entry = tkinter.Entry(
        app, textvariable=fourth_number_value, font=("Helvatical bold", 15)
    )
    answer_entry = tkinter.Entry(
        app, textvariable=answer_value, font=("Helvatical bold", 15)
    )
    computing_answer_entry = tkinter.Entry(
        app, textvariable=computing_answer_value, font=("Helvatical bold", 15)
    )
    first_operation_entry = tkinter.Entry(
        app, textvariable=first_operation_value, font=("Helvatical bold", 35)
    )
    second_operation_entry = tkinter.Entry(
        app, textvariable=second_operation_value, font=("Helvatical bold", 35)
    )
    third_operation_entry = tkinter.Entry(
        app, textvariable=third_operation_value, font=("Helvatical bold", 35)
    )

    OPERATIONS_ENTRIES = [
        first_operation_value,
        second_operation_value,
        third_operation_value,
    ]
    NUMBER_ENTRIES = [
        first_number_value,
        second_number_value,
        third_number_value,
        fourth_number_value,
    ]

    RESULT_OUTPUTS = [answer_value, computing_answer_value]

    # radiobuttons
    rb_x = 0.05
    rb_y = 0.5
    for txt, val in computing_options.items():
        r1 = tkinter.Radiobutton(
            app, text=txt, variable=computing, value=val, font=("Helvatical bold", 15)
        )
        r1.place(relx=rb_x, rely=rb_y)
        rb_y += 0.05

    # placing
    year_label.pack(side=tkinter.BOTTOM)
    curs_label.pack(side=tkinter.BOTTOM)
    author_label.pack(side=tkinter.BOTTOM)
    first_number_label.place(relx=0.034, rely=0.05)
    second_number_label.place(relx=0.284, rely=0.05)
    third_number_label.place(relx=0.534, rely=0.05)
    fourth_number_label.place(relx=0.795, rely=0.05)
    answer_label.place(relx=0.2, rely=0.25)
    computing_answer_label.place(relx=0.05, rely=0.7)
    left_bracket.place(relx=0.26, rely=0.09)
    right_bracket.place(relx=0.69, rely=0.09)
    computing_question_label.place(relx=0.05, rely=0.43)

    plus_button.place(relx=0.4, rely=0.45, relwidth=0.2, relheight=0.13)
    minus_button.place(relx=0.65, rely=0.45, relwidth=0.2, relheight=0.13)
    clear_button.place(relx=0.7, rely=0.29, relwidth=0.2, relheight=0.13)
    multiplication_button.place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.13)
    division_button.place(relx=0.65, rely=0.6, relwidth=0.2, relheight=0.13)
    equal_button.place(relx=0.52, rely=0.75, relwidth=0.2, relheight=0.13)
    instruction_button.place(relx=0.75, rely=0.87, relwidth=0.2, relheight=0.13)

    first_number_entry.place(relx=0.035, rely=0.1, relwidth=0.15, relheight=0.1)
    second_number_entry.place(relx=0.285, rely=0.1, relwidth=0.15, relheight=0.1)
    third_number_entry.place(relx=0.535, rely=0.1, relwidth=0.15, relheight=0.1)
    fourth_number_entry.place(relx=0.8, rely=0.1, relwidth=0.15, relheight=0.1)
    first_operation_entry.place(relx=0.21, rely=0.1, relwidth=0.04, relheight=0.1)
    second_operation_entry.place(relx=0.46, rely=0.1, relwidth=0.04, relheight=0.1)
    third_operation_entry.place(relx=0.73, rely=0.1, relwidth=0.04, relheight=0.1)
    answer_entry.place(relx=0.2, rely=0.3, relwidth=0.4, relheight=0.1)
    computing_answer_entry.place(relx=0.05, rely=0.76, relwidth=0.3, relheight=0.1)

    # commands
    plus_button.bind("<Button-1>", lambda event: handle_operation(event, "+"))
    minus_button.bind("<Button-1>", lambda event: handle_operation(event, "-"))
    multiplication_button.bind("<Button-1>", lambda event: handle_operation(event, "*"))
    division_button.bind("<Button-1>", lambda event: handle_operation(event, "/"))
    instruction_button.bind("<Button-1>", lambda event: get_instruction(event))
    clear_button.bind(
        "<Button-1>", lambda event: clear(event, entry_values, operation_values)
    )
    equal_button.bind("<Button-1>", lambda event: equal(event))

    first_number_entry.bind(
        "<FocusIn>", lambda event: focus_in(event, first_number_value)
    )
    first_number_entry.bind(
        "<FocusOut>", lambda event: focus_out(event, first_number_value)
    )
    second_number_entry.bind(
        "<FocusIn>", lambda event: focus_in(event, second_number_value)
    )
    second_number_entry.bind(
        "<FocusOut>", lambda event: focus_out(event, second_number_value)
    )
    third_number_entry.bind(
        "<FocusIn>", lambda event: focus_in(event, third_number_value)
    )
    third_number_entry.bind(
        "<FocusOut>", lambda event: focus_out(event, third_number_value)
    )
    fourth_number_entry.bind(
        "<FocusIn>", lambda event: focus_in(event, fourth_number_value)
    )
    fourth_number_entry.bind(
        "<FocusOut>", lambda event: focus_out(event, fourth_number_value)
    )

    app.mainloop()
