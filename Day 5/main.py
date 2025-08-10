from datetime import date
import csv
import os

categories = ['Food', 'Travel', 'Shopping', 'Bills', 'Misc']
file_name = "expenses.csv"

def add_expense():
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])

    amount = -1
    while amount < 0:
        try:
            amount = float(input('Enter the amount: '))
            if amount < 0:
                print('Please enter positive amount only')
        except ValueError:
            print("Invalid number. Please enter a valid amount.")

    for i in range(len(categories)):
        print(f"{i+1}. {categories[i]}")
    category_choice = 0
    while category_choice < 1 or category_choice > len(categories):
        try:
            category_choice = int(input('Choose one of the categories: '))
            if category_choice < 1 or category_choice > len(categories):
                print('Please enter a valid serial number to choose the category')
        except ValueError:
            print("Invalid choice. Please enter a number.")

    category = categories[category_choice - 1]
    current_date = date.today().strftime("%Y-%m-%d")
    description = input('Enter description (optional): ')

    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([current_date, category, amount, description])

    print(f" Expense added: {current_date}, {category}, {amount}, {description}")

def view_all_expenses():
    if not os.path.exists(file_name):
        print("⚠ No expenses found.")
        return

    choice = input("View (A)ll expenses or (F)ilter by date? ").strip().lower()

    with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
        read = csv.reader(csvfile)
        data = list(read)

        if not data:
            print("No expenses recorded.")
            return

        if choice == 'f':
            filter_date = input("Enter date (YYYY-MM-DD): ").strip()
            rows = [row for row in data if row[0] == filter_date or row[0] == "Date"]
        else:
            rows = data

        
        col_widths = [max(len(str(item)) for item in col) for col in zip(*rows)]
        for row in rows:
            print(" | ".join(str(item).ljust(width) for item, width in zip(row, col_widths)))

def summarise():
    if not os.path.exists(file_name):
        print('⚠ No file found')
        return
    with open(file_name, 'r', newline='', encoding='utf-8') as f:
        read = csv.reader(f)
        next(read, None) 
        total = 0
        for row in read:
            if row and row[2].strip():
                total += float(row[2])
        print(f"💰 Total Expenses: {total}")

def main():
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Summarise Expenses")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_all_expenses()
        elif choice == '3':
            summarise()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
