import ast
import operator
import flet as ft

def main(page: ft.Page):
    page.title = "My Colorful Calculator"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#101522"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    expression = ""
    result = ft.Text(
        "0",
        size=38,
        color="#FFFFFF",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.RIGHT,
    )

    display = ft.Container(
        content=ft.Column(
            [
                ft.Text("MY CALCULATOR", size=15, color="#42D9FF"),
                result,
            ],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.END,
        ),
        bgcolor="#202A40",
        padding=20,
        border_radius=20,
        height=125,
        width=340,
    )

    def safe_calculate(text):
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                return node.value

            if isinstance(node, ast.BinOp) and type(node.op) in operators:
                left = evaluate(node.left)
                right = evaluate(node.right)

                if isinstance(node.op, ast.Div) and right == 0:
                    raise ZeroDivisionError

                return operators[type(node.op)](left, right)

            if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
                return operators[type(node.op)](evaluate(node.operand))

            raise ValueError("Invalid expression")

        tree = ast.parse(text, mode="eval")
        return evaluate(tree)

    def button_click(e):
        nonlocal expression

        value = e.control.data

        if value == "C":
            expression = ""
            result.value = "0"

        elif value == "⌫":
            expression = expression[:-1]
            result.value = expression or "0"

        elif value == "=":
            if not expression:
                return

            try:
                answer = safe_calculate(expression)
                expression = str(answer)
                result.value = expression
            except ZeroDivisionError:
                expression = ""
                result.value = "Cannot divide by zero"
            except Exception:
                expression = ""
                result.value = "Invalid calculation"

        else:
            if value == "×":
                expression += "*"
            elif value == "÷":
                expression += "/"
            else:
                expression += value

            result.value = expression

        page.update()

    def make_button(label, color="#273650", text_color="#FFFFFF"):
        return ft.Container(
            content=ft.Text(
                label,
                size=23,
                weight=ft.FontWeight.BOLD,
                color=text_color,
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.Alignment.CENTER,
            bgcolor=color,
            border_radius=16,
            height=65,
            expand=True,
            on_click=button_click,
            data=label,
        )

    rows = [
        [("C", "#FF4D6D"), ("⌫", "#FF9F43"), ("÷", "#6750A4"), ("×", "#6750A4")],
        [("7", "#273650"), ("8", "#273650"), ("9", "#273650"), ("-", "#6750A4")],
        [("4", "#273650"), ("5", "#273650"), ("6", "#273650"), ("+", "#6750A4")],
        [("1", "#273650"), ("2", "#273650"), ("3", "#273650"), ("=", "#00B894")],
        [("0", "#273650"), (".", "#273650")],
    ]

    page.add(
        ft.Column(
            [
                display,
                ft.Container(height=12),
                *[
                    ft.Row(
                        [
                            make_button(label, color)
                            for label, color in row
                        ],
                        spacing=10,
                    )
                    for row in rows
                ],
            ],
            spacing=10,
            width=340,
        )
    )

ft.run(main)
