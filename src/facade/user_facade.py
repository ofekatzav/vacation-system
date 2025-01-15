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
        self.exit = "press e to exit"


    def add_user(self):
        print("========= SIGNUP =========")
        if self.get_first_name() or self.get_last_name() or self.get_email() or self.get_password() or self.get_b_o_d():
            print("************Exiting************")
            self.params = []
            return False

        if self.logic.user_exists(self.params[0], self.params[1], self.params[3]):
            print("User already exists in the database.")
            self.params = []
            return False

        if self.logic.add_user(*self.params):
            print("User added successfully.")
            return True
        else:
            print("Failed to add user.")
            self.params = []
            return False

    def login(self):
        # Collect login details
        print("========= LOGIN =========")
        if self.get_first_name() or self.get_last_name() or self.get_password():
            print("************Exiting************")
            self.params = []
            return False

        # Query the database for the user
        user = self.logic.get_user(self.params[0], self.params[1], self.params[2])

        # Check the results
        if user is None or len(user) == 0:
            print("Login failed: User not found.")
            self.params = []
            return False
        elif len(user) > 1:
            print("Login failed: Multiple users found with the same credentials.")
            self.params = []
            return False
        else:
            print(f"\n\nLogin successful! Welcome, {self.params[0]} {self.params[1]}.")
            return True

    def get_first_name(self):
        while True:
            first_name = input(f"{self.exit}\nEnter first name: ").strip()
            if first_name == "e":
                return "exit"
            if not first_name.replace(" ", "").isalpha():
                print("First name must contain only letters and spaces")
            elif len(first_name) < 2:
                print("First name must be at least 2 characters long")
            else:
                self.params.append(first_name)
                print("Keep going!")
                return

    def get_last_name(self):
        while True:
            last_name = input(f"{self.exit}\nEnter last name: ").strip()
            if last_name == "e":
                return "exit"
            if not last_name.replace(" ", "").isalpha():
                print("Last name must contain only letters and spaces")
            elif len(last_name) < 2:
                print("Last name must be at least 2 characters long")
            else:
                self.params.append(last_name)
                print("Keep going!")
                return

    def get_email(self):

        while True:
            email = input(f"{self.exit}\nEnter your email: ").strip()

            if email == "e":
                return "exit"

            if not email:
                print("Email cannot be empty")
                continue

            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.fullmatch(pattern, email):
                self.params.append(email)
                print("Keep going!")
                return

            else:
                print("Email is not valid")

    def get_password(self):
        while True:
            password = input(f"{self.exit}\nEnter password: ").strip()
            if password == "e":
                return "exit"
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
                print("Good!")
                return

    def get_b_o_d(self):

        while True:
            try:
                date_str = input(f"{self.exit}\nEnter your date of birth (YYYY-MM-DD): ")
                if date_str == "e":
                    return "exit"

                start_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                if start_date > self.now:
                    print("Date of birth cannot be in the future")
                    continue

                self.params.append(start_date)
                print("Great!")
                return
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD")

    def add_like(self, user_id, vacation_id):
        return self.logic.add_like(user_id, vacation_id)

    def remove_like(self, user_id, vacation_id):
        return self.logic.remove_like(user_id, vacation_id)

    def get_params(self):
        return self.params

    def set_params(self, param):
        self.params = param

    def get_user_id(self, first_name, last_name, password):
        return self.logic.get_user_id(first_name, last_name, password)

    def get_user_likes(self, user_id):
        return self.logic.get_user_likes(user_id)

    def is_admin(self, user_id):
        return self.logic.is_admin(user_id)


if __name__ == "__main__":
    user_facade = UserFacade()

    print("=== Add User ===")
    if user_facade.add_user():
        print("User successfully added to the system!")
    else:
        print("Could not add user to the system.")

    print("\n=== Login ===")
    if user_facade.login():
        print("Login was successful!")
    else:
        print("Login failed.")


