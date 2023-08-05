import time as time_lib
import argparse
from flask_api import status
import flask
from flask_cors import CORS
import os
import joblib
import json
import tensorflow as tf
import pandas
import numpy

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

from easierSDK.easier import EasierSDK
from easierSDK.classes.categories import Categories
from easierSDK.classes.model_metadata import ModelMetadata
from easierSDK.classes.easier_model import EasierModel
import easierSDK.classes.constants as constants
from easierSDK import datasetsAPI

# Variable definition
easier = None
easier_model = None

@app.route("/predict" + "/<string:input_data>", methods=["GET"])
def predict(input_data):
    request = flask.request
    results = {"status": "error"}

    if request.method == "GET":
        results["status"] = "success"

        stat = status.HTTP_200_OK

        global easier_model

        try:
            start_time = time_lib.clock()
        except Exception as e:
            start_time = time_lib.process_time()
        
        data = input_data.split(",")
        input_df = pandas.DataFrame([data]).apply(pandas.to_numeric, errors='ignore', axis=0)

        predictions = easier_model.get_model().predict(input_df.values)

        try:
            end_time = time_lib.clock()
        except Exception as e:
            end_time = time_lib.process_time()

        elapsed_time = end_time - start_time

        results["latency"] = elapsed_time
        results["prediction"] = predictions.tolist()
    else:
        results["status"] = "error_method_incorrect"
        stat = status.HTTP_405_METHOD_NOT_ALLOWED

    return flask.jsonify(results), stat 


@app.route("/compute", methods=["GET"])
def compute():
    request = flask.request
    results = {"status": "error"}
    print(request)
    if request.method == "GET":
        results["status"] = "success"

        stat = status.HTTP_200_OK

        try:
            start_time = time_lib.clock()
        except Exception as e:
            start_time = time_lib.process_time()

        data = request.get_json()
        confidences, classes_pred, predictions = get_prediction(data)

        try:
            end_time = time_lib.clock()
        except Exception as e:
            end_time = time_lib.process_time()

        elapsed_time = end_time - start_time
        results["latency"] = elapsed_time

        if predictions is None:
            stat = status.HTTP_500_INTERNAL_SERVER_ERROR
            results["status"] = "error while predicting"
            return flask.jsonify(results), stat

        results["prediction"] = predictions.tolist()
        if confidences: 
            results["confidence"] = confidences
            results["class"] = classes_pred.tolist()

    else:
        results["status"] = "error_method_incorrect"
        stat = status.HTTP_405_METHOD_NOT_ALLOWED

    return flask.jsonify(results), stat

def get_prediction(features_values_dict):
    
    global easier_model
    global easier

    # Parse data
    try:
        if easier_model.metadata.features and len(easier_model.metadata.features)>0:
            data = pandas.DataFrame(columns=easier_model.metadata.features)
            input_df = pandas.DataFrame([features_values_dict])
            data = data.append(input_df, sort=False).apply(pandas.to_numeric, errors='ignore', axis=0)
            # Drop missing columns, expected only to be label column
            data = data.dropna(axis=1)
        else:
            data = pandas.DataFrame([features_values_dict])
    except Exception as e:
        print("Could not parse properly the input data" + " - error: " + str(e))
        return None, None, None

    # Use feature encoder
    non_numeric = data.select_dtypes(include='object')
    if not non_numeric.empty and easier_model.get_feature_encoder():          
        data, _ = easier.datasets.one_hot_encode_data(data, one_hot_encoder= easier_model.get_feature_encoder())
                
    # Use scaler
    input_data = data.values
    if easier_model.get_scaler():
        input_data = easier_model.get_scaler().transform(input_data).reshape(len(input_data),-1)
    
    # Predict
    predictions = easier_model.get_model().predict(input_data)

    # Decode predictions if classifier
    if easier_model.get_label_encoder():
        classes_pred = easier_model.get_label_encoder().inverse_transform(numpy.argmax(predictions, axis=1))
        confidences = [float(prediction[numpy.argmax(predictions, axis=1)][0]) for prediction in predictions]
        return confidences, classes_pred, predictions
    else:
        return None, None, predictions

if __name__== "__main__":
    parser = argparse.ArgumentParser(description='EASIER Model Docker Image')
    parser.add_argument('--port', type=int, help='Port to access model.', default=5000)
    parser.add_argument('--models_path', type=str, help='Path to read models files. Default is /dockerized_model', default='./dockerized_model')
    args = parser.parse_args() # default to system args

    # Initializations
    port = os.getenv("port", args.port)
    easier_user = os.getenv("easier_user")
    easier_password = os.getenv("easier_password")
    easier = EasierSDK(easier_user=easier_user, easier_password=easier_password)

    repo = os.getenv("repo")
    category = os.getenv("category")
    model_name = os.getenv("model_name")
    experimentID = os.getenv("experimentID")

    easier_model = easier.models.get_model(repo_name=repo, category=category, model_name=model_name, experimentID=experimentID)    

    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)

