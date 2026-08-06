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


register()