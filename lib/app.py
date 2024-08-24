from flask import request, jsonify
from lib.config import app
from lib.database.sql_queries import SQLQuery
from sqlalchemy.exc import IntegrityError
from lib.mlearning.predict_ml import PredictModel


@app.route('/create', methods=["GET"])
def create_db_table():
    try:
        response = SQLQuery.create_db_table()
        return jsonify({
            "responseCode": "00",
            "responseMessage": response
        }), 201
    except Exception as e:
        print(f"Error: =====>>> {e}")
        return jsonify({
            "code": "E02",
            "desc": "Error creating table"
        }), 401


@app.route('/predict', methods=["POST"])
def predict_data():
    # ['Length', 'Non-local Param', 'Diameter', 'LEP k1', 'LEP k2', 'Temp',
    #        'Velocity', 'Initial Disp']
    try:
        request_data = {}
        if request.is_json:
            request_data = request.get_json()
        elif len(request.form) > 0:
            request_data = request.form
        # create a dict value for the incoming data
        features_dict = dict()
        user_id = request_data['user_id']
        features_dict["Length"] = request_data['length']
        features_dict["Non-local Param"] = request_data['non_local_param']
        features_dict["Diameter"] = request_data['diameter']
        features_dict["LEP k1"] = request_data['k1']
        features_dict["LEP k2"] = request_data['k2']
        features_dict["Temp"] = request_data['temperature_difference']
        features_dict["Velocity"] = request_data['velocity']
        features_dict["Initial Disp"] = request_data['initial_displacement']
        response = PredictModel.convert_model(features_dict, user_id)

        return jsonify({
            "responseCode": "00",
            "responseMessage": "Prediction successfully fetched",
            "responseData": response
        }), 201
    except IntegrityError as e:
        return jsonify({
            "code": "E04",
            "desc": f"Error: User with id already exist"
        }), 401
    except Exception as e:
        print(f"error === > {e}")
        return jsonify({
            "code": "E02",
            "desc": "Error inserting data"
        }), 401


@app.route('/fetch/all', methods=["GET"])
def fetch_all_data():
    try:
        data = []
        response = SQLQuery.fetch_all_data()
        print(f"Response data ===>>> {response}")
        if response is not None:
            for prediction in response:
                data.append(prediction.to_dict())
            return jsonify({
                "responseCode": "00",
                "responseMessage": "Prediction data fetched successfully",
                "responseData": data,
                "count": len(data)
            }), 201
    except Exception as e:
        print(f"Error: =====>>> {e}")
        return jsonify({
            "code": "E02",
            "desc": "Error fetching data"
        }), 401


@app.route('/history/<user_id>', methods=["GET"])
def fetch_by_id(user_id):
    if user_id is None:
        return jsonify({
            "code": "E03",
            "desc": "An id must be passed"
        }), 401
    try:
        data = []
        response = SQLQuery.fetch_data_by_id(user_id)
        if response is not None:
            for resp in response:
                data.append(resp.to_dict())
            return jsonify({
                "responseCode": "00",
                "responseMessage": "Prediction data fetched successfully",
                "responseData": data,
                "count": len(data)
            }), 201,
        else:
            return jsonify({
                "code": "E02",
                "desc": f"{user_id} not found."
            }), 401
    except Exception as e:
        print(f"Error: =====>>> {e}")
        return jsonify({
            "code": "E02",
            "desc": "Error fetching data"
        }), 401


if __name__ == '__main__':
    app.run()
