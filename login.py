import hashlib 
import tkinter as tk
from tkinter import messagebox
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_exist_user(username):
    try:
        with open("account.txt", "r") as f:
            for line in f:
                stored_username = line.strip().split(",")[0]
                if stored_username == username:
                    return True
    except FileNotFoundError:
        pass
    return False

def validation(username, password):
    if not username or not password:
        messagebox.showerror("Error", "Username or password cannot be empty.")
        return False
    return True

def store_acc(username, password):
    hashed_password = hash_password(password)
    with open("account.txt", "a") as f:
        f.write(f"{username},{hashed_password}\n")


def register():

    username = entry_username.get()
    if check_exist_user(username):
        messagebox.showerror("Error", "Account already exists.")
        return

    password = entry_password.get()
    if not validation(username, password):
        return
    store_acc(username, password)
    messagebox.showinfo("Success", "Account created successfully.")

def login():
    username = entry_username.get()
    password = entry_password.get()
    hashed_password = hash_password(password)

    try:
        with open("account.txt", "r") as f:
            for line in f:
                stored_username, stored_password = line.strip().split(",")
                if stored_username == username and stored_password == hashed_password:
                    messagebox.showinfo("Success", "Login successful.")
                    return True
    except FileNotFoundError:
        pass

    messagebox.showerror("Error", "Invalid username or password.")
    return False

root = tk.Tk()
root.title("Login/Register")
tk.Label(root,text="username").grid(row=0, column=0, padx=10, pady=10)
tk.Label(root,text="password").grid(row=1, column=0, padx=10, pady=10)

entry_username = tk.Entry(root)
entry_password = tk.Entry(root, show="*")

entry_username.grid(row=0, column=1, padx=10, pady=10)
entry_password.grid(row=1, column=1, padx=10, pady=10)

button = tk.Button(root, text="register", width=25, command=register)
button.grid(row=2, column=0, columnspan=2, pady=10)
button = tk.Button(root, text="login", width=25, command=login)
button.grid(row=3, column=0, columnspan=2, pady=10)
root.mainloop()