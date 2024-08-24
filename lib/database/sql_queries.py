from lib.config import db
from lib.model.models import Predictions


class SQLQuery:

    @staticmethod
    def create_db_table():
        """Creates the table based on the model definitions."""
        db.create_all()
        return "Tables created successfully."

    @staticmethod
    def insert_data(user_id, length, diameter, non_local_param, linear_foundation, non_linear_foundation,
                    temperature, velocity, initial_disp, data_3d, data_2d):
        """Inserts data into the Prediction table."""
        new_entry = Predictions(user_id=user_id,length=length, diameter=diameter,
                                non_local_param=non_local_param, linear_foundation=linear_foundation,
                                non_linear_foundation=non_linear_foundation, temperature=temperature,
                                velocity=velocity, initial_disp=initial_disp,
                                data_3d=data_3d, data_2d=data_2d)
        db.session.add(new_entry)
        db.session.commit()
        return "Data inserted successfully."

    @staticmethod
    def fetch_all_data():
        """Fetches all data from the Prediction table."""
        return Predictions.query.all()

    @staticmethod
    def fetch_data_by_id(user_id):
        """Fetches data for a specific user_id from the Prediction table."""
        result = Predictions.query.filter_by(user_id=user_id)
        print(f"User by id ====>> {result}")
        return result
