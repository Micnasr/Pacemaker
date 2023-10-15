import os
from cryptography.fernet import Fernet # pip install cryptography
import base64

# Cryptography Key Used To Encode / Decode
hardcoded_key = "Rw8ET5s7oZ4Mc9iK97qaxnGAt8r66sBkJ1oG-09NEN0="

class User:
    def __init__(self, name, password, data):
        self.name = name
        self.password = password
        self.data = data

class Accounts:
    def __init__(self):
        self.accounts = []
        self.length = 0
        self.old_serial = ""
        self.serial = ""


        # Get the directory of the currently executing script (this is so that when Tas open the project, working directory will not matter)
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.accounts_file_path = os.path.join(script_directory, "accounts.txt")
        self.device_file_path = os.path.join(script_directory, "device.txt")

        # Populate Array with Users from File
        self.load_accounts()

    # Read from file and store accounts in object
    def load_accounts(self):
        try:
            # Initialize the key
            cipher_suite = Fernet(hardcoded_key)

            with open(self.device_file_path, "r") as file:
                lines = file.readlines()
                self.old_serial = lines[0].strip()
            
            # Handle Reading Data from files and populating data structures
            with open(self.accounts_file_path, "r") as file:
                
                lines = file.readlines()

                for encrypted_message_str in lines:
                    
                    # Decrypt the message
                    encrypted_message = base64.b64decode(encrypted_message_str.encode())
                    decrypted_message = cipher_suite.decrypt(encrypted_message)

                    # Remove the 'b' prefix
                    decrypted_message = decrypted_message.decode()
                    decrypted_message = decrypted_message.lstrip('b')

                    # Decoded String
                    parts = decrypted_message.strip().split()

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
            self.accounts.append(User(username, password, [60, 120, 3.5, 0.4, 3.5, 0.4, 320, 250])) # Nominal values of Params
            self.length += 1
            self.update_file()
        else:
            print("Accounts limit reached (10 users).")

    # Write on File

    def update_device_file(self):
        with open(self.device_file_path, "w") as file:
            file.write(self.serial)
            
    def update_file(self):
        try:
            # Initialize the Key
            cipher_suite = Fernet(hardcoded_key)
            with open(self.accounts_file_path, "w") as file:
                for user in self.accounts:

                    raw_string = ""
                    raw_string += f"{user.name} {user.password} "
                    
                    for value in user.data:
                        raw_string += f"{value} "

                    raw_string += "\n"

                    # Encrypt Data 
                    encrypted_message = cipher_suite.encrypt(raw_string.encode())
                    encrypted_message_str = base64.b64encode(encrypted_message).decode()
                    
                    # Write on File
                    file.write(encrypted_message_str + '\n')


        except IOError as e:
            print(f"Error writing to accounts.txt: {e}")
