import os
import json
from datetime import datetime


def load_tasks():
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    else:
        tasks = []
    return tasks


def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file)


def add_task(tasks, task_name, priority, due_date):
    if due_date:
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            tasks.append({'task': task_name, 'completed': False, 'priority': priority, 'due_date': due_date.strftime("%Y-%m-%d")})
            save_tasks(tasks)
        except ValueError:
            print("Invalid date format! Please enter in YYYY-MM-DD format!")
    else:
        tasks.append({'task': task_name, 'completed': False, 'priority': priority, 'due_date': "9999-12-31"})
        save_tasks(tasks)


def view_tasks(tasks):
    if not tasks:
        print("No tasks found.")

    priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
    tasks.sort(key=lambda task: (datetime.strptime(task.get('due_date', "9999-12-31"), "%Y-%m-%d"),
                                priority_order.get(task['priority'], 4)))
    
    for i, task in enumerate(tasks):
        status = "Completed" if task['completed'] else "Not completed"
        print(f"{i+1}. {task['task']} - {status} - Priority: {task['priority']} - Due: {task.get('due_date', 'No due date')}")


def complete_task(tasks, task_index):
    if task_index < len(tasks) and task_index >= 0:
        tasks[task_index]['completed'] = True
        save_tasks(tasks)
        print(f"Task '{tasks[task_index]['task']}' marked as completed.")
    else:
        print("Invalid task number.")


def delete_task(tasks, task_index):
    if task_index < len(tasks) and task_index >= 0:
        print(f"Task '{tasks[task_index]['task']}' deleted.")
        del tasks[task_index]
        save_tasks(tasks)
    else:
        print("Invalid task number.")

def edit_task(tasks, task_index, new_task_name):
    if not tasks:
        print("No tasks found.")
        return
    if 0 <= task_index < len(tasks):
        print(f"Task '{tasks[task_index]['task']}' updated to '{new_task_name}'.")
        tasks[task_index]['task'] = new_task_name
        save_tasks(tasks)
    else:
        print("Invalid task number.")

def edit_priority(tasks, task_index, new_priority):
    if 0 <= task_index < len(tasks):
        print(f"Task '{tasks[task_index]['task']}' priority updated to '{new_priority}'.")
        tasks[task_index]['priority'] = new_priority
        save_tasks(tasks)
    else:
        print("Invalid task number.")

def edit_due_date(tasks, task_index, new_due_date):
    try:
        new_due_date = datetime.strptime(new_due_date, "%Y-%m-%d").date()
        tasks[task_index]['due_date'] = new_due_date.strftime("%Y-%m-%d")
        save_tasks(tasks)
        print(f"Task '{tasks[task_index]['task']}' due date updated to '{new_due_date.strftime('%Y-%m-%d')}'.")
    except ValueError:
        print("Invalid date format! Please enter in YYYY-MM-DD format!")

def main():
    tasks = load_tasks()

    while True:
        print("\nTo-Do List:")
        print("1. Add a task")
        print("2. View tasks")
        print("3. Mark task as completed")
        print("4. Delete a task")
        print("5. Edit a task")
        print("6. Edit Task Priority")
        print("7. Edit Task Due Date")
        print("8. Exit")
        
        choice = input("Choose an option: ")

        if choice == "1":
            task_name = input("Enter the task: ")
            priority = input("Enter priority (High, Medium, Low): ").capitalize()
            due_date = input("Enter due date (YYYY-MM-DD) or leave blank for no due date: ").strip()
            if due_date:
                add_task(tasks, task_name, priority, due_date)
            else:
                add_task(tasks, task_name, priority, "9999-12-31")
                
        elif choice == "2":
            view_tasks(tasks)

        elif choice == "3":
            view_tasks(tasks)
            try:
                task_number = int(input("Enter the task number to mark as completed: ")) - 1
                complete_task(tasks, task_number)
            except ValueError:
                print("Invalid input, please enter a valid task number.")

        elif choice == "4":
            view_tasks(tasks)
            try:
                task_number = int(input("Enter the task number to delete: ")) - 1
                delete_task(tasks, task_number)
            except ValueError:
                print("Invalid input, please enter a valid task number.")

        elif choice == "5":
            view_tasks(tasks)
            try:
                task_number = int(input("Enter the task number to edit: ")) - 1
                new_name = input("Enter the new task name: ")
                edit_task(tasks, task_number, new_name)
            except ValueError:
                print("Invalid input, please enter a valid task number.")

        elif choice == "6":
            view_tasks(tasks)
            try:
                task_number = int(input("Enter the task number to edit priority: ")) - 1
                new_priority = input("Enter the new priority (High, Medium, Low): ").capitalize()
                edit_priority(tasks, task_number, new_priority)
            except ValueError:
                print("Invalid input, please enter a valid task number.")

        elif choice == "7":
            view_tasks(tasks)
            try:
                task_number = int(input("Enter the task number to edit due date: ")) - 1
                new_due_date = input("Enter the new due date (YYYY-MM-DD): ").strip()
                edit_due_date(tasks, task_number, new_due_date)
            except ValueError:
                print("Invalid input, please enter a valid task number.")

        elif choice == "8":
            print("Goodbye!")
            
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
