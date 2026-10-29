"""Ask a set of test questions (run from backend/): uv run python try_questions.py"""
from rag.retrieval import ask_question

QUESTIONS = [
    "What was the total revenue in FY2024?",
    "What payment terms do servo motor suppliers get?",
    "What is the customs duty for programmable controllers imported from Japan?",
    "Over how many years is filling line equipment depreciated?",
    "Who won the football world cup 2022?",
]

MODE = "similarity"  # or "multiquery" / "contextual"

for number, question in enumerate(QUESTIONS, 1):
    print(f"\n{number}. {question}")
    print("    " + ask_question(question, MODE).replace("\n", "\n    "))
