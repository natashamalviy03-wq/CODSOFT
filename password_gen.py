import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

class Passgen:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Generator")
        self.master.geometry("400x500")
        self.master.configure(bg="#1B262C")  # Dark navy background

        # Notebook
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Generator Frame
        self.generator_frame = tk.Frame(self.notebook, bg="#0F4C75")  # Deep blue frame
        self.notebook.add(self.generator_frame, text="Generator")

        self.setup_generator()

    def setup_generator(self):
        # Variables
        self.length_var = tk.StringVar(value="12")
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.number_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=False)
        self.password_var = tk.StringVar()

        # Title
        tk.Label(self.generator_frame, text="Password Generator", 
                 font=("Arial", 16, "bold"), bg="#0F4C75", fg="#BBE1FA").pack(pady=15)

        # Password Length
        tk.Label(self.generator_frame, text="Password Length", 
                 bg="#0F4C75", fg="#BBE1FA", font=("Arial", 12)).pack(pady=5)
        tk.Entry(self.generator_frame, textvariable=self.length_var, width=5, 
                 bg="#3282B8", fg="white", insertbackground="white", font=("Arial", 12)).pack(pady=5)

        # Checkbuttons
        tk.Checkbutton(self.generator_frame, text="Uppercase", variable=self.uppercase_var, 
                       bg="#0F4C75", fg="#BBE1FA", selectcolor="#3282B8").pack(pady=3)
        tk.Checkbutton(self.generator_frame, text="Lowercase", variable=self.lowercase_var, 
                       bg="#0F4C75", fg="#BBE1FA", selectcolor="#3282B8").pack(pady=3)
        tk.Checkbutton(self.generator_frame, text="Numbers", variable=self.number_var, 
                       bg="#0F4C75", fg="#BBE1FA", selectcolor="#3282B8").pack(pady=3)
        tk.Checkbutton(self.generator_frame, text="Symbols", variable=self.symbols_var, 
                       bg="#0F4C75", fg="#BBE1FA", selectcolor="#3282B8").pack(pady=3)

        # Buttons
        ttk.Style().configure("TButton", font=("Arial", 12, "bold"), padding=6)
        tk.Button(self.generator_frame, text="Generate Password", bg="#2EA338", fg="white", 
                  font=("Arial", 12, "bold"), command=self.generator_password).pack(pady=15)
        
        # Password Entry
        ttk.Entry(self.generator_frame, textvariable=self.password_var, width=30, 
                  font=("Arial", 12), state="readonly").pack(pady=5)
        
        tk.Button(self.generator_frame, text="Copy to Clipboard", bg="#5840C5", fg="white", 
                  font=("Arial", 12, "bold"), command=self.copy_to_clipboard).pack(pady=10)

    #generate
    def generator_password(self):
        length = int(self.length_var.get())
        character = ""
        if self.uppercase_var.get():
            character += string.ascii_uppercase
        if self.lowercase_var.get():
            character += string.ascii_lowercase
        if self.number_var.get():
            character += string.digits
        if self.symbols_var.get():
            character += string.punctuation

        if not character:
            self.password_var.set("Select at least one character type")
        else:
            password = ''.join(random.choice(character) for i in range(length))
            self.password_var.set(password)

    #copy
    def copy_to_clipboard(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.password_var.get())
        self.master.update()


if __name__ == "__main__":
    root = tk.Tk()
    app = Passgen(root)
    root.mainloop()
