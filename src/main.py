from facade.user_facade import *
from facade.vacation_facade import *
class start:
    def __init__(self):
        self.uf = UserFacade()
        self.vf = VacationFacade()
        self.invalid = "************ Oops, your input was invalid please try again ************"
        self.user_params = None

        while self.home_screen():
            self.user_params = self.uf.get_params()
            password = self.user_params[2] if len(self.user_params) < 4 else self.user_params[3]
            self.user_id = self.uf.get_user_id(self.user_params[0], self.user_params[1], password)
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
            print("1 - Logout\n2 - View all vacations\n3 - View your liked vacations \n4 - add like to vacation\n 5-remove like to a vacation")

            option = input()
            if option == "1":
                print("************ Logging out ************")
                self.user_params = None
                break
            elif option == "2":
                print("Here are all the vacations:")
                vacations = self.vf.show_all_vacation()
                for vacation in vacations:
                    print("----------------------")
                    print(vacation)


            elif option == "3":
                print("Here are all your liked vacations:")
                self.uf.logic.get_user_likes(self.user_id)
            elif option == "4":
                print("Please write the title of the vacation\n")
                title = input()
                print("Please write the start date  of the vacation\n")
                start_d = input()
                print("Please write the end date  of the vacation\n")
                end_d = input()
                self.uf.logic.add_like( self.user_id[0],(self.vf.logic.get_vac_id(title, start_d, end_d))[0])



            else:
                print(self.invalid)






#kk



if __name__ == "__main__":
    s = start()