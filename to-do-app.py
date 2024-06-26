import psycopg2
from psycopg2 import sql
from datetime import datetime


#postgres init 
pg_conn_str = psycopg2.connect("dbname=to-do-app user=postgres password=postgres")
pg_cursor = pg_conn_str.cursor()


#view all tasks
def view_all_tasks():
    pg_cursor.execute("select id, task_name, due_date from tasks order by due_date asc")
    all_tasks_list = pg_cursor.fetchall()
    for row in all_tasks_list:
        print(f"{row[0]}: {row[1]} - due by {row[2]}")

def add_new_task(task, due_date):
    if due_date == '':
        due_date = 'not added'  
    if due_date == 'not added':
        due_date = datetime.now()
    pg_cursor.execute(
        "insert into tasks (task_name, due_date) values (%s, %s)",
        (task, due_date)
    )
    pg_conn_str.commit()
    print("Task added successfully !")

#drop task basis task_id
def drop_task(task_id):
    pg_cursor.execute(
        "delete FROM tasks where id = %s",
        (task_id,)
    )
    pg_conn_str.commit()
    print("Task deleted!")

#update
def update_task(task_id, new_task=None, new_due_date=None):

    pg_cursor.execute("select count(*) from tasks where id = %s", (task_id,))
    if pg_cursor.fetchone()[0] == 0:
        print(f"No task found with ID {task_id}. Please enter a valid task ID.")
        return
    variables = []
    params = []
    if new_task:
        variables.append("task_name = %s")
        params.append(new_task)
    if new_due_date:
        variables.append("due_date = %s")
        params.append(new_due_date)
    params.append(task_id)

    if variables:
        update_query = "update tasks set " + ", ".join(variables) + " where id = %s"
        pg_cursor.execute(update_query, tuple(params))
        pg_conn_str.commit()
        print(f"Task with ID: {task_id} updated successfully!")
    else:
        print("No updates provided.")

#MAIN FUNCTION
def to_do_app():
    while True:
        print("Select an option from 1-4:")
        print("1. Add a task")
        print("2. Delete a task")
        print("3. View all tasks")
        print("4. Update a task")
        print("5. Exit ")
        user_input = input("Enter your choice : ")

        if user_input == '1' :
            task = input("Enter task details: ")
            due_date = input("Enter due date (timestamp without timezone) (YYYY-MM-DD HH:MM:SS), or leave blank for current timestamp: ")
            if due_date:
                due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S")
            add_new_task(task, due_date)


        elif user_input == '2' :
            task_id = int(input("Enter task ID to drop: "))
            drop_task(task_id)


        elif user_input == '3':
             view_all_tasks()

        elif user_input == '4' :

            task_id = int(input("Enter task ID to update: "))
            new_task = input("Enter new task details or leave blank: ")
            new_due_date = input("Enter new due date (YYYY-MM-DD HH:MM:SS), or leave blank: ")

            if new_due_date:
                new_due_date = datetime.strptime(new_due_date, "%Y-%m-%d %H:%M:%S")
            update_task(task_id, new_task, new_due_date)

        elif user_input == '5':
            print("Exiting ! ")
            break
        else:
             print ("Enter only integer input between 1-4. Try again")


if __name__ == "__main__":
    try:
        to_do_app()
    finally:
        pg_cursor.close()
        pg_conn_str.close()
