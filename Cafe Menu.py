import sqlite3
import getpass

# Connect to SQLite3 database (creates the database if it does not exist)
conn = sqlite3.connect('cafe_menu_system.db')
cursor = conn.cursor()

# Create necessary tables if they do not exist
def initialize_database():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            employee_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MenuItems (
            item_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            available INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY,
            employee_id INTEGER,
            items TEXT NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Billing (
            bill_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            customer_name TEXT,
            payment_method TEXT,
            total_amount REAL,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        )
    ''')
    conn.commit()

# Function for employee login
def employee_login():
    print("\n--- Employee Login ---")
    employee_id = input("Enter Employee ID: ")
    password = getpass.getpass("Enter Password: ")
    
    cursor.execute('SELECT * FROM Employees WHERE employee_id = ? AND password = ?', (employee_id, password))
    result = cursor.fetchone()
    
    if result:
        print(f"Welcome, {result[1]}!")
        return employee_id
    else:
        print("Invalid Employee ID or Password. Please try again.")
        return None

# Function to add a new menu item
def add_menu_item():
    print("\n--- Add Menu Item ---")
    name = input("Enter item name: ")
    category = input("Enter item category: ")
    price = float(input("Enter item price: "))
    available = int(input("Is the item available? (1 for Yes, 0 for No): "))

    cursor.execute('INSERT INTO MenuItems (name, category, price, available) VALUES (?, ?, ?, ?)', (name, category, price, available))
    conn.commit()
    print("Menu item added successfully.")

# Function to view all menu items
def view_menu_items():
    print("\n--- Menu Items ---")
    cursor.execute('SELECT * FROM MenuItems')
    items = cursor.fetchall()
    
    for item in items:
        print(f"ID: {item[0]}, Name: {item[1]}, Category: {item[2]}, Price: {item[3]}, Available: {'Yes' if item[4] == 1 else 'No'}")

# Function to take an order
def take_order(employee_id):
    print("\n--- Take Order ---")
    order_items = []
    total_amount = 0.0

    while True:
        item_id = int(input("Enter Menu Item ID (0 to finish): "))
        if item_id == 0:
            break
        
        cursor.execute('SELECT * FROM MenuItems WHERE item_id = ? AND available = 1', (item_id,))
        item = cursor.fetchone()

        if item:
            quantity = int(input(f"Enter quantity for {item[1]}: "))
            total_amount += item[3] * quantity
            order_items.append(f"{item[1]} x{quantity} @ {item[3]} each")
        else:
            print("Item not available or does not exist. Please try again.")
    
    cursor.execute('INSERT INTO Orders (employee_id, items, total_amount) VALUES (?, ?, ?)', (employee_id, ', '.join(order_items), total_amount))
    conn.commit()
    print(f"Order placed successfully. Total amount: {total_amount}")

# Function to generate a bill
def generate_bill():
    print("\n--- Generate Bill ---")
    order_id = int(input("Enter Order ID: "))
    cursor.execute('SELECT * FROM Orders WHERE order_id = ?', (order_id,))
    order = cursor.fetchone()

    if order:
        customer_name = input("Enter Customer Name: ")
        payment_method = input("Enter Payment Method (Cash/Card): ")

        cursor.execute('INSERT INTO Billing (order_id, customer_name, payment_method, total_amount) VALUES (?, ?, ?, ?)', 
                       (order_id, customer_name, payment_method, order[3]))
        conn.commit()
        print(f"Bill generated successfully for Order ID: {order_id}.")
    else:
        print("Invalid Order ID. Please try again.")

# Main program loop
def main():
    initialize_database()

    while True:
        print("\n--- Café Menu System ---")
        print("1. Employee Login")
        print("2. Add Menu Item")
        print("3. View Menu Items")
        print("4. Take Order")
        print("5. Generate Bill")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            employee_id = employee_login()
        elif choice == '2':
            add_menu_item()
        elif choice == '3':
            view_menu_items()
        elif choice == '4':
            if employee_id:
                take_order(employee_id)
            else:
                print("Please login first.")
        elif choice == '5':
            generate_bill()
        elif choice == '6':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

# Close the database connection
conn.close()
