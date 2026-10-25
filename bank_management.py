import json
import os
from datetime import datetime

DATA_FILE = "bank_data.json"


def load_accounts():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read account data.")
    return {}


def save_accounts(accounts):
    with open(DATA_FILE, "w") as file:
        json.dump(accounts, file, indent=4)


def create_account(accounts):
    name = input("Enter customer name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    account_no = input("Enter a new account number: ").strip()

    if not account_no.isdigit():
        print("Account number must contain digits only.")
        return

    if account_no in accounts:
        print("Account number already exists.")
        return

    accounts[account_no] = {
        "name": name,
        "balance": 0.0,
        "transactions": []
    }

    save_accounts(accounts)
    print("Account created successfully!")


def find_account(accounts):
    account_no = input("Enter account number: ").strip()

    if account_no not in accounts:
        print("Account not found.")
        return None

    return account_no


def deposit_money(accounts):
    account_no = find_account(accounts)
    if account_no is None:
        return

    try:
        amount = float(input("Enter deposit amount: "))

        if not 0 < amount < 1_000_000_000:
            print("Enter a valid positive amount.")
            return

        account = accounts[account_no]
        account["balance"] = round(account["balance"] + amount, 2)
        account["transactions"].append({
            "type": "Deposit",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        save_accounts(accounts)
        print("Deposit successful!")

    except ValueError:
        print("Please enter a valid number.")


def withdraw_money(accounts):
    account_no = find_account(accounts)
    if account_no is None:
        return

    try:
        amount = float(input("Enter withdrawal amount: "))

        if not 0 < amount < 1_000_000_000:
            print("Enter a valid positive amount.")
            return

        account = accounts[account_no]

        if amount > account["balance"]:
            print("Insufficient balance.")
            return

        account["balance"] = round(account["balance"] - amount, 2)
        account["transactions"].append({
            "type": "Withdrawal",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        save_accounts(accounts)
        print("Withdrawal successful!")

    except ValueError:
        print("Please enter a valid number.")


def check_balance(accounts):
    account_no = find_account(accounts)
    if account_no is None:
        return

    account = accounts[account_no]
    print("Account holder:", account["name"])
    print(f"Available balance: Rs. {account['balance']:.2f}")


def show_transactions(accounts):
    account_no = find_account(accounts)
    if account_no is None:
        return

    transactions = accounts[account_no]["transactions"]

    if not transactions:
        print("No transactions yet.")
        return

    print("\nTransaction History")
    for item in transactions:
        print(
            item["date"],
            "|", item["type"],
            "| Rs.", f"{item['amount']:.2f}"
        )


def main():
    accounts = load_accounts()

    while True:
        print("\n===== BANK MANAGEMENT SYSTEM =====")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_account(accounts)
        elif choice == "2":
            deposit_money(accounts)
        elif choice == "3":
            withdraw_money(accounts)
        elif choice == "4":
            check_balance(accounts)
        elif choice == "5":
            show_transactions(accounts)
        elif choice == "6":
            print("Thank you for using our system!")
            break
        else:
            print("Invalid choice. Please select 1 to 6.")


if __name__ == "__main__":
    main()
