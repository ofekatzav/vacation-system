from src.utils.DAL import DAL


class CountryLogic:
    def __init__(self):
        self.dal = DAL()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dal.close()

    def get_all_countries(self):


        query = "SELECT * from countries"
        result = self.dal.get_table(query)
        return result if result is not None else []

    def add_country(self, country_name):
        try:
            query = """
            INSERT INTO vacations 
            (country_name)
            VALUES 
            (%s)
            """
            params = (country_name)
            self.dal.insert(query, params)
            return True

        except Exception as err:
            print(f"Error adding vacation: {err}")
            return False

    def edit_country(self, id, **kwargs):
        if not kwargs:
            return False

        clause = ", ".join([f"{k} = %s" for k in kwargs.keys()])

        params = tuple(kwargs.values()) + (id,)
        query = f"UPDATE countries SET {clause} WHERE id = %s"

        try:
            self.dal.update(query, params)
            return True
        except Exception as e:
            print(f"Error updating country: {e}")
            return False

    def del_country(self, id):
        query = "DELETE FROM countries WHERE id = %s"
        params = (id,)
        try:
            result = self.dal.delete(query, params)
            return True
        except Exception as err:
            print(f"Error deleting country: {err}")
            return False

    def check_if_country_exist(self, countries_name):
        query = "SELECT COUNT(*) FROM countries WHERE LOWER(country_name) = LOWER(%s)"
        params = (countries_name,)
        try:
            result = self.dal.get_table(query, params)
            return True if result is not None else False
        except Exception as err:
            print(f"Error checking if country exists: {err}")
            return False




if __name__ == "__main__":
    try:
        with CountryLogic() as country_logic:
            country = country_logic.get_all_countries()
            for country in country:
                print("----------------------")
                print(country)
    except Exception as err:
        print(f"Error: {err}")