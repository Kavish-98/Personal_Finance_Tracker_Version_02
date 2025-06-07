import json
from datetime import datetime

# Initialize Global dictionary to store transactions
transactions = {}
count = len(transactions)

# Function to load transactions from a JSON file
def load_transactions():
    global transactions
    try:
        with open("transactions.json", "r") as file:
            transactions = json.load(file)
            if not isinstance(transactions, dict):
                print("Invalid JSON data. Starting with an empty dictionary.")
                transactions = {}
    except FileNotFoundError:
        print("File not found. Starting with an empty dictionary.")
    except json.JSONDecodeError:
        print("Invalid JSON format. Starting with an empty dictionary.")

# Function to save transactions to a JSON file
def save_transactions():
    with open("transactions.json", "w") as file:
        json.dump(transactions, file, indent=4)

# Function to open and read the file, then parse each line to add to the transactions dictionary
def read_bulk_transactions_from_file():
    global transactions
    while True:
        try:
            file_name = input('Enter the file name without extension : ')
            with open(f'{file_name}.txt', 'r') as file:
                for line in file:
                    line = line.strip().split(',')
                    # Check if the line has the correct number of elements
                    if len(line) == 4:
                        category = line[0].capitalize()
                        amount = float(line[1])
                        transaction_type = line[2].upper()
                        date = line[3]
                        if category in transactions.keys():
                            transactions[category].append({"amount": amount, "type": transaction_type, "date": date})
                        else:
                            transactions.update({category:[{"amount": amount, "type": transaction_type, "date": date}]})
                save_transactions()
                print('Bulk reading success!\n')
                break
        except FileNotFoundError:
            print('Invalid text file!')

# Function to handle input errors and validate user inputs

# Function to transaction choice error handling
def transactions_choice_error_handling(message):
    while True:
        try:
            choice = int(input(message))
        except ValueError:
            print("Invalid choice.please try again!!!")
        else:
            if 0 < choice <= 7 :
                return choice
            else:
                print("Invalid choice.please try again!!!")
                
# Function to transaction amount error handling
def transactions_amount_error_handling(message):
    while True:
        try:
            transactions_amount = float(input(message))
        except ValueError:
            print("Invalid Input!!!")
            continue
        else:
            return transactions_amount
        
#Function to Transaction category error handling        
def transactions_category_error_handling(message):
    while True:
        transactions_category = input(message).capitalize()
        if transactions_category != '':
            return transactions_category
        else:
            continue
           
##Function to Transaction type error handling  
def transactions_type_error_handling(message):
    while True:
        value = input(message).upper()
        if value == "INCOME" or value == "EXPENSE":
            return value
        else:
            print("Invalid Input!!!")

##Function to Transaction date error handling  
def transactions_date_error_handling(message):
    while True:
        value = input(message)
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return value
        except ValueError:
            print("Invalid Input!!!")
            
##Function to Transaction index error handling  
def transactions_index_error_handling(message, category):
    while True:
        try:
            value = int(input(message))
        except ValueError:
            print("Invalid Input!!!")
        else:
            if value <= 0 or value > len(transactions[category]):
                print("Invalid transaction index.")
            else:
                return value

# Function to add a new transaction to the dictionary
def add_transactions():
    global transactions
    category = transactions_category_error_handling("Enter the category:")
    amount = transactions_amount_error_handling("Enter the amount:")
    transaction_type = transactions_type_error_handling("Enter the type (Income/Expense):")
    date = transactions_date_error_handling("Enter the date (YYYY-MM-DD):")
    if category in transactions.keys():
        transactions[category].append({"amount": amount, "type": transaction_type, "date": date})
    else:
        transactions.update({category:[{"amount": amount, "type": transaction_type, "date": date}]})
    save_transactions()
    print("\nTransaction successfully saved!!\n")

# Function to view all transactions
def view_transactions():
    global transactions
    count = 1
    if not transactions:
        print("No transactions  found.")
        return
    for key, value in transactions.items():
        print('\nTransaction category : ',key)
        for transaction in value:
            print('\tTransaction number : ',count)
            print('\t\t' + str(transaction))
            count+=1
        count = 1

# Function to update an existing transaction
def update_transactions():
    global transactions
    view_transactions()
    if not transactions:
        return
    category = transactions_category_error_handling("Enter the category:")
    while category not in transactions.keys():
        print("Please enter a category that already exists!!")
        category = transactions_category_error_handling("Enter the category:")
    update_index = transactions_index_error_handling("Enter which transaction to update:",category)
    amount = transactions_amount_error_handling("Enter the new amount:")
    transaction_type = transactions_type_error_handling("Enter the new type (Income/Expense):")
    date = transactions_date_error_handling("Enter the new date (YYYY-MM-DD):")
    transactions[category][update_index - 1] = {"amount": amount, "type": transaction_type, "date": date}
    save_transactions()
    print("\nTransaction successfully updated!!\n")

# Function to delete a transaction
def delete_transactions():
    global transactions
    count = 0
    view_transactions()
    if not transactions:
        return
    category = transactions_category_error_handling("Enter the category:")
    while category not in transactions.keys():
        print("Please enter a category that already exists!!")
        category = transactions_category_error_handling("Enter the category:")
    update_index = transactions_index_error_handling("Enter which transaction to delete:",category)
    del transactions[category][update_index - 1]
    if len(transactions[category]) == 0:
        del transactions[category]
    save_transactions()
    print("\nTransaction successfully deleted!!\n")

# Function to display summary
def display_summary():
    global transactions
    total_income = sum(transaction["amount"] for category_transactions in transactions.values() for transaction in category_transactions if transaction["type"] == "INCOME")
    total_expense = sum(transaction["amount"] for category_transactions in transactions.values() for transaction in category_transactions if transaction["type"] == "EXPENSE")
    balance = total_income - total_expense
    print(f"\nTotal_Income: {total_income}")
    print(f"Total Expense: {total_expense}")
    print(f"Balance: {balance}\n")

# Main function
def main_menu():
    load_transactions()
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Read data in bulk")
        print("7. Exit")
        choice = transactions_choice_error_handling("Enter your choice:")
        if choice == 1:
            add_transactions()
        elif choice == 2:
            view_transactions()
        elif choice == 3:
            update_transactions()
        elif choice == 4:
            delete_transactions()
        elif choice == 5:
            display_summary()
        elif choice == 6:
            read_bulk_transactions_from_file()
        elif choice == 7:
            print("Exiting program.")
            break
        else:
            print("Invalid choice. please try again")

if __name__ == "__main__":
    main_menu()
