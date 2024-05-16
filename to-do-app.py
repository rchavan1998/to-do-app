import psycopg2
from psycopg2 import sql


def to_do_app():
        print("Select an option from 1-4:")
        print("1. Add a task")
        print("2. Delete a task")
        print("3. View all tasks")
        print("4. Update a task")
        print("5. Exit to main menu")



if __name__ == "__main__":
    try:
        to_do_app()
    finally:
        print('abc')