from facade.user_facade import *
class start:
    def __init__(self):
        self.uf = UserFacade()
        self.invalid = "************ Oops, your input was invalid please try again ************"

        while self.home_screen():
            self.app_menu()


    def home_screen(self):
        print("Choose an option:")
        flag = -1
        while flag == -1:
            print("\n1 - SIGNUP \n2 - LOGIN\n3 - EXIT")
            option = input()
            if option == "1" and self.uf.add_user():
                flag = 1
            elif option == "2" and self.uf.login():
                flag = 1
            elif option == "3":
                print("Bye bye <3")
                flag = 0
            elif option != "1" and option != "2" and option != "3":
                print(self.invalid)
        return flag
    def app_menu(self):
        while True:
            print("What would you like to do?")
            print("1 - Logout\n2 - View all vacations\n3 - View your liked vacations")
            option = input()
            if option == "1":
                print("************ Logging out ************")
                break
            elif option == "2":
                print("Here are all the vacations:")
            elif option == "3":
                print("Here are all your liked vacations:")
            else:
                print(self.invalid)










if __name__ == "__main__":
    s = start()