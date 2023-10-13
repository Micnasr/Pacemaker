import os

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password

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
                    if len(parts) == 2:
                        username, password = parts
                        self.accounts.append(User(username, password))
                        self.length += 1
        except FileNotFoundError:
            # Handle the case where the file doesn't exist yet
            pass

    # Add User to Object
    def add_user(self, username, password):
        # Create User
        if self.length < 10:
            self.accounts.append(User(username, password))
            self.length += 1
            self.update_file()
        else:
            print("Accounts limit reached (10 users).")

    # Write on File
    def update_file(self):
        try:
            with open(self.accounts_file_path, "w") as file:
                for user in self.accounts:
                    file.write(f"{user.name} {user.password}\n")
        except IOError as e:
            print(f"Error writing to accounts.txt: {e}")
