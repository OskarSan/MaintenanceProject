from tkinter import *
from tkinter import messagebox
import sqlite3


class LoginWindow:
    def __init__(self, root, parent=None):
        self.root = root
        self.parent = parent
        self.root.title("Login")
        self.root.geometry("400x300")
        Label(root, text="Email").pack()
        self.email_entry = Entry(root)
        self.email_entry.pack()
        Label(root, text="Password").pack()
        self.pass_entry = Entry(root, show="*")
        self.pass_entry.pack()
        Button(root, text="Login", command=self.login).pack()
        self.user_role = None
        # Make modal if parent is given
        if self.parent:
            self.root.transient(self.parent)

    def login(self):
        email = self.email_entry.get()
        password = self.pass_entry.get()
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("SELECT utype FROM employee WHERE email=? AND pass=?", (email, password))
        result = cur.fetchone()
        con.close()
        if result:
            self.user_role = result[0]
            self.root.destroy()  # Close login window
        else:
            messagebox.showerror("Error", "Invalid credentials")
