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
        #need to fix
        query = "SELECT COUNT(*) as count FROM countries WHERE LOWER(country_name) = LOWER(%s)"
        params = (countries_name,)
        try:
            result = self.dal.get_table(query, params)
            return True if result is not None and result[0]['count']>0 else False
        except Exception as err:
            print(f"Error checking if country exists: {err}")
            return False





if __name__ == "__main__":
    try:
        with CountryLogic() as country_logic:
            # Validate get_all_countries
            print("Fetching all countries...")
            countries = country_logic.get_all_countries()
            if countries:
                print("Countries retrieved:")
                for country in countries:
                    print(country)
            else:
                print("No countries found.")

            # Validate add_country
            new_country = "Spain"
            print(f"Adding country: {new_country}")
            if country_logic.check_if_country_exist(new_country):
                print(f"Country {new_country} already exists.")
            else:
                success = country_logic.add_country(new_country)
                if success:
                    print(f"Country {new_country} added successfully.")
                else:
                    print(f"Failed to add country {new_country}.")

            # Validate edit_country
            country_id = 1
            new_data = {"country_name": "Spain Updated"}
            print(f"Updating country with ID {country_id}...")
            if country_logic.edit_country(country_id, **new_data):
                print("Country updated successfully.")
            else:
                print(f"Failed to update country with ID {country_id}.")

            # Validate del_country
            del_country_id = 2
            print(f"Deleting country with ID {del_country_id}...")
            if country_logic.del_country(del_country_id):
                print("Country deleted successfully.")
            else:
                print(f"Failed to delete country with ID {del_country_id}.")

            # Validate check_if_country_exist
            country_name_to_check = "Spain"
            print(f"Checking if country '{country_name_to_check}' exists...")
            if country_logic.check_if_country_exist(country_name_to_check):
                print(f"Country '{country_name_to_check}' exists.")
            else:
                print(f"Country '{country_name_to_check}' does not exist.")

    except Exception as err:
        print(f"Error: {err}")