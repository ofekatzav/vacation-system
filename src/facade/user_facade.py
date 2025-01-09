import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

import re
from datetime import datetime, date
from src.logic.user_logic import UserLogic


class UserFacade:
    def __init__(self):
        self.params = []
        self.now = date.today()
        self.logic = UserLogic()


    def add_user(self):
        self.get_first_name()
        self.get_last_name()
        self.get_email()
        self.get_password()
        self.get_b_o_d()
        if self.logic.user_exists(self.params[0], self.params[1], self.params[3]):
            print("User already exists in the database.")
            return False

        if self.logic.add_user(*self.params):
            print("User added successfully.")
            return True
        else:
            print("Failed to add user.")
            return False

    def login(self):
        # Collect login details
        self.get_first_name()
        self.get_last_name()
        self.get_password()

        # Query the database for the user
        user = self.logic.get_user(self.params[0], self.params[1], self.params[2])

        # Check the results
        if user is None or len(user) == 0:
            print("Login failed: User not found.")
            return False
        elif len(user) > 1:
            print("Login failed: Multiple users found with the same credentials.")
            return False
        else:
            print(f"Login successful! Welcome, {self.params[0]} {self.params[1]}.")
            return True

    def get_first_name(self):
        while True:
            first_name = input("Enter first name : ").strip()
            if not first_name.replace(" ", "").isalpha():
                print("first name must contain only letters and spaces")
            elif len(first_name) < 2:
                print("first name must be at least 2 characters long")
            else:
                self.params.append(first_name)
                print("first name added")
                break
    def get_last_name(self):
        while True:
            last_name = input("Enter last name : ").strip()
            if not last_name.replace(" ", "").isalpha():
                print("last name must contain only letters and spaces")
            elif len(last_name) < 2:
                print("last name must be at least 2 characters long")
            else:
                self.params.append(last_name)
                print("last name added")
                break

    def get_email(self):
        while True:
            email = input("Enter your email : ").strip()

            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(pattern, email):
                self.params.append(email)
                print("email added")
                break
            else:
                print("email is not valid")

    def get_password(self):
        while True:
            password = input("Enter password : ").strip()
            if len(password) < 8:
                print("Password must be at least 8 characters long.")


            elif not any(char.isupper() for char in password):
               print("Password must include at least one uppercase letter.")


            elif not any(char.islower() for char in password):
               print("Password must include at least one lowercase letter.")


            elif not any(char.isdigit() for char in password):
                print("Password must include at least one digit.")
            else:
                self.params.append(password)
                print("password added")
                break

    def get_b_o_d(self):

        while True:
            try:
                date_str = input("Enter your date of birth (YYYY-MM-DD): ")
                start_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                if start_date > self.now:
                    print("date of birth cannot be in the future")
                    continue

                self.params.append(start_date)
                print("Start date added")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD")






if __name__ == "__main__":

    user = UserFacade()




    print("=== Add User ===")
    if user.add_user():
        print("User successfully added to the system!")
    else:
        print("Could not add user to the system.")


