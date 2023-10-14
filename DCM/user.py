import os

class User:
    def __init__(self, name, password, data):
        self.name = name
        self.password = password
        self.data = data

class Accounts:
    def __init__(self):
        self.accounts = []
        self.length = 0

        # Get the directory of the currently executing script (this is so that when Tas open the project, working directory will not matter)
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.accounts_file_path = os.path.join(script_directory, "accounts.txt")

        # Populate Array with Users from File
        self.load_accounts()

    # Read from file and store accounts in object
    def load_accounts(self):
        try:
            with open(self.accounts_file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) == 10:
                        username, password = parts[0:2]
                        data = parts[2:]
                        self.accounts.append(User(username, password, data))
                        self.length += 1
        except FileNotFoundError:
            # Handle the case where the file doesn't exist yet
            pass

    # Add User to Object
    def add_user(self, username, password):
        # Create User
        if self.length < 10:
            self.accounts.append(User(username, password, [60, 120, 3.5, 0.4, 3.5, 0.4, 320, 250]))
            self.length += 1
            self.update_file()
        else:
            print("Accounts limit reached (10 users).")

    # Write on File
    def update_file(self):
        try:
            with open(self.accounts_file_path, "w") as file:
                for user in self.accounts:
                    file.write(f"{user.name} {user.password} ")
                    for value in user.data:
                        file.write(f"{value} ")
                    file.write("\n")
        except IOError as e:
            print(f"Error writing to accounts.txt: {e}")
