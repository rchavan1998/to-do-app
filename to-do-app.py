import psycopg2
from psycopg2 import sql


#postgres init 
pg_conn_str = psycopg2.connect("dbname=to-do-app user=postgres password=postgres")
pg_cursor = pg_conn_str.cursor()


#view all tasks
def view_all_tasks():
    pg_cursor.execute("select id, task_name, due_date FROM tasks ORDER BY due_date ASC")
    all_tasks_list = pg_cursor.fetchall()
    for row in all_tasks_list:
        print(f"{row[0]}: {row[1]} - due by {row[2]}")



#MAIN FUNCTION
def to_do_app():
        print("Select an option from 1-4:")
        # print("1. Add a task")
        # print("2. Delete a task")
        print("3. View all tasks")
        # print("4. Update a task")
        # print("5. Exit to main menu")
        user_input = input("Enter your choice : ")

        if user_input == '3':
             view_all_tasks()
        else:
             print ("Enter only integer input. Try again")


if __name__ == "__main__":
    try:
        to_do_app()
    finally:
        pg_cursor.close()
        pg_conn_str.close()
