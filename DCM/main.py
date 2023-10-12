import tkinter as tk
from tkinter import messagebox

import user as u

# Find User in Accounts and Return Password
def FindUser(username):
    for person in users.accounts:
        if person.name == username:
            return person.password
            
    return ""

# Function to check if the entered username and password are correct
def login():
    username = entry_username.get()
    password = entry_password.get()

    if FindUser(username) == password:
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password")

# Function to handle the signup process
def signup():
    username = entry_username.get()
    password = entry_password.get()
    
    # Add account to the object if it does not already exist
    if (FindUser(username) == ""):
        
        # Only Allow 10 users to be stored locally
        if users.length < 10:
            users.add_user(username, password)
            messagebox.showinfo("Signup Successful", "Account created for " + username + "!")
        else:
            messagebox.showerror("Signup Failed", "Max of 10 Users Reached")

    else:
        messagebox.showerror("Signup Failed", "Username Exits Already, Did you mean to Log in?")


# Create an Accounts object
users = u.Accounts()


# Create the main window
window = tk.Tk()
window.title("Login/Signup Screen")

# Set the starting size of the window (width x height)
window.geometry("500x300")  # Adjust the dimensions as needed

# Create a frame to hold the login and signup components
frame = tk.Frame(window)
frame.pack(expand=True, fill="both", pady=50)  # Center vertically with padding

# Username Field
label_username = tk.Label(frame, text="Username:")
label_username.pack()
entry_username = tk.Entry(frame)
entry_username.pack()

# Password Field
label_password = tk.Label(frame, text="Password:")
label_password.pack()
entry_password = tk.Entry(frame, show="*")  # The 'show' option hides the password
entry_password.pack()

# Create a login button
login_button = tk.Button(frame, text="Login", command=login)
login_button.pack()

# Create a signup button
signup_button = tk.Button(frame, text="Signup", command=signup)
signup_button.pack()

# Start the Tkinter main loop
window.mainloop()
