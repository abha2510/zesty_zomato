import os
from tabulate import tabulate

menu_file = "menu.txt"
orders_file = "orders.txt"

menu = []
orders = []
order_id_counter = 1

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_menu():
    clear_screen()
    headers = ["ID", "Dish Name", "Price", "Availability"]
    table_data = [[dish["id"], dish["name"], dish["price"], "Yes" if dish["availability"] else "No"] for dish in menu]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    input("Press Enter to continue.")

def add_dish():
    clear_screen()
    dish_id = input("Enter dish ID: ")
    dish_name = input("Enter dish name: ")
    dish_price = float(input("Enter dish price: "))
    dish_availability = input("Is the dish available? (yes/no): ").lower() == "yes"
    menu.append({
        "id": dish_id,
        "name": dish_name,
        "price": dish_price,
        "availability": dish_availability
    })
    print("Dish added to the menu.")
    input("Press Enter to continue.")

def remove_dish():
    clear_screen()
    dish_id = input("Enter the dish ID to remove: ")
    for dish in menu:
        if dish["id"] == dish_id:
            menu.remove(dish)
            print("Dish removed from the menu.")
            break
    else:
        print("Dish not found in the menu.")
    input("Press Enter to continue.")

def update_availability():
    clear_screen()
    dish_id = input("Enter the dish ID to update availability: ")
    for dish in menu:
        if dish["id"] == dish_id:
            dish["availability"] = not dish["availability"]
            print("Availability updated.")
            break
    else:
        print("Dish not found in the menu.")
    input("Press Enter to continue.")


def take_order():
    global order_id_counter
    clear_screen()
    customer_name = input("Enter customer name: ")
    print("Menu:")
    headers = ["ID", "Dish Name", "Price", "Availability"]
    table_data = [[dish["id"], dish["name"], dish["price"], "Available" if dish["availability"] else "Not Available"] for dish in menu]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    dish_ids = input("Enter dish IDs (comma-separated) from the menu: ").split(",")
    ordered_dishes = []
    total_price = 0
    for dish_id in dish_ids:
        for dish in menu:
            if dish["id"] == dish_id and dish["availability"]:
                ordered_dishes.append(dish)
                total_price += dish["price"]
                break
    else:
        if not ordered_dishes:
            print("No dishes added to the order or invalid dish IDs.")
        else:
            order = {
                "id": order_id_counter,
                "customer_name": customer_name,
                "dishes": ordered_dishes,
                "status": "Received",
                "total_price": total_price
            }
            orders.append(order)
            order_id_counter += 1
            print("Order placed successfully.")
    input("Press Enter to continue.")



# Rest of the code remains the same
def update_order_status():
    clear_screen()
    order_id = int(input("Enter the order ID to update status: "))
    for order in orders:
        if order["id"] == order_id:
            print("1. Received")
            print("2. Preparing")
            print("3. Ready for Pickup")
            print("4. Delivered")
            status_choice = input("Enter the new status (1-4): ")
            if status_choice == "1":
                order["status"] = "Received"
            elif status_choice == "2":
                order["status"] = "Preparing"
            elif status_choice == "3":
                order["status"] = "Ready for Pickup"
            elif status_choice == "4":
                order["status"] = "Delivered"
            else:
                print("Invalid status choice.")
            print("Status updated.")
            break
    else:
        print("Order not found.")
    input("Press Enter to continue.")

def review_orders():
    clear_screen()
    if not orders:
        print("No orders placed.")
    else:
        headers = ["Order ID", "Customer Name", "Dishes", "Total Price", "Status"]
        table_data = []
        for order in orders:
            dish_names = [dish["name"] for dish in order["dishes"]]
            dishes_str = ", ".join(dish_names)
            table_data.append([order["id"], order["customer_name"], dishes_str, order["total_price"], order["status"]])
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    input("Press Enter to continue.")


def filter_orders_by_status():
    clear_screen()
    status_choice = input("Enter the status to filter orders by (Received/Preparing/Ready for Pickup/Delivered): ")
    filtered_orders = [order for order in orders if order["status"].lower() == status_choice.lower()]
    if not filtered_orders:
        print(f"No orders with status '{status_choice}'.")
    else:
        headers = ["Order ID", "Customer Name", "Dishes", "Total Price", "Status"]
        table_data = []
        for order in filtered_orders:
            dish_names = [dish["name"] for dish in order["dishes"]]
            dishes_str = ", ".join(dish_names)
            table_data.append([order["id"], order["customer_name"], dishes_str, order["total_price"], order["status"]])
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    input("Press Enter to continue.")

def save_data():
    with open(menu_file, "w") as f:
        for dish in menu:
            f.write(f"{dish['id']},{dish['name']},{dish['price']},{dish['availability']}\n")

    with open(orders_file, "w") as f:
        for order in orders:
            dish_ids = ",".join([dish['id'] for dish in order['dishes']])
            f.write(f"{order['id']},{order['customer_name']},{dish_ids},{order['status']},{order['total_price']}\n")

def load_data():
    try:
        with open(menu_file, "r") as f:
            for line in f:
                dish_data = line.strip().split(",")
                dish = {
                    "id": dish_data[0],
                    "name": dish_data[1],
                    "price": float(dish_data[2]),
                    "availability": dish_data[3] == "True"
                }
                menu.append(dish)

        with open(orders_file, "r") as f:
            for line in f:
                order_data = line.strip().split(",")
                order_dishes = []
                dish_ids = order_data[2].split(",")
                for dish_id in dish_ids:
                    for dish in menu:
                        if dish["id"] == dish_id:
                            order_dishes.append(dish)
                            break

                order = {
                    "id": int(order_data[0]),
                    "customer_name": order_data[1],
                    "dishes": order_dishes,
                    "status": order_data[3],
                    "total_price": float(order_data[4])
                }
                orders.append(order)

        global order_id_counter
        if orders:
            order_id_counter = orders[-1]["id"] + 1

    except FileNotFoundError:
        pass

def main():
    global order_id_counter
    load_data()
    while True:
        clear_screen()
        print("Zesty Zomato - Main Menu")
        print("1. Display Menu")
        print("2. Add Dish")
        print("3. Remove Dish")
        print("4. Update Dish Availability")
        print("5. Take Order")
        print("6. Update Order Status")
        print("7. Review Orders")
        print("8. Filter Orders by Status")
        print("9. Exit")
        choice = input("Enter your choice (1-9): ")
        if choice == "1":
            display_menu()
        elif choice == "2":
            add_dish()
        elif choice == "3":
            remove_dish()
        elif choice == "4":
            update_availability()
        elif choice == "5":
            take_order()
        elif choice == "6":
            update_order_status()
        elif choice == "7":
            review_orders()
        elif choice == "8":
            filter_orders_by_status()
        elif choice == "9":
            save_data()
            print("Exiting the program. Data has been saved.")
            break
        else:
            print("Invalid choice. Please try again.")
        clear_screen()

if __name__ == "__main__":
    main()