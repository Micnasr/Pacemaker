import tkinter as tk
from tkinter import ttk
import registration as reg
import user as u
import wmi
import io                                           
from contextlib import redirect_stdout                  
import re 

# Import the Enum class for state management
from enum import Enum

# Create an Accounts object
users = u.Accounts()

def grabHardwareID():
    c = wmi.WMI()
    serial_value = -1

    captured_output = io.StringIO()

    with redirect_stdout(captured_output):
        for item in c.Win32_PhysicalMedia():
            print(item)
        for drive in c.Win32_DiskDrive():
            print(drive)
        for disk in c.Win32_LogicalDisk():
            print(disk)

    output_text = captured_output.getvalue()

    pattern = r'\b[0-9A-Fa-f]{8}&\d&\d{12}\b'

    # Search for the pattern using regex
    match = re.search(pattern, output_text)

    if match:
        serial_value = match.group(0)
        users.serial = serial_value
        users.update_device_file()

    if "SEGGER" in output_text:
        return 1, serial_value
    else:
        return 0, serial_value

connected, serial = grabHardwareID()
#Provisional Placeholder for Hardware Connection


#EGRAMS DATA STRUCTURE
#For the egrams data structure, we are planning on using a two dimensional array, where each internal array represents the data after a particular timestep.
#This way, we can sample at a particular timestep and see how the egram data is changing over time


# Define an enumeration for the different states
class AppState(Enum):
    WELCOME = 1
    TELEMETRY = 2
    EGRAM = 3

# Create the main window
window = tk.Tk()

# Set the starting size of the window (width x height)
window.geometry("600x450")

# Create a frame to hold the components
frame = tk.Frame(window)
frame.pack(expand=True, fill="both", pady=50)

# Function to clear the current frame
def clear_frame():
    for widget in frame.winfo_children():
        widget.pack_forget()

# Handle New Hardware / Connection Visuals
def connection_UI():
    connected_label = tk.Label(frame, text="", fg="white")
    connected_label.pack(pady=10)

    #Display whether a device is connected or not 
    if connected:
        if serial == users.old_serial:
            connected_label.config(text=f"Communicating With Device: {serial}", bg="green")
        else:
            connected_label.config(text=f"Communicating With New Device: {serial}", bg="green")
    else:
        connected_label.config(text="Not Communicating With Device", bg = "red")

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
    window.title("Pacemaker Welcome")

    # Create a welcome label
    welcome_label = tk.Label(frame, text="Pacemaker Welcome")
    welcome_label.pack()

    connection_UI()

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
    window.title("Telemetry")

    #Method for updating text on screen when mode is changed
    def update_text():
        #Arrays to hold all the labels on screen so they can be changed later
        entry_boxes = []
        error_labels = []
        value_labels = []
        #Clear screen
        for widget in frame2.winfo_children():
            widget.destroy()
        #Get correct parameters based on current mode
        mode_key = mode_settings[selected.get()]
        current_mode = mode_order[selected.get()]
        for i in range(len(mode_key)):
            #Create labels for each parameter's name and place them one row down each iteration
            mode_label = tk.Label(frame2, text=params[mode_key[i]] + ":")
            mode_label.grid(row = i, column = 0, pady = 10)

            #Create labels for the values of each parameter
            value_label = tk.Label(frame2, text=current_user.data[current_mode][mode_key[i]])
            value_label.grid(row=i, column=1, pady=10, padx = 5)
            #Store labels inside of an array to edit them later
            value_labels.append(value_label)

            if (params[mode_key[i]] != "Activity Threshold"):
                #Create text boxes to program parameters
                param_entry = tk.Entry(frame2)
                param_entry.grid(row = i, column = 2, padx = 10, pady = 10)
                #Store text boxes inside an array so their values can be read later
                entry_boxes.append(param_entry)
            else:
                # Create a dropdown menu
                options = ["V-Low", "Low", "Med-Low", "Med","Med-High", "High", "V-High"]
                selected_option = tk.StringVar()
                dropdown = ttk.Combobox(frame2, values=options, textvariable=selected_option)
                dropdown.set("Select an option")
                dropdown.grid(row=i, column=2, padx=10, pady=10)
                entry_boxes.append(dropdown)

            #Create labels for error messages in case the inputted values are invalid
            error_label = tk.Label(frame2, text="", fg="red")
            error_label.grid(row=i, column=3, padx = 5, pady = 10)
            #Store labels in an array to be edited later
            error_labels.append(error_label)

        #Place a button to submit changes, and when the button is pressed, execute the update_params method 
        submit_buttom = tk.Button(frame2, text="Submit Changes", command=lambda: update_params(entry_boxes,mode_key,error_labels,value_labels,current_mode))
        submit_buttom.grid(row=i+1, column=2)
    
    #Method to update the parameter values
    def update_params(entries,key,errors,values,current_mode):
        #Loop through every text box
        for i in range(len(entries)):
            #Get the entered data
            entry_text = entries[i].get().strip()
            #Check if the text box is empty
            if entry_text != "":
                # if off replace to 0
                if entry_text.lower() == "off":
                    entry_text = "0"
                #Check if the parameter is meant to be an integer
                if int_or_float[key[i]] == 1:
                    #Check if the entered data is an integer
                    if entry_text.isdigit():
                        #Check if the input is valid
                        if check_input(i, key[i], int(entry_text), errors):
                            #If the input is valid, store the result in the user data and save it to the file
                            current_user.data[current_mode][key[i]] = entry_text
                            users.update_file()
                            #Get rid of error message and change the parameter value on screen
                            errors[i].config(text="")
                            values[i].config(text = entry_text)
                    else:
                        #If the data isn't an integer, throw an error
                        errors[i].config(text = "Must enter an integer")
                #If the parameter is meant to be a float
                elif int_or_float[key[i]] == 0:
                    #Get rid of decimal point and check if the resultant is a number (check if the inputted data is a number)
                    if entry_text.replace(".","").isnumeric():
                        #Check if the input is valid
                        if check_input(i, key[i], float(entry_text), errors):
                            #If the input is valid, store the result in the user data and save it to the file with two decimal places
                            current_user.data[current_mode][key[i]] = str(round(float(entry_text),2))
                            users.update_file()
                            #Get rid of error message and change the parameter value on screen
                            errors[i].config(text="")
                            values[i].config(text = entry_text)
                    else:
                        #If the data isn't a number, throw an error
                        errors[i].config(text = "Must enter a number")
                else:
                    current_user.data[current_mode][key[i]] = entry_text
                    users.update_file()
                    errors[i].config(text="")
                    values[i].config(text = entry_text)
            else:
                #If the text box is an empty field, get rid of the error message
                errors[i].config(text="")

    #Method to check for valid input
    def check_input(label_index, index, input_data, errors):
        #Array that stores information about a parameter's valid data ranges
        param_data = params_increment[index]
        #Loop through each data range 
        for interval in param_data:
            #Check if the entered data is within one of the valid ranges
            if input_data >= interval[0] and input_data <= interval[1]:
                #Separate the case when there's no increment to avoid a zero division error
                if interval[2] == 0:
                    return 1
                #Check if the input is a multiple of the increment
                elif abs(round((input_data-interval[0])/interval[2]) - (input_data-interval[0])/interval[2]) <= 0.001:
                    return 1
                #If the entered data is on the wrong increment
                else:
                    #Throw an error and tell the user what the valid increment is
                    errors[label_index].config(text = f"Between {interval[0]} and {interval[1]}, increment must be {interval[2]}")
                    return 0
        #If the user entered data that is outside of all valid ranges
        error_string = "Input must be "
        #Tell the user the valid ranges
        for i in range(len(param_data)):
            #Include "or" when listing the last interval
            if i == len(param_data)-1 and len(param_data) > 1:
                error_string += "or "
            #Check to make sure the interval is not a singular option
            if (param_data[i][0] == param_data[i][1]):
                error_string += f"{param_data[i][0]}"
            else:
                #Add the valid intervals to the string
                error_string += f"{param_data[i][0]} - {param_data[i][1]}"
            #Add a comma after each interval
            if i != len(param_data)-1:
                error_string += ", "
        #Update the corresponding error label
        errors[label_index].config(text = error_string)
        return 0

    #Array to hold the names of the four modes
    modes = [
        "AOO",
        "VOO",
        "AAI",
        "VVI",
        "AOOR", 
        "VOOR",
        "AAIR",
        "VVIR"  
    ]

    #Array holding all parameter names
    params = [
        "Lower Rate Limit", 
        "Upper Rate Limit",
        "Maximum Sensor Rate", 
        "Atrial Amplitude",
        "Ventricular Amplitude",
        "Atrial Pulse Width",  
        "Ventricular Pulse Width",
        "Atrial Sensitivity", 
        "Ventricular Sensitivity",
        "VRP", 
        "ARP",
        "PVARP",
        "Hysteresis",
        "Rate Smoothing",
        "Activity Threshold",
        "Reaction Time",
        "Response Factor",
        "Recovery Time"
    ]

    #1 = int, 0 = float
    #Array to hold whether each parameter should be an int or float
    int_or_float = [1,1,1,0,0,1,1,0,0,1,1,1,1,1,-1,1,1,1]
    #3D array holding valid range info for each parameter
    params_increment = [[[30,50,5],[50,90,1],[90,175,5]],                                                           # Lower Rate Limit
                        [[50,175,5]],                                                                               # Upper rate Limit
                        [[50,175,5]],                                                                               # Maximum Sensor Rate
                        [[0,0,0],[0.1,5,0.1]],                                                                      # Atrial Amplitude
                        [[0,0,0],[0.1,5,0.1]],                                                                      # Venticular Amplitude
                        [[1,30,1]],                                                                                 # Atrial Pulse Width
                        [[1,30,1]],                                                                                 # Venticular Pulse Width
                        [[0,5,0.1]],                                                                                # Atrial Sensitivity
                        [[0,5,0.1]],                                                                                # Venticular Sensitivity
                        [[150,500,10]],                                                                             # VRP
                        [[150,500,10]],                                                                             # ARP
                        [[150,500,10]],                                                                             # PVARP
                        [[0,0,0],[30,50,5],[50,90,1],[90,175,5]],                                                   # Hysteresis
                        [[0,0,0],[3,3,0],[6,6,0],[9,9,0],[12,12,0],[15,15,0],[18,18,0],[21,21,0],[25,25,0]],        # Rate Smoothing
                        [],                                                                                         # Activity Threshold
                        [[10,50,10]],                                                                               # Reaction Time
                        [[1,16,1]],                                                                                 # Response Factor 
                        [[2,16,1]]                                                                                  # Recovery Time                             
                        ]

    #Lookup table that lists the parameters displayed in each mode
    mode_settings = {
        "AOO" : [0, 1, 3, 5],
        "VOO" : [0, 1, 4, 6],
        "AAI" : [0, 1, 3, 5, 7, 10, 11, 12, 13],
        "VVI" : [0, 1, 4, 6, 8, 9, 12, 13],
        "AOOR" : [0, 1, 2, 3, 5, 14, 15, 16, 17],
        "VOOR" : [0, 1, 2, 4, 6, 14, 15, 16, 17],
        "AAIR" : [0, 1, 2, 3, 5, 7, 10, 11, 12, 13, 14, 15, 16, 17],
        "VVIR" : [0, 1, 2, 4, 6, 8, 9, 12, 13, 14, 15, 16, 17]
    }

    #Lookup table to establish an order of the four modes
    mode_order = {
        "AOO" : 0,
        "VOO" : 1,
        "AAI" : 2,
        "VVI" : 3,
        "AOOR" : 4,
        "VOOR" : 5,
        "AAIR" : 6,
        "VVIR" : 7
    }

    # Create a telemetry label
    telemetry_label = tk.Label(frame, text="Welcome to Telemetry")
    telemetry_label.pack()

    egram_button = tk.Button(frame, text="Egram Data", command=lambda: update_state(AppState.EGRAM))
    egram_button.pack(pady=5)

    signout_button = tk.Button(frame, text="Sign Out", command=lambda: update_state(AppState.WELCOME))
    signout_button.pack(pady=5)

    connection_UI()

    #Set default for the dropdown menu
    selected = tk.StringVar(frame)
    selected.set(modes[0])

    #Create dropdown menu to select modes
    dropdown = tk.OptionMenu(frame, selected, *modes)
    dropdown.pack()

    #Create button to select mode
    mode_button = tk.Button(frame, text="Select", command=update_text)
    mode_button.pack()

    #Create new frame to allow grid placement
    frame2 = tk.Frame(frame)
    frame2.pack()

def show_egram_state():
    clear_frame()
    window.title("Egram Data")

    egram_label = tk.Label(frame, text="Egram Data")
    egram_label.pack()

    back_button = tk.Button(frame, text="Go Back", command=lambda: update_state(AppState.TELEMETRY))
    back_button.pack(pady=5)

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
    elif new_state == AppState.EGRAM:
        show_egram_state()

# Call the initial state
show_welcome_state()

# Start the Tkinter main loop
window.mainloop()
