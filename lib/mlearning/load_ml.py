import json
import pickle
import numpy as np

with open('lib/mlearning/xgb_vibration_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Define the target names
target_names = [
    'mode1_theta1', 'mode1_theta2', 'mode1_lambda1', 'mode1_lambda2',
    'mode1_psi1', 'mode1_psi2', 'mode1_mu1', 'mode1_mu2', 'mode1_frequency',
    'mode2_theta1', 'mode2_theta2', 'mode2_lambda1', 'mode2_lambda2',
    'mode2_psi1', 'mode2_psi2', 'mode2_mu1', 'mode2_mu2', 'mode2_frequency',
    'mode3_theta1', 'mode3_theta2', 'mode3_lambda1', 'mode3_lambda2',
    'mode3_psi1', 'mode3_psi2', 'mode3_mu1', 'mode3_mu2', 'mode3_frequency'
]


def model_predict(input_data, model=loaded_model):
    """
    This function takes in input data and a trained multi-output regression model,
    and returns the predictions as a JSON string.

    Parameters:
    input_data (array-like): The input features to predict on.
    model (MultiOutputRegressor): The trained multi-output regression model.

    Returns:
    str: JSON string with the predictions mapped to their respective target names.
    """
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1) if len(input_data_as_numpy_array.shape) == 1 else input_data_as_numpy_array

    # Make predictions
    prediction = model.predict(input_data_reshaped)

    # Convert prediction to a list of floats
    prediction_as_list = prediction[0].tolist()

    # Map predictions to target names
    prediction_dict = {target_names[i]: float(prediction_as_list[i]) for i in range(len(target_names))}

    # Convert to JSON
    prediction_json = json.dumps(prediction_dict, indent=4)

    return prediction_json

# input_sample = X_test
# prediction_json = model_predict(input_sample, loaded_model)
# print(prediction_json)
