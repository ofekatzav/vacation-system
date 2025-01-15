from src.utils.DAL import DAL


class UserLogic:
    def __init__(self):
        self.dal = DAL()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dal.close()

    def get_all_users(self):


        query = "SELECT * from users"
        result = self.dal.get_table(query)
        return result if result is not None else []

    def add_user(self, first_name, last_name, email, password, d_o_b, roles_id =1):
        try:
            query = """
            INSERT INTO users
             (first_name, last_name, email, password, d_o_b, roles_id) 
            VALUES 
            (%s, %s, %s, %s, %s, %s )
            """
            params = (first_name, last_name, email,
                    password, d_o_b, roles_id)
            self.dal.insert(query, params)
            print("Added user successfully")
            return True

        except Exception as err:
            print(f"Error adding user: {err}")
            return False

    def edit_user(self, id, **kwargs):
        if not kwargs:
            return False

        clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])

        params = tuple(kwargs.values()) + (id,)
        query = f"UPDATE users SET {clause} WHERE id = %s"

        try:
            self.dal.update(query, params)
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    def del_user(self, id):
        query = "DELETE FROM users WHERE id = %s"
        params = (id,)
        try:
            result = self.dal.delete(query, params)
            return True
        except Exception as err:
            print(f"Error deleting user: {err}")
            return False
    def get_user(self, first_name, last_name, password):
        query = "SELECT * from users WHERE first_name = %s AND last_name = %s AND password = %s"
        params = (first_name, last_name, password)
        try:
            result = self.dal.get_table(query, params)
            return result if result is not None else None
        except Exception as err:
            print(f"Error getting user: {err}")

    def user_exists(self, first_name, last_name, password):

        query = "SELECT COUNT(*) as count FROM users WHERE first_name = %s AND last_name = %s AND password = %s"
        params = (first_name, last_name, password)
        try:
            result = self.dal.get_scalar(query, params)
            return result['count'] > 0 if result else False
        except Exception as err:
            print(f"Error checking if user exists: {err}")
            return False


    def is_admin(self, user_id):
        query = "SELECT roles_id FROM users WHERE id = %s"
        params = (user_id,)
        try:
            result = self.dal.get_scalar(query, params)
            return True if result is not None and int(result['roles_id'])==2 else False
        except Exception as err:
            print(f"Error checking if user exists: {err}")

    def get_user_id(self, first_name, last_name, password):
        query = "SELECT id from users WHERE first_name = %s AND last_name = %s AND password = %s"
        params = (first_name, last_name, password)
        try:
            result = self.dal.get_table(query, params)
            return result if result is not None else None
        except Exception as err:
            print(f"Error getting user_id: {err}")

    def add_like(self, user_id, vacation_id):

        if not self.check_vac_id_exist(vacation_id):
            print("Vacation not found, try again")
            return False

        elif self.check_like_already_exist(user_id, vacation_id):
            print("You already liked that vacation")
            return False

        else:
            query = "INSERT INTO likes (users_id , vacations_id) VALUES (%s , %s)"
            params = (user_id, vacation_id)
            self.dal.insert(query, params)
            query = "update vacations set likes = likes + 1 where id = (%s)"
            params = (vacation_id,)
            self.dal.update(query, params)
            print("LIKED")
            return True


    def remove_like(self,user_id, vacation_id):

        if not self.check_vac_id_exist(vacation_id):
            print("Vacation not found, try again")
            return False

        elif not self.check_like_already_exist(user_id, vacation_id):
            print("You didn't like that vacation")
            return False

        else:
            query = "DELETE FROM likes WHERE users_id = %s AND vacations_id = %s"
            params = (user_id, vacation_id)
            self.dal.delete(query, params)
            query = "update vacations set likes = likes - 1 where id = (%s)"
            params = (vacation_id,)
            self.dal.update(query, params)
            print("Removed like successfully")
            return True

    def get_user_likes(self, user_id):
        query = "SELECT v.* from vacations v, likes l WHERE l.users_id = %s and l.vacations_id = v.id"
        params = (user_id,)
        result = self.dal.get_table(query, params)
        return result if result is not None else []

    def check_like_already_exist(self, user_id, vacation_id):
        query = "select * from likes where users_id = %s and vacations_id = %s"
        params = (user_id, vacation_id)
        result = self.dal.get_table(query, params)
        return bool(result)


    def check_vac_id_exist(self, vac_id):
        query = "SELECT * from vacations where id = %s"
        params = (vac_id,)
        result = self.dal.get_one(query, params)
        return bool(result)

if __name__ == "__main__":
    try:
        with UserLogic() as userLogic:
            # Validate get_all_users
            print("Fetching all users...")
            users = userLogic.get_all_users()
            if users:
                print("Users retrieved:")
                for user in users:
                    print(user)
            else:
                print("No users found.")

            # Validate add_user
            new_user = ("John", "Doe", "john.doe@example.com", "password123", "1990-01-01", 1)
            print(f"Adding user: {new_user}")
            if userLogic.user_exists(*new_user[:3]):
                print(f"User {new_user[0]} {new_user[1]} already exists.")
            else:
                success = userLogic.add_user(*new_user)
                print("User added successfully." if success else "Failed to add user.")

            # Validate is_admin
            user_id = 1
            print(f"Checking if user ID {user_id} is an admin...")
            if userLogic.is_admin(user_id):
                print(f"User ID {user_id} is an admin.")
            else:
                print(f"User ID {user_id} is not an admin.")

    except Exception as err:
        print(f"Error: {err}")