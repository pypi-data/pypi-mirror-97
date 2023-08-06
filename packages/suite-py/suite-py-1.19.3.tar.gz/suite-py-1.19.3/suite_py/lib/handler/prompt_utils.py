# -*- encoding: utf-8 -*-
from PyInquirer import prompt


def ask_confirm(text, default=True):
    questions = [
        {"type": "confirm", "message": text, "name": "continue", "default": default}
    ]
    answer = prompt(questions)
    return bool(answer["continue"])


def ask_questions_input(question_text, default_text=""):
    questions = [
        {
            "type": "input",
            "name": "value",
            "message": question_text,
            "default": default_text,
        }
    ]

    answer = prompt(questions)
    return answer["value"]


def ask_questions_editor(question_text, default_text=""):
    questions = [
        {
            "type": "editor",
            "name": "value",
            "message": question_text,
            "default": default_text,
            "eargs": {"editor": "default"},
        }
    ]

    answer = prompt(questions)
    return answer["value"]


def ask_choices(question_text, choices, default_text=""):
    questions = [
        {
            "type": "list",
            "name": "value",
            "message": question_text,
            "choices": choices,
            "default": default_text,
        }
    ]

    answer = prompt(questions)
    return answer["value"]


def ask_multiple_choices(question_text, choices):
    questions = [
        {
            "type": "checkbox",
            "name": "values",
            "message": question_text,
            "choices": [{"name": choice} for choice in choices],
        }
    ]

    answer = prompt(questions)
    return answer["values"]
