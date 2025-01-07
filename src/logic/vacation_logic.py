from src.utils.DAL import DAL


class VacationLogic:
    def __init__(self):
        self.dal = DAL()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dal.close()

    def get_all_vacations(self):
        '''returns: list of vacation dictionaries'''
        '''empty list if no vacations in the database'''

        query = "SELECT * from vacations"
        result = self.dal.get_table(query)
        return result if result is not None else []

    def add_vacation(self, title, description, start_date, end_date, countries_name, price, image):
        try:
            query = """
            INSERT INTO vacations 
            (title, description, start_date, end_date, price, likes, image_url , countries_id)
            VALUES 
            (%s, %s, %s, %s, %s, 0, %s , (SELECT id FROM mydb.countries WHERE country_name LIKE %s))
            """
            params = (title, description, start_date,
                    end_date, price, image , f"%{countries_name}%",)
            self.dal.insert(query, params)
            print("Added vacation")
            return True

        except Exception as err:
            print(f"Error adding vacation: {err}")
            return False

    def edit_vacation(self, id, **kwargs):
        if not kwargs:
            return False

        clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])

        params = tuple(kwargs.values()) + (id,)
        query = f"UPDATE vacations SET {clause} WHERE id = %s"

        try:
            self.dal.update(query, params)
            return True
        except Exception as e:
            print(f"Error updating vacation: {e}")
            return False

    def del_vacation(self, id):
        query = "DELETE FROM vacations WHERE id = %s"
        params = (id,)
        try:
            result = self.dal.delete(query, params)
            return True
        except Exception as err:
            print(f"Error deleting vacation: {err}")
            return False


if __name__ == "__main__":
    try:
        with VacationLogic() as vacation_logic:
            vacations = vacation_logic.get_all_vacations()
            for vacation in vacations:
                print("----------------------")
                print(vacation)
    except Exception as err:
        print(f"Error: {err}")