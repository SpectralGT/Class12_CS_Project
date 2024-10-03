import mysql.connector
from datetime import datetime
import inquirer

# Connect to the MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="test1",  # Use your MySQL username
        password="password",  # Use your MySQL password
        database="expense_tracker"
    )

# Add a transaction (income or expense)
def add_transaction(transaction_type, category, amount):
    db = connect_db()
    cursor = db.cursor()

    query = "INSERT INTO transactions (date, type, category, amount) VALUES (%s, %s, %s, %s)"
    values = (datetime.now().strftime('%Y-%m-%d'), transaction_type, category, amount)
    
    cursor.execute(query, values)
    db.commit()
    
    print(f"{transaction_type.capitalize()} of {amount} added to category '{category}'")
    cursor.close()
    db.close()

# View all transactions
def view_transactions():
    db = connect_db()
    cursor = db.cursor()

    query = "SELECT * FROM transactions ORDER BY date"
    cursor.execute(query)
    records = cursor.fetchall()

    print("\nDate       | Type    | Category         | Amount")
    print("---------------------------------------------")
    for row in records:
        print(f"{row[1]} | {row[2]:<7} | {row[3]:<15} | {row[4]:.2f}")

    cursor.close()
    db.close()

# Display a summary of income, expenses, and balance
def summary():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    expenses = cursor.fetchone()[0] or 0

    balance = income - expenses
    
    print("\nSummary:")
    print(f"Total Income  : {income:.2f}")
    print(f"Total Expenses: {expenses:.2f}")
    print(f"Balance       : {balance:.2f}")

    cursor.close()
    db.close()

# Function to handle user choices
def menu():
    questions = [
        inquirer.List(
            'option',
            message="What do you want to do?",
            choices=[
                'Add a transaction',
                'View all transactions',
                'Show summary report',
                'Exit'
            ]
        )
    ]

    answers = inquirer.prompt(questions)
    
    if answers['option'] == 'Add a transaction':
        add_transaction_flow()
    elif answers['option'] == 'View all transactions':
        view_transactions()
    elif answers['option'] == 'Show summary report':
        summary()
    elif answers['option'] == 'Exit':
        print("Exiting...")

# Function to prompt for transaction details
def add_transaction_flow():
    # Prompt user for transaction details
    type_question = [
        inquirer.List(
            'type',
            message="What type of transaction?",
            choices=['income', 'expense']
        )
    ]
    type_answer = inquirer.prompt(type_question)

    category_question = [
        inquirer.Text('category', message="Enter the category (e.g., Salary, Groceries)")
    ]
    category_answer = inquirer.prompt(category_question)

    amount_question = [
        inquirer.Text('amount', message="Enter the amount", validate=lambda _, x: x.isdigit() or x.replace('.', '', 1).isdigit())
    ]
    amount_answer = inquirer.prompt(amount_question)

    # Add the transaction
    add_transaction(type_answer['type'], category_answer['category'], float(amount_answer['amount']))

# Main loop for CLI interaction
if __name__ == '__main__':

    print("""┳┳┓   ┓    ┓     ┏┓ ┓         ┏┓•    ┓ 
┃┃┃┏┓┏┫┏┓  ┣┓┓┏  ┣┫╋┣┓┏┓┏┓┓┏  ┗┓┓┏┓┏┓┣┓
┛ ┗┗┻┗┻┗   ┗┛┗┫  ┛┗┗┛┗┗┻┛ ┗┛  ┗┛┗┛┗┗┫┛┗
              ┛                     ┛  """)

    while True:
        menu()
        again_question = [
            inquirer.List(
                'continue',
                message="Do you want to perform another operation?",
                choices=['Yes', 'No']
            )
        ]
        again_answer = inquirer.prompt(again_question)
        if again_answer['continue'] == 'No':
            print("Goodbye!")
            break
