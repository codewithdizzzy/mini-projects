"""A simple daily expense tracker that stores data in a JSON file."""

from __future__ import annotations

import json
import math
from datetime import date
from pathlib import Path
from typing import Any


DEFAULT_FILE = Path(__file__).with_name("expenses.json")


def load_expenses(file_path: Path = DEFAULT_FILE) -> list[dict[str, Any]]:
    """Load expenses from JSON, returning an empty list when the file is absent."""
    try:
        with file_path.open("r", encoding="utf-8") as file:
            expenses = json.load(file)
    except FileNotFoundError:
        return []
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Could not read {file_path}: {error}") from error

    if not isinstance(expenses, list):
        raise ValueError("The expense file does not contain a list of expenses.")
    return expenses


def save_expenses(expenses: list[dict[str, Any]], file_path: Path = DEFAULT_FILE) -> None:
    """Save expenses safely, replacing the old file only after writing succeeds."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_file = file_path.with_suffix(".tmp")
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=2)
            file.write("\n")
        temporary_file.replace(file_path)
    except OSError as error:
        raise ValueError(f"Could not save {file_path}: {error}") from error


def get_date() -> str:
    """Return today's date in a simple, readable format."""
    return date.today().isoformat()


def get_amount(message: str) -> float:
    """Ask for a valid positive amount."""
    while True:
        try:
            amount = float(input(message))
            if not math.isfinite(amount) or amount <= 0:
                raise ValueError
        except ValueError:
            print("Enter a valid amount greater than zero.")
            continue
        return amount


def add_expense(expenses: list[dict[str, Any]], file_path: Path) -> None:
    """Add one expense to the list and save it."""
    description = input("Description: ").strip()
    while not description:
        print("Description cannot be empty.")
        description = input("Description: ").strip()

    category = input("Category (food, transport, shopping, bills, entertainment, other): ").strip().lower()
    while not category:
        print("Category cannot be empty.")
        category = input("Category: ").strip().lower()

    amount = get_amount("Amount: ")
    expense = {
        "date": get_date(),
        "description": description,
        "category": category,
        "amount": round(amount, 2),
    }
    expenses.append(expense)
    save_expenses(expenses, file_path)
    print(f"Expense added: ${amount:.2f}")


def show_expenses(expenses: list[dict[str, Any]]) -> None:
    """Display all expenses in a readable table."""
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\nYour expenses:")
    print("-" * 70)
    for expense in expenses:
        print(
            f"{expense['date']} | {expense['description']} | "
            f"{expense['category']} | ${expense['amount']:.2f}"
        )
    print("-" * 70)


def show_summary(expenses: list[dict[str, Any]]) -> None:
    """Show total spending and spending by category."""
    total = round(sum(expense["amount"] for expense in expenses), 2)
    category_totals: dict[str, float] = {}

    for expense in expenses:
        category = expense.get("category", "other")
        category_totals[category] = round(category_totals.get(category, 0) + expense["amount"], 2)

    print(f"\nTotal spent: ${total:.2f}")
    print("Spending by category:")
    for category, amount in sorted(category_totals.items()):
        print(f"  {category}: ${amount:.2f}")


def delete_expense(expenses: list[dict[str, Any]], file_path: Path) -> None:
    """Delete an expense selected by its number from the list."""
    if not expenses:
        print("There are no expenses to delete.")
        return

    show_expenses(expenses)
    choice = input("Expense number to delete: ")
    try:
        index = int(choice) - 1
    except ValueError:
        print("Enter a valid expense number.")
        return

    if index < 0 or index >= len(expenses):
        print("Expense number is out of range.")
        return

    deleted = expenses.pop(index)
    save_expenses(expenses, file_path)
    print(f"Deleted: {deleted['description']} for ${deleted['amount']:.2f}")


def main() -> None:
    """Run the interactive expense tracker."""
    file_path = DEFAULT_FILE
    try:
        expenses = load_expenses(file_path)
    except ValueError as error:
        print(error)
        return

    print("Daily Expense Tracker")
    print("=" * 24)

    while True:
        print("\n1. Add expense")
        print("2. View expenses")
        print("3. View summary")
        print("4. Delete expense")
        print("5. Save and exit")
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                add_expense(expenses, file_path)
            elif choice == "2":
                show_expenses(expenses)
            elif choice == "3":
                show_summary(expenses)
            elif choice == "4":
                delete_expense(expenses, file_path)
            elif choice == "5":
                save_expenses(expenses, file_path)
                print("Goodbye!")
                break
            else:
                print("Invalid option. Choose a number from 1 to 5.")
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    main()
