import tkinter as tk
import sqlite3
from tkinter import font

class ToDoList:
    def __init__(self):
        self.conn = sqlite3.connect("To_do_list_db")
        self.cursor = self.conn.cursor()
        self.db()
        self.window = tk.Tk()
        self.window.title('To-do-list')
        self.window.geometry("350x400")
        tk.Label(self.window, text="Check your to-do-list and complete the assigments!").pack()
        tk.Button(self.window, text="Add an assignment", command=self.add_assignment).pack()
        self.cursor.execute("SELECT id, assignment FROM tasks ORDER BY id")
        self.tasks = self.cursor.fetchall()
        for task in self.tasks:
            self.task_frameall = tk.Frame(self.window)
            self.task_frameall.pack()
            task_name = task
            variavel_check = tk.BooleanVar()
            check = tk.Checkbutton(self.task_frameall, variable=variavel_check).pack(side=tk.LEFT)
            self.assignment_label = tk.Label(self.task_frameall, text=f"{task_name}").pack(side=tk.RIGHT) 
        self.conn.commit()
        self.window.mainloop()

    def db(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assignment TEXT NOT NULL
        )''')
        self.conn.commit()

    def add_assignment(self):
        self.assignment_entry= tk.Entry(self.window)
        self.assignment_entry.pack()
        self.confirmbtn = tk.Button(self.window, text="Confirm", command=self.new_assignment)
        self.confirmbtn.pack()

    def new_assignment(self):
        task_frame = tk.Frame(self.window)
        task_frame.pack()
        self.assignment = self.assignment_entry.get()
        self.assignment_entry.pack_forget() 
        self.confirmbtn.pack_forget()
        self.cursor.execute(f"INSERT INTO tasks (assignment) VALUES (?)", (self.assignment,))
        self.cursor.execute("SELECT id, assignment FROM tasks ORDER BY id DESC LIMIT 1")
        task = self.cursor.fetchone()
        self.conn.commit()
        if task:
            task_name= task
            text = f"{task_name}"
        assignment_label = tk.Label(task_frame, text=f"{text}").pack(side=tk.RIGHT)
        variavel_check = tk.BooleanVar()
        check = tk.Checkbutton(task_frame, variable=variavel_check).pack(side=tk.LEFT)

if __name__ == "__main__":
     ToDoList()


    
