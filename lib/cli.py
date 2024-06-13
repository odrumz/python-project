# Import libraries
import sqlite3
from helpers import exit_program
from datetime import datetime

# Function to create database tables
def create_tables():
    conn = sqlite3.connect("farm.db")
    cursor = conn.cursor()

    # Create products table
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
        farm_id INTEGER PRIMARY KEY AUTOINCREMENT,
        farm_product TEXT NOT NULL,
        quantity INTEGER,
        day_id INTEGER,
        FOREIGN KEY (day_id) REFERENCES days(day_id)
    )''')

    # Create days table
    cursor.execute('''CREATE TABLE IF NOT EXISTS days (
        day_id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT NOT NULL
    )''')

    conn.commit()
    conn.close()

# Initialize database tables
create_tables()

# Farm class
class Farm:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("farm.db")
        self.cursor = self.conn.cursor()

    def add_product(self, farm_product, quantity):
        # Insert product into products table
        self.cursor.execute('INSERT INTO products (farm_product, quantity) VALUES (?, ?)', (farm_product, quantity))
        self.conn.commit()

    def add_day(self, day):
        # Insert day into days table
        self.cursor.execute('INSERT INTO days (day) VALUES (?)', (day,))
        self.conn.commit()

    def link(self, day_id, farm_id):
        # Check if day_id exists
        self.cursor.execute('SELECT * FROM days WHERE day_id = ?', (day_id,))
        if not self.cursor.fetchone():
            print("Day ID does not exist.")
            return

        # Link product with the specified day
        self.cursor.execute('UPDATE products SET day_id = ? WHERE farm_id = ?', (day_id, farm_id))
        self.conn.commit()
        print(f"Day ID ({day_id}) is linked to farm_id ({farm_id}).")

    def details(self):
        # Fetch details of products with their linked days
        query = '''SELECT products.farm_id, products.farm_product, products.quantity, days.day_id, days.day
                   FROM products
                   LEFT JOIN days ON products.day_id = days.day_id'''
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def search_product(self, search_term):
        # Search for a product by name or day
        self.cursor.execute('''SELECT products.farm_id, products.farm_product, products.quantity, days.day_id, days.day
                               FROM products
                               LEFT JOIN days ON products.day_id = days.day_id
                               WHERE products.farm_product LIKE ? OR days.day LIKE ?''', ('%' + search_term + '%', '%' + search_term + '%'))
        return self.cursor.fetchall()
  
    def delete_product(self, farm_id):
        # Check if farm_id exists
        self.cursor.execute('SELECT * FROM products WHERE farm_id = ?', (farm_id,))
        if not self.cursor.fetchone():
            print(f'No product found with farm_id ({farm_id}).')
            return

        # Delete product with the specified farm_id
        self.cursor.execute('DELETE FROM products WHERE farm_id = ?', (farm_id,))
        self.conn.commit()
        print(f"Product with farm_id ({farm_id}) has been deleted.")

# Function to create customer and orders tables
def create_customer_tables():
    conn = sqlite3.connect("customer.db")
    cursor = conn.cursor()

    # Create customers table
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone_number INTEGER
    )''')

    # Create orders table
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        farm_product TEXT NOT NULL,
        quantity INTEGER,
        order_date DATE NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )''')

    conn.commit()
    conn.close()

# Initialize customer and orders tables
create_customer_tables()

# Customer class
class Customer:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("customer.db")
        self.cursor = self.conn.cursor()

    def add_customer(self, name, phone_number):
        # Insert customer into customers table
        self.cursor.execute('INSERT INTO customers (name, phone_number) VALUES (?, ?)', (name, phone_number))
        self.conn.commit()
    
    def add_order(self, customer_id, farm_product, quantity, order_date):
        try:
            # Validate and format order_date
            order_date = datetime.strptime(order_date, '%Y-%m-%d').date()
            # Insert order into orders table
            self.cursor.execute('INSERT INTO orders (customer_id, farm_product, quantity, order_date) VALUES (?, ?, ?, ?)', 
                                (customer_id, farm_product, quantity, order_date))
            self.conn.commit()
            print("Order added successfully.")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    def search_order(self, search_term):
        # Search for an order by product name or customer name
        self.cursor.execute('''SELECT orders.order_id, customers.name, orders.farm_product, orders.quantity, orders.order_date
                               FROM orders
                               JOIN customers ON orders.customer_id = customers.customer_id
                               WHERE orders.farm_product LIKE ? OR customers.name LIKE ?''', 
                               ('%' + search_term + '%', '%' + search_term + '%'))
        return self.cursor.fetchall()

    def delete_order(self, order_id):
        # Check if order_id exists
        self.cursor.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
        if not self.cursor.fetchone():
            print(f'No order found with order_id ({order_id}).')
            return

        # Delete order with the specified order_id
        self.cursor.execute('DELETE FROM orders WHERE order_id = ?', (order_id,))
        self.conn.commit()
        print(f"Order with order_id ({order_id}) has been deleted.")

    def display(self):
        # Fetch details of customers and their orders
        query = '''SELECT customers.customer_id, customers.name, customers.phone_number, orders.order_id, orders.farm_product, 
                          orders.quantity, orders.order_date
                   FROM customers
                   LEFT JOIN orders ON customers.customer_id = orders.customer_id'''
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        if records:
            for record in records:
                print(  f"{record[1]} has ordered {record[5]} bags of {record[4]} on {record[6]}")
            
        else:
            print("No customers or orders found.")

# Function to display menu options
def menu():
    print("Please select an option:")
    print("1. Add product")
    print("2. Add day")
    print("3. Link the product with the day collected")
    print("4. Display details")
    print("5. Search product")
    print("6. Delete product")
    print("7. Add customer")
    print("8. Add order")
    print("9. Display customers and orders")
    print("10. Search order")
    print("11. Delete order")
    print("0. Exit the program")

# Main function
def main():
    farm_db = Farm()
    customer_db = Customer()
    while True:
        menu()
        choice = input(">>> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            farm_product = input("Enter product: ")
            quantity = input("Enter quantity: ")
            farm_db.add_product(farm_product, quantity)
        elif choice == "2":
            day = input("Enter day: ")
            farm_db.add_day(day)
        elif choice == "3":
            day_id = int(input("Enter day id: "))
            farm_id = int(input("Enter farm id: "))
            farm_db.link(day_id, farm_id)
        elif choice == "4":
            details = farm_db.details()
            for detail in details:
                print(f"On {detail[4]}, {detail[2]} bags {detail[1]} were collected.")
        elif choice == "5":
            search_term = input("Enter product name or day to search: ")
            products = farm_db.search_product(search_term)
            if products:
                for product in products:
                    print(f"Farm ID: {product[0]}, Product: {product[1]}, Quantity: {product[2]}, Day ID: {product[3]}, Day: {product[4]}")
            else:
                print("No matching products found.")
        elif choice == "6":
            farm_id = int(input("Enter farm_id to DELETE : "))
            farm_db.delete_product(farm_id)
        elif choice == "7":
            name = input("Enter customer name: ")
            phone_number = input("Enter customer phone number: ")
            customer_db.add_customer(name, phone_number)
        elif choice == "8":
            customer_id = int(input("Enter customer ID: "))
            farm_product = input("Enter product: ")
            quantity = int(input("Enter quantity: "))
            order_date = input("Enter order date (YYYY-MM-DD): ")
            customer_db.add_order(customer_id, farm_product, quantity, order_date)
        elif choice == "9":
            customer_db.display()
        elif choice == "10":
            search_term = input("Enter product name or customer name to search: ")
            orders = customer_db.search_order(search_term)
            if orders:
                for order in orders:
                    print(f"Order ID: {order[0]}, Customer Name: {order[1]}, Product: {order[2]}, Quantity: {order[3]}, Order Date: {order[4]}")
            else:
                print("No matching orders found.")
        elif choice == "11":
            order_id = int(input("Enter order_id to DELETE : "))
            customer_db.delete_order(order_id)
        else:
            print("Invalid option")

# Execute main function
if __name__ == "__main__":
    main()
