from flask import Flask, request
import pandas as pd
from joblib import load
import os

app = Flask(__name__)

# Determine the path where the models and CSV files will be located inside the Docker container
MODEL_DIR = "/Intern/"
DATA_DIR = "/Intern/"

# Load the saved models
ca_model = load(os.path.join(MODEL_DIR, 'RandomForest_ModelCa.joblib'))
hb_model = load(os.path.join(MODEL_DIR, 'RandomForest_ModelHb.joblib'))
gl_model = load(os.path.join(MODEL_DIR, 'RandomForest_ModelGl.joblib'))

# Load the CSV files
df_ca = pd.read_csv(os.path.join(DATA_DIR, "interpolatedca.csv"))
df_hb = pd.read_csv(os.path.join(DATA_DIR, "interpolatedHb.csv"))
df_gl = pd.read_csv(os.path.join(DATA_DIR, "interpolatedgl.csv"))  

# Function to predict concentration value given values from the 2nd to 4th columns
def predict_concentration(model, df, input_value):
    try:
        # Predict concentration value using the loaded Random Forest model
        concentration_prediction = model.predict([[input_value] * 3])
        return format(concentration_prediction[0], ".2f")
    except Exception as e:
        return str(e)

@app.route("/")
def root():
    with open(os.path.join(DATA_DIR, "result.html")) as file:
        return file.read()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        model_choice = request.form['model']
        input_values_str = request.form['input_value']
        input_values = [float(value.strip()) for value in input_values_str.split(',')]

        results = "<table border='1'><tr><th>Input Value</th><th>Predicted Concentration</th></tr>"

        if model_choice == "ca":
            for value in input_values:
                predicted_concentration = predict_concentration(ca_model, df_ca, value)
                results += f"<tr><td>{value}</td><td>{predicted_concentration}</td></tr>"
        elif model_choice == "hb":
            for value in input_values:
                predicted_concentration = predict_concentration(hb_model, df_hb, value)
                results += f"<tr><td>{value}</td><td>{predicted_concentration}</td></tr>"
        elif model_choice == "gl":
            for value in input_values:
                predicted_concentration = predict_concentration(gl_model, df_gl, value)
                results += f"<tr><td>{value}</td><td>{predicted_concentration}</td></tr>"
        else:
            return "Invalid model choice. Please choose 'ca', 'hb', or 'gl'."

        results += "</table>"
        return results
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(port=5002, host='0.0.0.0', debug=False)
