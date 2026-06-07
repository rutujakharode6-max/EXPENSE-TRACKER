import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"

def initialize_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({"budget": 1000.0, "expenses": []}, f)

def get_data():
    initialize_data()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_expense(desc, amount, category, date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
        
    data = get_data()
    expense = {
        "id": int(datetime.now().timestamp() * 1000),
        "desc": desc,
        "amount": float(amount),
        "category": category,
        "date": date_str
    }
    data["expenses"].append(expense)
    save_data(data)
    return expense

def delete_expense(expense_id):
    data = get_data()
    data["expenses"] = [e for e in data["expenses"] if e["id"] != expense_id]
    save_data(data)

def set_budget(amount):
    data = get_data()
    data["budget"] = float(amount)
    save_data(data)

def get_budget():
    data = get_data()
    return data.get("budget", 1000.0)

def get_expenses():
    data = get_data()
    return data.get("expenses", [])

def get_category_totals():
    expenses = get_expenses()
    totals = {}
    for exp in expenses:
        cat = exp["category"]
        totals[cat] = totals.get(cat, 0) + exp["amount"]
    return totals
