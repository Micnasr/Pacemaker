from tkinter import messagebox

# Find User in Accounts and Return Password
def find_user(users, username):
    for person in users.accounts:
        if person.name == username:
            return person.password

    # User not Found
    return -1

# Function to check if the entered username and password are correct
def login(users, username, password):
    if find_user(users, username) == password:
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        return 1
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password")
        return 0

# Function to handle the signup process
def signup(users, username, password):
    # Only allow signup if the username is NOT used
    if (find_user(users, username) == -1):
        # Only allow 10 users max
        if users.length < 10:
            # Make sure the input is valid
            if password == "" or username == "":
                messagebox.showerror("Signup Failed", "Empty Field")
            else:
                users.add_user(username, password)
                messagebox.showinfo("Signup Successful", "Account created for " + username + "!")
        else:
            messagebox.showerror("Signup Failed", "Max of 10 Users Reached")
    else:
        messagebox.showerror("Signup Failed", "Username Exists Already, Did you mean to Log in?")
