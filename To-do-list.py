import tkinter as tk

class ToDoList:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('To-do-list')
        self.window.geometry("350x400")
        tk.Label(self.window, text="Check your to-do-list and complete the assigments!").pack()
        tk.Button(self.window, text="Add an assigment", command=self.add_assignment).pack()
        self.window.mainloop()

    def add_assignment(self):
        self.assignment_entry= tk.Entry(self.window)
        self.assignment_entry.pack()
        self.confirmbtn = tk.Button(self.window, text="Confirm", command=self.new_assignment)
        self.confirmbtn.pack()

    def new_assignment(self):
        task_frame = tk.Frame(self.window)
        task_frame.pack()
        assignment = self.assignment_entry.get()
        self.assignment_entry.pack_forget() 
        self.confirmbtn.pack_forget()   
        tk.Label(task_frame, text=f"{assignment}").pack(side=tk.RIGHT)
        variavel_check = tk.BooleanVar()
        check=tk.Checkbutton(task_frame, variable=variavel_check).pack(side=tk.LEFT)

if __name__ == "__main__":
     ToDoList()


    
