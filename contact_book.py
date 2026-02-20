from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import json
import os

FILE_NAME = "contacts.json"
contact = {}


def load_contacts():
    global contact
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file: 
            contact = json.load(file)
    else:
        contact = {}

def save_contacts():
    with open(FILE_NAME, "w") as file:
        json.dump(contact, file, indent=4)

def open_add_window():
    add_win = Toplevel(win)
    add_win.title("Add New Contact")
    add_win.geometry("400x350")
    add_win.resizable(False, False)

    Label(add_win, text="Add New Contact",
          font=("Arial", 16, "bold")).pack(pady=10)

    Label(add_win, text="Name").pack()
    name_entry = Entry(add_win, width=30)
    name_entry.pack(pady=5)

    Label(add_win, text="Phone").pack()
    phone_entry = Entry(add_win, width=30)
    phone_entry.pack(pady=5)

    Label(add_win, text="Email").pack()
    email_entry = Entry(add_win, width=30)
    email_entry.pack(pady=5)

    Label(add_win, text="Address").pack()
    address_entry = Entry(add_win, width=30)
    address_entry.pack(pady=5)

    def save_contact():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        address = address_entry.get().strip()

        if not name or not phone:
            messagebox.showwarning("Error",
                                   "Name and Phone are required")
            return

        if not phone.isdigit() or len(phone) < 10:
            messagebox.showwarning("Error",
                                   "Phone must contain only digits")
            return

        contact[name] = {
            "phone": phone,
            "email": email,
            "address": address
        }

        save_contacts()  
        update_listbox()

        messagebox.showinfo("Success",
                            "Contact Added Successfully")
        add_win.destroy()

    Button(add_win, text="Save Contact",
           bg="#0b4485", fg="white",
           width=20,
           command=save_contact).pack(pady=15)

#update

def open_update_window():
    selected = listbox.selection()

    if not selected:
        messagebox.showwarning("Warning",
                               "Select a contact to update")
        return

    item = listbox.item(selected)
    old_name = item["values"][0]

    update_win = Toplevel(win)
    update_win.title("Update Contact")
    update_win.geometry("400x350")
    update_win.resizable(False, False)

    Label(update_win, text="Update Contact",
          font=("Arial", 16, "bold")).pack(pady=10)

    Label(update_win, text="Name").pack()
    name_entry = Entry(update_win, width=30)
    name_entry.pack(pady=5)

    Label(update_win, text="Phone").pack()
    phone_entry = Entry(update_win, width=30)
    phone_entry.pack(pady=5)

    Label(update_win, text="Email").pack()
    email_entry = Entry(update_win, width=30)
    email_entry.pack(pady=5)

    Label(update_win, text="Address").pack()
    address_entry = Entry(update_win, width=30)
    address_entry.pack(pady=5)

    name_entry.insert(0, old_name)
    phone_entry.insert(0, contact[old_name]["phone"])
    email_entry.insert(0, contact[old_name]["email"])
    address_entry.insert(0, contact[old_name]["address"])

    def save_updated():
        new_name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        address = address_entry.get().strip()

        if not new_name or not phone:
            messagebox.showwarning("Error",
                                   "Name and Phone are required")
            return

        if not phone.isdigit():
            messagebox.showwarning("Error",
                                   "Phone must contain only digits")
            return

        
        del contact[old_name]

       
        contact[new_name] = {
            "phone": phone,
            "email": email,
            "address": address
        }

        save_contacts()  
        update_listbox()

        messagebox.showinfo("Success",
                            "Contact Updated Successfully")
        update_win.destroy()

    Button(update_win, text="Save Changes",
           bg="#0b4485", fg="white",
           width=20,
           command=save_updated).pack(pady=15)



def update_listbox():
    for item in listbox.get_children():
        listbox.delete(item)

    for name, info in contact.items():
        listbox.insert("", "end",
                       values=(name,
                               info["phone"],
                               info["email"],
                               info["address"]))

def delete_contact():
    selected = listbox.selection()

    if not selected:
        messagebox.showwarning("Warning",
                               "Select a contact to delete")
        return

    item = listbox.item(selected)
    name = item["values"][0]

    del contact[name]
    save_contacts()   
    update_listbox()

    messagebox.showinfo("Deleted",
                        "Contact Deleted Successfully")

def search_contact():
    search_term = entry_search.get().lower().strip()

    if not search_term:
        messagebox.showwarning("Warning",
                               "Enter name or phone to search")
        return

    for item in listbox.get_children():
        listbox.delete(item)

    found = False

    for name, info in contact.items():
        values = (name, info["phone"],
                  info["email"], info["address"])

        if search_term in name.lower() or search_term in info["phone"]:
            listbox.insert("", "end",
                           values=values,
                           tags=("found",))
            found = True

    listbox.tag_configure("found", background="lightgreen")

    if not found:
        messagebox.showwarning("Not Found",
                               "Contact not found")



win = Tk()
win.title("Contact Book")
win.geometry("700x600")
win.resizable(False, False)

load_contacts()  

Label(win, text="Contact Book 📱",
      font=("Arial", 22, "bold")).pack(pady=10)

# Search
Label(win, text="Search by Name or Phone").pack(pady=5)
entry_search = Entry(win, width=30)
entry_search.pack()

Button(win, text="Search",
       width=20,
       bg="#0b4485", fg="white",
       command=search_contact).pack(pady=10)

# Treeview
columns = ("name", "phone", "email", "address")
listbox = ttk.Treeview(win,
                       columns=columns,
                       show="headings")

for col in columns:
    listbox.heading(col, text=col.capitalize())
    listbox.column(col, width=160)

listbox.pack(pady=20)

update_listbox()  

# Buttons
Button(win, text="Add Contact",
       width=25,
       bg="#0b4485", fg="white",
       command=open_add_window).pack(pady=5)

Button(win, text="Update Contact",
       width=25,
       bg="#0b4485", fg="white",
       command=open_update_window).pack(pady=5)

Button(win, text="Delete Contact",
       width=25,
       bg="#0b4485", fg="white",
       command=delete_contact).pack(pady=5)

win.mainloop()
