import tkinter as tk
import registration as reg
import user as u

# Import the Enum class for state management
from enum import Enum

# Create an Accounts object
users = u.Accounts()

# Define an enumeration for the different states
class AppState(Enum):
    WELCOME = 1
    TELEMETRY = 2

# Create the main window
window = tk.Tk()
window.title("Pacemaker Welcome")

# Set the starting size of the window (width x height)
window.geometry("600x450")

# Create a frame to hold the components
frame = tk.Frame(window)
frame.pack(expand=True, fill="both", pady=50)

# Function to clear the current frame
def clear_frame():
    for widget in frame.winfo_children():
        widget.pack_forget()

# Function to display the Welcome state
def show_welcome_state():

    def handle_login():
        username = entry_username.get()
        password = entry_password.get()

        # Calls the login function in registration and updates the GUI State
        login_check = reg.login(users, username, password)
        if login_check[0]:
            global current_user
            current_user = login_check[1]
            update_state(AppState.TELEMETRY)

    def handle_signup():
        username = entry_username.get()
        password = entry_password.get()

        reg.signup(users, username, password)

    clear_frame()

    # Create a welcome label
    welcome_label = tk.Label(frame, text="Pacemaker Welcome")
    welcome_label.pack()

    # Create username and password fields
    label_username = tk.Label(frame, text="Username:")
    label_username.pack()
    entry_username = tk.Entry(frame)
    entry_username.pack()

    label_password = tk.Label(frame, text="Password:")
    label_password.pack()
    entry_password = tk.Entry(frame, show="*")
    entry_password.pack()

    # Create a login button
    login_button = tk.Button(frame, text="Login", command=handle_login)
    login_button.pack()

    # Create a signup button
    signup_button = tk.Button(frame, text="Signup", command=handle_signup)
    signup_button.pack()

# Function to display the Telemetry state
def show_telemetry_state():
    clear_frame()

    def update_text():
        for widget in frame2.winfo_children():
            widget.destroy()
        settings = mode_settings[selected.get()]
        for i in range(len(settings)):
            mode_label = tk.Label(frame2, text=params[settings[i]] + ":")
            mode_label.grid(row = i, column = 0, pady = 10)

            value_label = tk.Label(frame2, text=current_user.data[settings[i]])
            value_label.grid(row=i, column=1, pady=10, padx = 5)

            param_entry = tk.Entry(frame2)
            param_entry.grid(row = i, column = 2, padx = 10, pady = 10)
        submit_buttom = tk.Button(frame2, text="Submit Changes")
        submit_buttom.grid(row=i+1, column=2)

    modes = [
        "AOO",
        "VOO",
        "AAI",
        "VVI"    
    ]

    params = ["Lower Rate Limit", "Upper Rate Limit", "Atrial Amplitude", "Atrial Pulse Width", "Ventricular Amplitude", "Ventricular Pulse Width", "VRP", "ARP"]

    mode_settings = {
        "AOO" : [0, 1, 2, 3],
        "VOO" : [0, 1, 4, 5],
        "AAI" : [0, 1, 2, 3, 7],
        "VVI" : [0, 1, 4, 5, 6]
    }

    # Create a telemetry label
    telemetry_label = tk.Label(frame, text="Welcome to Telemetry")
    telemetry_label.pack()

    selected = tk.StringVar(frame)
    selected.set(modes[0])

    dropdown = tk.OptionMenu(frame, selected, *modes)
    dropdown.pack()

    mode_button = tk.Button(frame, text="Select", command=update_text)
    mode_button.pack()

    frame2 = tk.Frame(frame)
    frame2.pack()

    

# Create a StringVar to store the current state (allows 2 way communication between widgets and variables)
current_state = tk.StringVar()
current_state.set(AppState.WELCOME)

# Switch Between States
def update_state(new_state):
    current_state.set(new_state)
    if new_state == AppState.WELCOME:
        show_welcome_state()
    elif new_state == AppState.TELEMETRY:
        show_telemetry_state()

# Call the initial state
show_welcome_state()

# Start the Tkinter main loop
window.mainloop()
