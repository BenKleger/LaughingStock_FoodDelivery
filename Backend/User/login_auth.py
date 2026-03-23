from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from FastAPI_DB.services.users_service import create_users, get_user_by_username
from FastAPI_DB.schemas.user import UserCreate

invalid = True

def login():
    print("Select Valid Option: \n(0) Login\n(1) Create New Account\n")

    while(invalid):
        option = input()
        if (option == "0" or option == "1"):
            break
        print("Invalid Entry. Try Again.\n")

    print()

    if (option == "1"): create()
    else: 
        while(invalid):
            username_input = input("Username: ")
            password_input = input("Password: ")

            try:
                if (get_user_by_username(username_input).password == password_input):
                    print("\nLogin successful!")
                    break
                print("Incorrect email or password. Please try again.\n")
            except HTTPException:
                print("Incorrect email or password. Please try again.\n")
        
        return get_user_by_username(username_input).id
            
def create():
    while(invalid):
        username_input = input("Username: ")
        try:
            get_user_by_username(username_input)
            print("Username is taken.\n\n")
        except HTTPException:
            acc_type = (input("Select account type: \n(1) Customer \n(2) Driver \n(3) Manager\n")) 
            if acc_type != "1" and acc_type != "2" and acc_type != "3":
                print("Invalid account type. Please try again.\n\n")
                continue

            password1_input = input("Password: ")
            password2_input = input("Repeat Password: ")
            
            if (password1_input == password2_input):
                new_user = create_users(UserCreate(username=username_input, password=password1_input, type = int(acc_type)))
                print("\nAccount creation successful!")
                return new_user
            else:
                print("Passwords do not match. Please try again.\n\n")