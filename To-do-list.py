import tkinter as tk
import sqlite3

class ToDoList:
    def __init__(self):
        # Initialize the main window
        self.window = tk.Tk()
        self.window.title('To-do-list')
        self.window.geometry("350x400")
        
        # Create header label
        tk.Label(self.window, text="Check your to-do-list and complete the assigments!").pack()
        
        # Create button to add new assignments
        tk.Button(self.window, text="Add an assignment", command=self.add_assignment).pack()
        self.assignment_label = tk.Label()
        
        # Initialize database connection and load existing tasks
        self.db()
        
        # Start the GUI main loop
        self.window.mainloop()

    def db(self):
        # Establish database connection
        self.conn = sqlite3.connect("To_do_list_db")
        self.cursor = self.conn.cursor()
        
        # Create tasks table if it doesn't exist
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assignment TEXT NOT NULL
        )''')
        
        # Fetch all existing tasks from database
        self.cursor.execute("SELECT id, assignment FROM tasks ORDER BY id")
        self.tasks = self.cursor.fetchall()
        
        # Display each existing task with a checkbox
        for task in self.tasks:
            task_id = task[0]  # Get the ID
            task_name = task[1]  # Get the assignment text
            self.task_frameall = tk.Frame(self.window)
            self.task_frameall.pack()
            check = tk.Checkbutton(self.task_frameall).pack(side=tk.LEFT)
            self.assignment_label = tk.Label(self.task_frameall, text=f"{task_name}").pack(side=tk.LEFT) 
            delete_btn = tk.Button(self.task_frameall, text="Delete", command=lambda tid=task_id: self.deleteassignment(tid)).pack(side=tk.RIGHT)
        
        # Commit any changes to database
        self.conn.commit()

    def add_assignment(self):
        # Create entry field for new assignment text
        self.assignment_entry = tk.Entry(self.window)
        self.assignment_entry.pack()
        
        # Create confirm button to save the new assignment
        self.confirmbtn = tk.Button(self.window, text="Confirm", command=self.new_assignment)
        self.confirmbtn.pack()

    def new_assignment(self):
        # Create frame for the new task
        task_frame = tk.Frame(self.window)
        task_frame.pack()

        # Get the assignment text from entry field
        self.assignment = self.assignment_entry.get()
        
        # Remove entry field and confirm button after capturing text
        self.assignment_entry.pack_forget() 
        self.confirmbtn.pack_forget()
        
        # Insert new assignment into database
        self.cursor.execute(f"INSERT INTO tasks (assignment) VALUES (?)", (self.assignment,))
        
        # Fetch the newly inserted task to display it
        self.cursor.execute("SELECT id, assignment FROM tasks ORDER BY id DESC LIMIT 1")
        task = self.cursor.fetchone()
        self.conn.commit()
        
        # Display the new task with a checkbox
        if task:
            task_id = task[0]  # Get the ID
            task_name = task[1]  # Get the assignment text
        check = tk.Checkbutton(task_frame).pack(side=tk.LEFT)
        assignment_label = tk.Label(task_frame, text=f"{task_name}").pack(side=tk.LEFT)
        delete_btn = tk.Button(task_frame, text="Delete", command=lambda tid=task_id: self.deleteassignment(tid)).pack(side=tk.RIGHT)

    def deleteassignment(self, task_id):
        # Delete the specific task by ID
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        
        # Refresh the window to show updated list
        self.refresh_tasks()

    def refresh_tasks(self):
        # Clear all existing task frames
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()
        
        # Reload tasks from database
        self.cursor.execute("SELECT id, assignment FROM tasks ORDER BY id")
        self.tasks = self.cursor.fetchall()
        
        for task in self.tasks:
            task_id = task[0]
            task_name = task[1]
            
            self.task_frameall = tk.Frame(self.window).pack()
            
            check = tk.Checkbutton(self.task_frameall).pack(side=tk.LEFT)
            
            self.assignment_label = tk.Label(self.task_frameall, text=f"{task_name}").pack(side=tk.LEFT)

            delete_btn = tk.Button(self.task_frameall, text="Delete", command=lambda tid=task_id: self.deleteassignment(tid)).pack(side=tk.RIGHT)
            

if __name__ == "__main__":
    # Run the application
    ToDoList()