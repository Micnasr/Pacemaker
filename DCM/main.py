import tkinter as tk
from tkinter import messagebox

import registration as reg
import user as u

# Create an Accounts object
users = u.Accounts()


# Create the main window
window = tk.Tk()
window.title("Pacemaker Welcome")  # Change the window title

# Set the starting size of the window (width x height)
window.geometry("500x300")  # Adjust the dimensions as needed

# Create a welcome label at the top of the window
welcome_label = tk.Label(window, text="Pacemaker Welcome")
welcome_label.pack()

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
login_button = tk.Button(frame, text="Login", command=lambda: reg.login(users, entry_username.get(), entry_password.get()))
login_button.pack()

# Create a signup button
signup_button = tk.Button(frame, text="Signup", command=lambda: reg.signup(users, entry_username.get(), entry_password.get()))
signup_button.pack()

# Start the Tkinter main loop
window.mainloop()
