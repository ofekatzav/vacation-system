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
    def add_like(self, first_name, last_name , password, vacation_title):
        query = "INSERT INTO likes VALUES ((SELECT id FROM mydb.users WHERE first_name LIKE %s) , (SELECT id FROM mydb.vacations WHERE title LIKE %s))"
        params = (first_name, last_name, password ,vacation_title)
        self.dal.insert(query, params)
        print("Added like successfully")
        return True

if __name__ == "__main__":
    try:
        with UserLogic() as userLogic:
            users = userLogic.get_all_users()
            for user in users:
                print("----------------------")
                print(user)
    except Exception as err:
        print(f"Error: {err}")