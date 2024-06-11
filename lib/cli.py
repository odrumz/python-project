
import sqlite3
from helpers import (
    exit_program,
    helper_1
)

def create_tables():
    conn = sqlite3.connect("farmdb")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXIST products'''
                )
 


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            helper_1()
        else:
            print("Invalid option")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Some useful function")


if __name__ == "__main__":
    main()
