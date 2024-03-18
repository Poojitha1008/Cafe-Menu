# Define the cafe menu using a list of tuples where each tuple contains the item name and its price
cafe_menu = [
    ("Espresso", 1.50),
    ("Latte", 2.00),
    ("Cappuccino", 2.25),
    ("Mocha", 2.50),
    ("Americano", 2.00)
]

# Function to display the menu
def display_menu():
    print("Welcome to the Cafe!")
    print("Menu:")
    for index, item in enumerate(cafe_menu, start=1):
        print(f"{index}. {item[0]}")

# Function to take user input and process their order
def place_order():
    while True:
        try:
            choice = int(input("Enter the number of the item you'd like to order (or 0 to exit): "))
            if choice == 0:
                print("Thank you for visiting. Have a great day!")
                break
            elif choice < 1 or choice > len(cafe_menu):
                print("Invalid choice. Please enter a number within the range.")
            else:
                selected_item = cafe_menu[choice - 1]
                print(f"You've selected: {selected_item[0]} - ${selected_item[1]}")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Main function
def main():
    display_menu()
    place_order()
    print("Thank you for your order! We hope to see you again soon.")

# Run the main function
if __name__ == "__main__":
    main()
