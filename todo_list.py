import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json

class ModernTodos:
    def __init__(self, master):
        self.master = master
        self.master.title("Modern To-Do List")
        self.master.geometry("500x550")
        self.master.configure(bg="#2E3440") 

        #style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#2E3440")
        style.configure("TButton", padding=5, font=('Helvetica', 10), foreground="white")
        style.configure("TEntry", padding=5, font=('Helvetica', 10))
        style.configure("Treeview", font=('Helvetica', 10), rowheight=28, background="#ECEFF4", foreground="#2E3440",
                        fieldbackground="#ECEFF4")
        style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'), background="#4C566A", foreground="white")

        #mainframe
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Task Entry
        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(self.frame, textvariable=self.task_var, width=30)
        self.task_entry.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

        self.add_button = tk.Button(self.frame, text="Add Task", bg="#5E81AC", fg="white", font=("Helvetica", 10, "bold"),
                                    command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=5, pady=10)

        #treeview
        self.task_tree = ttk.Treeview(self.frame, columns=("task", "status"), show="headings", height=15,
                                      selectmode="browse")
        self.task_tree.heading("task", text="Task")
        self.task_tree.heading("status", text="Status")
        self.task_tree.column("task", width=300)
        self.task_tree.column("status", width=100)
        self.task_tree.grid(row=1, columnspan=3, padx=5, pady=10, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        scrollbar.grid(row=1, column=3, sticky='ns')
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        # Bind click for toggle select
        self.task_tree.bind("<Button-1>", self.toggle_selection)

        #butons
        self.delete_button = tk.Button(self.frame, text="Delete Task", bg="#E63946", fg="white",
                                       font=("Helvetica", 10, "bold"), command=self.delete_task)
        self.delete_button.grid(row=2, column=0, ipadx=5, ipady=8, padx=5, pady=10, sticky='ew')

        self.update_button = tk.Button(self.frame, text="Update Task", bg="#FF8C42", fg="white",
                                       font=("Helvetica", 10, "bold"), command=self.update_task)
        self.update_button.grid(row=2, column=1, ipadx=5, ipady=8, padx=5, pady=10, sticky='ew')

        self.complete_button = tk.Button(self.frame, text="Mark Complete", bg="#38B000", fg="white",
                                         font=("Helvetica", 10, "bold"), command=self.mark_complete)
        self.complete_button.grid(row=2, column=2, ipadx=5, ipady=8, padx=5, pady=10, sticky='ew')

        self.save_button = tk.Button(self.frame, text="Save Tasks", bg="#00B4D8", fg="white",
                                     font=("Helvetica", 10, "bold"), command=self.save_task)
        self.save_button.grid(row=3, column=0, columnspan=3, ipadx=5, ipady=8, padx=5, pady=10, sticky='ew')

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        #COLORS
        self.task_tree.tag_configure('Pending', background='#F0E68C')   
        self.task_tree.tag_configure('Completed', background='#98FB98') 

        #load
        self.load_task()

    #add
    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            self.task_tree.insert("", tk.END, values=(task, "Pending"), tags=("Pending",))
            self.task_var.set("")
        else:
            messagebox.showwarning("Warning", "Please Enter a Task")

    #delete
    def delete_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            self.task_tree.delete(selected_item)
        else:
            messagebox.showwarning("Warning", "Please select a task")

    #update
    def update_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Select task to update")
            return

        old_task = self.task_tree.item(selected_item)["values"][0]
        new_task = simpledialog.askstring("Update Task", "Edit your task:", initialvalue=old_task)

        if new_task:
            status = self.task_tree.item(selected_item)["values"][1]
            self.task_tree.item(selected_item, values=(new_task, status), tags=(status,))

    #completed
    def mark_complete(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Select task to mark complete")
            return

        task = self.task_tree.item(selected_item)["values"][0]
        self.task_tree.item(selected_item, values=(task, "Completed"), tags=("Completed",))

    #save
    def save_task(self):
        tasks = []
        for child in self.task_tree.get_children():
            task_data = self.task_tree.item(child)["values"]
            tasks.append({"task": task_data[0], "status": task_data[1]})
        with open("tasks.json", "w") as f:
            json.dump(tasks, f, indent=4)
        messagebox.showinfo("Success", "Tasks Saved!")

    #load
    def load_task(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                tasks = json.load(f)
                for t in tasks:
                    if isinstance(t, dict):
                        task_text = t.get("task", "")
                        status = t.get("status", "Pending")
                    else:
                        task_text = t
                        status = "Pending"
                    self.task_tree.insert('', tk.END, values=(task_text, status), tags=(status,))

    #toggle
    def toggle_selection(self, event):
        region = self.task_tree.identify("region", event.x, event.y)
        if region == "heading":
            return
        iid = self.task_tree.identify_row(event.y)
        if not iid:
            return
        if iid in self.task_tree.selection():
            self.task_tree.selection_remove(iid)
        else:
            self.task_tree.selection_set(iid)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTodos(root)
    root.mainloop()

