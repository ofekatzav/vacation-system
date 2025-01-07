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


        return self.logic.add_user(*self.params)

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




    def get_countries_name(self):
        while True:
            countries_name = input("Enter country name: ").lower()
            if self.country_logic.check_if_country_exist(countries_name):
                print("Country added to vacation info!")
                self.params.append(countries_name)
                break
            else:
                print(
                    "Country does not exist in database, here is a list of all countries:")
                countries = self.country_logic.get_all_countries()
                print(" | ".join(country["country_name"]
                      for country in countries))



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



    def get_price(self):
        while True:
            try:
                price = float(input("Enter price: "))
                if not 1000 <= price <= 10000:
                    print("Price must be between 1000 and 10000")
                else:
                    self.params.append(price)
                    print("Price added")
                    break
            except ValueError:
                print("Price must be a number!")

    def get_image(self):
        while True:
            image_url = input(
                "Enter image URL (optional, press Enter to skip): ").strip()
            if not image_url:
                self.params.append(None)
                print("No image URL selected")
                break

            # Basic URL validation with regular expression
            url_pattern = r'^https?:\/\/[^\s\/$.?#].[^\s]*$'
            if not re.match(url_pattern, image_url):
                print("Invalid URL format!")
                continue

            self.params.append(image_url)
            print("Image URL added")
            break


if __name__ == "__main__":

    user = UserFacade()

    result = user.add_user()

    print("\nBooking Results:")
    print("---------------")
    print(f"user first name: {user.params[0]}")
    print(f"user last name: {user.params[1]}")
    print(f"user email: {user.params[2]}")
    print(f"user password  : {user.params[3]}")
    print(f"user date of birth : {user.params[4]}")
