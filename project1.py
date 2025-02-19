from cryptography.fernet import Fernet
import os

def key_generation():
    
    if not os.path.exists('key.key'):
        key = Fernet.generate_key()
        with open('key.key', 'wb') as key_file:
            key_file.write(key)
        print("Key generated successfully.")
    else:
        print("Key already exists.")

def load_key():
    
    try:
        with open('key.key', 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print("Error: Key file not found! Please run key_generation().")
        exit()

key_generation()
key = load_key()
fer = Fernet(key)

def view():
    
    try:
        with open('password.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                try:
                    usr, enc_pass = data.split("|")
                    dec_pass = fer.decrypt(enc_pass.encode()).decode()
                    print(f"User: {usr} | Password: {dec_pass}")
                except Exception as e:
                    print(f"Error decrypting password for {usr}: {e}")
    except FileNotFoundError:
        print("No passwords stored yet.")

def add():
    """Add a new password."""
    name = input("Enter User Account ID: ").strip()
    pwd = input("Enter the Password: ").strip()
    
    if not name or not pwd:
        print("Error: Username and password cannot be empty.")
        return

    enc_pwd = fer.encrypt(pwd.encode()).decode()
    
    with open('password.txt', 'a') as f:
        f.write(name + "|" + enc_pwd + "\n")
    
    print("Password saved successfully.")

while True:
    mod = input("Would you like to add a password or view the password? (view|add) or 'q' to Quit: ").strip().lower()

    if mod == "q":
        break
    elif mod == "view":
        view()
    elif mod == "add":
        add()
    else:
        print("Invalid choice. Please enter 'view', 'add', or 'q'.")
