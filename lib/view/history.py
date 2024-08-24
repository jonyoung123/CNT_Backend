from lib.database.sql_queries import SQLQuery


class PredictionHistory:

    @staticmethod
    def history_data(user_id):
        data = []
        response = SQLQuery.fetch_data_by_id(user_id)
        if response is not None:
            for resp in response:
                data.append(resp.to_dict())

        final_data = dict()
