# import sqlite3
# from helpers import exit_program

# def create_tables():
#     conn = sqlite3.connect("farm.db")
#     cursor = conn.cursor()

#     cursor.execute('''CREATE TABLE IF NOT EXISTS products (
#         farm_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         farm_product TEXT NOT NULL,
#         quantity INTEGER,
#         day_id INTEGER,
#         FOREIGN KEY (day_id) REFERENCES days(day_id)
#     )''')

#     cursor.execute('''CREATE TABLE IF NOT EXISTS days (
#         day_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         day TEXT NOT NULL
#     )''')

#     conn.commit()
#     conn.close()

# create_tables()

# class Farm:
#     def __init__(self) -> None:
#         self.conn = sqlite3.connect("farm.db")
#         self.cursor = self.conn.cursor()

#     def add_product(self, farm_product, quantity):
#         self.cursor.execute('INSERT INTO products (farm_product, quantity) VALUES (?, ?)',
#                             (farm_product, quantity))
#         self.conn.commit()

#     def add_day(self, day):
#         self.cursor.execute('INSERT INTO days (day) VALUES (?)', (day,))
#         self.conn.commit()

#     def record(self, day_id, farm_id):
#         self.cursor.execute('SELECT * FROM products WHERE day_id = ? AND farm_id = ?', (day_id, farm_id))
#         return self.cursor.fetchone() is not None

#     def link(self, day_id, farm_id):
#         if self.record(day_id):
#             self.cursor.execute('UPDATE products SET day_id = ? WHERE farm_id = ?',
#                                 (day_id, farm_id))
#             self.conn.commit()
#             print(f"Day id ({day_id}) is linked to farm_id ({farm_id}).")
#         else:
#             print(f'The details do not exist')

#     def details(self):
#         query = '''SELECT products.farm_id, products.farm_product, products.quantity, days.day_id, days.day
#                 FROM products
#                 LEFT JOIN days ON products.day_id = days.day_id'''
#         self.cursor.execute(query)
#         return self.cursor.fetchall()

        
#     def delete_product(self, farm_id):
#         if self.record(farm_id):  # Pass the farm_id argument to the record method
#             self.cursor.execute('DELETE FROM products WHERE farm_id = ?', (farm_id,))
#             self.conn.commit()
#             print(f"Product with farm_id ({farm_id}) has been deleted.")
#         else:
#             print(f'No product found with farm_id ({farm_id}).')


# def menu():
#     print("Please select an option:")
#     print("1. Add product")
#     print("2. Add day")
#     print("3. Link the product with the day collected")
#     print("4. Display details")
#     print("5. Search product details")
#     print("6. Delete product details")
#     print("0. Exit the program")

# def main():
#     db = Farm()
#     while True:
#         menu()
#         choice = input(">>> ")
#         if choice == "0":
#             exit_program()
#         elif choice == "1":
#             farm_product = input("Enter product: ")
#             quantity = input("Enter quantity: ")
#             db.add_product(farm_product, quantity)
#         elif choice == "2":
#             day = input("Enter day: ")
#             db.add_day(day)
#         elif choice == "3":
#             day_id = int(input("Enter day id: "))
#             farm_id = int(input("Enter farm id: "))
#             db.link(day_id, farm_id)
#         elif choice == "4":
#             details = db.details()
#             for detail in details:
#                 print(f"On {detail[4]}, {detail[2]} {detail[1]} were collected.")
#         # elif choice == "5":
#         elif choice == "6":
#             farm_id = int(input("Enter farm_id to DELETE : "))
#             db.delete_product(farm_id)
#         else:
#             print("Invalid option")

# if __name__ == "__main__":
#     main()


# Import libraries
import sqlite3
from helpers import exit_program

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

# Function to display menu options
def menu():
    print("Please select an option:")
    print("1. Add product")
    print("2. Add day")
    print("3. Link the product with the day collected")
    print("4. Display details")
    print("5. Delete product")
    print("0. Exit the program")

# Main function
def main():
    db = Farm()
    while True:
        menu()
        choice = input(">>> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            farm_product = input("Enter product: ")
            quantity = input("Enter quantity: ")
            db.add_product(farm_product, quantity)
        elif choice == "2":
            day = input("Enter day: ")
            db.add_day(day)
        elif choice == "3":
            day_id = int(input("Enter day id: "))
            farm_id = int(input("Enter farm id: "))
            db.link(day_id, farm_id)
        elif choice == "4":
            details = db.details()
            for detail in details:
                print(f"On {detail[4]}, {detail[2]} {detail[1]} were collected.")
        elif choice == "5":
            farm_id = int(input("Enter farm_id to DELETE : "))
            db.delete_product(farm_id)
        else:
            print("Invalid option")

# Execute main function
if __name__ == "__main__":
    main()


