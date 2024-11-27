import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

def create_connection():
    if not os.path.exists('passwords.db'):
        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS passwords
                     (username TEXT, password TEXT)''')
        conn.commit()
    else:
        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
    return conn, c

def add(c, conn):
    username = entryName.get()
    password = entryPassword.get()
    if username and password:
        c.execute("INSERT INTO passwords VALUES (?,?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Password added!!")
    else:
        messagebox.showerror("Error", "Please enter both the fields")

def get(c):
    username = entryName.get()
    c.execute("SELECT password FROM passwords WHERE username=?", (username,))
    row = c.fetchone()
    if row:
        messagebox.showinfo("Password", f"Password for {username} is {row[0]}")
    else:
        messagebox.showinfo("Password", "No Such Username Exists!!")

def getlist(c):
    c.execute("SELECT * FROM passwords")
    rows = c.fetchall()
    if rows:
        mess = "List of passwords:\n"
        for row in rows:
            mess += f"Password for {row[0]} is {row[1]}\n"
        messagebox.showinfo("Passwords", mess)
    else:
        messagebox.showinfo("Passwords", "Empty List!!")

def delete(c, conn):
    username = entryName.get()
    try:
        c.execute("DELETE FROM passwords WHERE username=?", (username,))
        conn.commit()
        messagebox.showinfo("Success", "Password deleted!!")
    except sqlite3.OperationalError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    conn, c = create_connection()

    root = tk.Tk()
    root.title("Password Manager")
    root.configure(background='#f0f0f0')  # Set the background color of the root window

    labelName = tk.Label(root, text="Username:", bg='#f0f0f0', fg='#00698f')  # Set the background and foreground colors of the label
    labelName.pack()
    entryName = tk.Entry(root, width=30, bg='#ffffff', fg='#000000')  # Set the background and foreground colors of the entry
    entryName.pack()

    labelPassword = tk.Label(root, text="Password:", bg='#f0f0f0', fg='#00698f')  # Set the background and foreground colors of the label
    labelPassword.pack()
    entryPassword = tk.Entry(root, width=30, show="*", bg='#ffffff', fg='#000000')  # Set the background and foreground colors of the entry
    entryPassword.pack()

    buttonAdd = tk.Button(root, text="Add", command=lambda: add(c, conn), bg='#007bff', fg='#ffffff')  # Set the background and foreground colors of the button
    buttonAdd.pack()

    buttonGet = tk.Button(root, text="Get", command=lambda: get(c), bg='#007bff', fg='#ffffff')  # Set the background and foreground colors of the button
    buttonGet.pack()

    buttonGetList = tk.Button(root, text="Get List", command=lambda: getlist(c), bg='#007bff', fg='#ffffff')  # Set the background and foreground colors of the button
    buttonGetList.pack()

    buttonDelete = tk.Button(root, text="Delete", command=lambda: delete(c, conn), bg='#007bff', fg='#ffffff')  # Set the background and foreground colors of the button
    buttonDelete.pack()

    root.mainloop()