import json

import numpy as np
from lib.view.solve_equation import SolveEquation
from lib.mlearning.load_ml import model_predict
from lib.database.sql_queries import SQLQuery


class PredictModel:

    @staticmethod
    def predict_model(features) -> dict:
        expected_order = ['Length', 'Non-local Param', 'Diameter', 'LEP k1', 'LEP k2', 'Temp', 'Velocity',
                          'Initial Disp']
        feature_array = []

        for order in expected_order:
            feature_array.append(features[order])

        # convert the feature_array to a numpy array
        new_array = np.array(feature_array)
        data = json.loads(model_predict(new_array))
        predicted_data = {key: value for key, value in data.items()}
        return predicted_data

    @staticmethod
    def convert_model(features, user_id):
        try:
            predicted_data = PredictModel.predict_model(features)
            arranged_data = dict()

            if predicted_data is not None and isinstance(predicted_data, dict):
                # add the mode 1 data into the map
                arranged_data["mode 1"] = dict()
                arranged_data["mode 1"]["theta1"] = predicted_data["mode1_theta1"]
                arranged_data["mode 1"]["theta2"] = predicted_data["mode1_theta2"]
                arranged_data["mode 1"]["lambda1"] = predicted_data["mode1_lambda1"]
                arranged_data["mode 1"]["lambda2"] = predicted_data["mode1_lambda2"]
                arranged_data["mode 1"]["psi1"] = predicted_data["mode1_psi1"]
                arranged_data["mode 1"]["psi2"] = predicted_data["mode1_psi2"]
                arranged_data["mode 1"]["phi1"] = predicted_data["mode1_mu1"]
                arranged_data["mode 1"]["phi2"] = predicted_data["mode1_mu2"]

                arranged_data["mode 2"] = dict()
                arranged_data["mode 2"]["theta1"] = predicted_data["mode2_theta1"]
                arranged_data["mode 2"]["theta2"] = predicted_data["mode2_theta2"]
                arranged_data["mode 2"]["lambda1"] = predicted_data["mode2_lambda1"]
                arranged_data["mode 2"]["lambda2"] = predicted_data["mode2_lambda2"]
                arranged_data["mode 2"]["psi1"] = predicted_data["mode2_psi1"]
                arranged_data["mode 2"]["psi2"] = predicted_data["mode2_psi2"]
                arranged_data["mode 2"]["phi1"] = predicted_data["mode2_mu1"]
                arranged_data["mode 2"]["phi2"] = predicted_data["mode2_mu2"]

                arranged_data["mode 3"] = dict()
                arranged_data["mode 3"]["theta1"] = predicted_data["mode3_theta1"]
                arranged_data["mode 3"]["theta2"] = predicted_data["mode3_theta2"]
                arranged_data["mode 3"]["lambda1"] = predicted_data["mode3_lambda1"]
                arranged_data["mode 3"]["lambda2"] = predicted_data["mode3_lambda2"]
                arranged_data["mode 3"]["psi1"] = predicted_data["mode3_psi1"]
                arranged_data["mode 3"]["psi2"] = predicted_data["mode3_psi2"]
                arranged_data["mode 3"]["phi1"] = predicted_data["mode3_mu1"]
                arranged_data["mode 3"]["phi2"] = predicted_data["mode3_mu2"]

                data = SolveEquation.solve_deformation(arranged_data, features['Length'])

                SQLQuery.insert_data(
                    user_id=user_id,
                    length=features["Length"],
                    diameter=features["Diameter"],
                    non_local_param=features["Non-local Param"],
                    linear_foundation=features["LEP k1"],
                    non_linear_foundation=features["LEP k2"],
                    temperature=features["Temp"],
                    velocity=features["Velocity"],
                    initial_disp=features["Initial Disp"],
                    data_2d=data["data_2d"],
                    data_3d=data["data_3d"]
                )
                print(features)
                final_data = {'user_id': user_id, 'length': features["Length"],
                              'diameter': features["Diameter"], 'non_local_param': features["Non-local Param"],
                              'linear_foundation': features["LEP k1"],
                              'non_linear_foundation': features["LEP k2"], 'temperature': features["Temp"],
                              'velocity': features["Velocity"], 'initial_disp': features["Initial Disp"],
                              'data_2d': data["data_2d"], 'data_3d': data["data_3d"]}

                print(final_data)
                return final_data

        except Exception as e:
            print(e)
            return e
