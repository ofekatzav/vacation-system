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



if __name__ == "__main__":
    try:
        with LikesLogic() as like_logic:
            likes = like_logic.get_all_likes()
            for like in likes:
                print("----------------------")
                print(like)
    except Exception as err:
        print(f"Error: {err}")