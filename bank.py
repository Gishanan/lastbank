import random
import os
from getpass import getpass
from datetime import datetime

accounts = {}

ACCOUNT_FILE = "account.txt"

datetime.now()

# Load accounts from file
def load_accounts():
    if not os.path.exists(ACCOUNT_FILE):
        return
    with open(ACCOUNT_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 6:
                user_id, acc_no, name, balance, password, tx_str = parts
                transactions = tx_str.split("|") if tx_str else []
                accounts[acc_no] = {
                    "user_id": user_id,
                    "name": name,
                    "balance": float(balance),
                    "password": password,
                    "transactions": transactions
                }

# Save accounts to file
def save_accounts():
    with open(ACCOUNT_FILE, "w") as f:
        for acc_no, acc in accounts.items():
            tx_str = "|".join(acc["transactions"])
            f.write(f"{acc['user_id']},{acc_no},{acc['name']},{acc['balance']},{acc['password']},{tx_str}\n")

# Generate  user ID
def create_account_id():
    if not os.path.exists(ACCOUNT_FILE) or os.path.getsize(ACCOUNT_FILE) == 0:
        return "g001"
    with open(ACCOUNT_FILE, "r") as f:
        last_line = f.readlines()[-1]
        last_id = int(last_line.split(",")[0][1:])
        return f"g{last_id + 1:03}"

# Generate unique account number
def generate_account_number():
    while True:
        account_number = "77" + str(random.randint(100000000, 999999999))
        if account_number not in accounts:
            return account_number

#current datetime
def get_datetime():
    current= datetime.now()
    return current                    

# Create account
def create_account():
    name = input("Enter account holder name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name = input("Enter account holder name: ").strip()

    while True:
        try:
            balance = float(input("Enter initial balance: "))
            if balance < 0:
                print("Balance must be non-negative.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    while True:
        password = getpass("Set a password: ")
        confirm = getpass("Confirm password: ")
        if password == confirm:
            break
        else:
            print("Passwords do not match.")

    acc_no = generate_account_number()
    user_id = create_account_id()

    accounts[acc_no] = {
        "user_id": user_id,
        "name": name,
        "balance": balance,
        "password": password,
        "transactions": []
    }
    save_accounts()
    print(f"Account created successfully! Account Number: {acc_no}")

# Authenticate user
def authenticate():
    acc_no = input("Enter account number: ").strip()
    if acc_no not in accounts:
        print("Account not found.")
        return None
    password = getpass("Enter password: ")
    if accounts[acc_no]["password"] != password:
        print("Incorrect password.")
        return None
    return acc_no

# Deposit
def deposit_money():
    acc_no = authenticate()
    if not acc_no:
        return
    try:
        amount = float(input("Enter deposit amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Invalid amount.")
        return
    datetime = get_datetime()

    accounts[acc_no]["balance"] += amount
    accounts[acc_no]["transactions"].append(f"{datetime}Deposit: +{amount}")
    save_accounts()
    print("====== Deposit successful ======")
    print(f"New Balance: {accounts[acc_no]['balance']}")

# Withdraw
def withdraw_money():
    acc_no = authenticate()
    if not acc_no:
        return
    try:
        amount = float(input("Enter withdrawal amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Invalid amount.")
        return

    if amount > accounts[acc_no]["balance"]:
        print("Insufficient balance.")
        return
    datetime = get_datetime()
    accounts[acc_no]["balance"] -= amount
    accounts[acc_no]["transactions"].append(f"{datetime}Withdrawal: -{amount}")
    save_accounts()
    print("====== Withdrawal successful ======")
    print(f"New Balance: {accounts[acc_no]['balance']}")

# Check balance
def check_balance():
    acc_no = authenticate()
    if not acc_no:
        return
    print(f"Account Holder: {accounts[acc_no]['name']}")
    print(f"Current Balance: Rs.{accounts[acc_no]['balance']}")

# View transaction history
def view_transaction_history():
    datetime.now()
    acc_no = authenticate()
    if not acc_no:
        return
    print(f"\nTransaction History for {datetime} {acc_no} ({accounts[acc_no]['name']}):")
    tx = accounts[acc_no]["transactions"]
    if not tx:
        print("No transactions yet.")
    else:
        for t in tx:
            print(f" - {t}")

# Transfer money
def transfer_money():
    sender = authenticate()
    if not sender:
        return
    receiver = input("Enter recipient account number: ").strip()
    if receiver not in accounts:
        print("Recipient account not found.")
        return
    if sender == receiver:
        print("Cannot transfer to the same account.")
        return
    try:
        amount = float(input("Enter amount to transfer: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Invalid amount.")
        return
    if amount > accounts[sender]["balance"]:
        print("Insufficient funds.")
        return

    accounts[sender]["balance"] -= amount
    accounts[receiver]["balance"] += amount
    accounts[sender]["transactions"].append(f"Transfer to {receiver}: -{amount}")
    accounts[receiver]["transactions"].append(f"Transfer from {sender}: +{amount}")
    save_accounts()
    print("====== Transfer successful ======")

# Main menu
def main():
    load_accounts()
    while True:
        print("\n===== Banking Application =====")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Transfer Money")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            create_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            view_transaction_history()
        elif choice == '6':
            transfer_money()
        elif choice == '7':
            print("Thank you for using the banking app!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
