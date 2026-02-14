import os
import tkinter as tk
from tkinter import ttk, messagebox
import json

class ModernTodos:
    def __init__(self, master):
        self.master = master
        self.master.title("Modern To-Do List")
        self.master.geometry("400x500")
        self.master.configure(bg="#f0f0f0")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", padding=10, font=('Helvetica', 10))
        style.configure("TEntry", padding=10, font=('Helvetica', 10))
        style.configure("Treeview", font=('Helvetica', 10), rowheight=25)
        style.configure("Tview.heading", font=('Helvetica', 11, 'bold'))
        
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(self.frame, textvariable=self.task_var, width=30)
        
        self.task_entry.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        
        self.add_button = ttk.Button(self.frame, text="Add Task", command=self.add_task) 
        self.add_button.grid(row=0, column=1, padx=5, pady=10)
        
        self.task_tree = ttk.Treeview(self.frame, columns=("task",), show="headings", height=15)
        self.task_tree.heading("task", text="Tasks")
        self.task_tree.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        scrollbar.grid(row=1, column=2, sticky='ns')
        
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        self.delete_button = ttk.Button(self.frame, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, padx=5, pady=10, sticky='ew')
        
        self.save_button = ttk.Button(self.frame, text="Save Task", command=self.save_task)
        self.save_button.grid(row=2, column=1, padx=5, pady=10, sticky='ew')
        
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        
        self.load_task()
        
    def add_task(self):
        task = self.task_var.get()
        if task:
            self.task_tree.insert("", tk.END, values=(task,))
            self.task_var.set("")
        else:
            messagebox.showwarning("Warning", "Please Enter a Task")
                
    def delete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            for item in selected_item:
                self.task_tree.delete(item)
        else:
            messagebox.showwarning("Warning", "Please select a task to delete")
                
    def save_task(self):
        # Line 59 Fix: Correct indentation
        tasks = [self.task_tree.item(child)['values'][0] for child in self.task_tree.get_children()]
        with open("tasks.json", "w") as f:
            json.dump(tasks, f)
        messagebox.showinfo("Success", "Tasks saved!")
            
    def load_task(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
                for t in tasks:
                    self.task_tree.insert('', tk.END, values=(t,))


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTodos(root)
    root.mainloop()
