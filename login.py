def check_exist_user(username):
    try:
        with open("account.txt", "r") as f:
            for line in f:
                stored_username = line.strip().split(",")[0]
                if stored_username == username:
                    return True
    except FileNotFoundError:
        pass
    return False


def store_acc(username, password):
    with open("account.txt", "a") as f:
        f.write(f"{username},{password}\n")


def register():
    username = input("Enter your username: ")
    if check_exist_user(username):
        print("Account already exists.")    
        return

    password = input("Enter your password: ")
    store_acc(username, password)
    print("Account created successfully.")

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    try:
        with open("account.txt", "r") as f:
            for line in f:
                stored_username, stored_password = line.strip().split(",")
                if stored_username == username and stored_password == password:
                    print("Login successful.")
                    return True
    except FileNotFoundError:
        pass

    print("Invalid username or password.")
    return False

option = input("Do you want to register or login? (register/login): ").strip().lower()
if option == "register":
    register()
elif option == "login":
    login()