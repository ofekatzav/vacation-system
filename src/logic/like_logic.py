from src.utils.DAL import DAL


class LikesLogic:
    def __init__(self):
        self.dal = DAL()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dal.close()

    def get_all_likes(self):


        query = "SELECT * from likes"
        result = self.dal.get_table(query)
        return result if result is not None else []

    def add_like(self , user_id , vacation_id):
        try:
            query = """
            INSERT INTO likes 
            (users_id , vacations_id)
            VALUES 
            (user_id, vacations_id)
            """
            params = (user_id, vacation_id)
            self.dal.insert(query, params)
            print("Added like")
            return True

        except Exception as err:
            print(f"Error adding like: {err}")
            return False


if __name__ == "__main__":
    try:
        with LikesLogic() as like_logic:
            likes = like_logic.get_all_likes()
            for like in likes:
                print("----------------------")
                print(like)
    except Exception as err:
        print(f"Error: {err}")