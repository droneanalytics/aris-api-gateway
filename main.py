import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
from api_util import (
    add_images_to_s3,
    get_image_from_s3,
    init_aws_services,
    upload_manifest,
    init_mongo_client,
    get_manifest_from_s3,
)
from api_mongo import (
    get_model_arn,
    get_project_name,
    get_model_name,
    update_project_name,
    update_model_name,
    update_model_arn,
    get_training_properties,
)
from error_codes import (
    HTTP_BAD_REQUEST,
    HTTP_CONFLICT,
    HTTP_INTERNAL_SERVER_ERROR,
    ERR_MISSING_JSON_PAYLOAD,
    ERR_MISSING_PARAM,
    ERR_GENERAL_EXCEPTION,
)
#
# Load environment variables
load_dotenv()

app = Flask(__name__)

RUNPOD_IP = "https://6rd3pdsxlbr7a5-4000.proxy.runpod.net"

@app.route("/run_inference", methods=["POST"])
def run_inference_api():
    """
    Gateway to forward requests to the RunPod container and return the response.

    Request Parameters (JSON payload):
        - org_id: Organization ID
        - property_id: Property ID
        - image_name: Name of the image to run inference on
    """
    try:
        incoming_data = request.jsona
        if not incoming_data:
            print("Missing JSON payload.")
            return (
                jsonify({"message": ERR_MISSING_JSON_PAYLOAD}),
                HTTP_BAD_REQUEST,
            )

        # Forward the request to RunPod endpoint
        response = requests.post(RUNPOD_IP + "/run_inference", json=incoming_data)

        # Check if the request was successful
        if response.status_code == 200:
            print("RunPod request successful.")
            # Return the response from the RunPod endpoint
            return jsonify(response.json())
        else:
            print("RunPod request failed.")
            # Forward any error messages from the RunPod endpoint
            return (
                jsonify(response.json()),
                response.status_code,
            )

    except Exception as e:
        return (
            jsonify({"message": ERR_GENERAL_EXCEPTION.format(str(e))}),
            HTTP_INTERNAL_SERVER_ERROR,
        )

@app.route("/train_model", methods=["POST"])
def train_api():
    try:
        incoming_data = request.json
        if not incoming_data:
            print("Missing JSON payload.")
            return (
                jsonify({"message": ERR_MISSING_JSON_PAYLOAD}),
                HTTP_BAD_REQUEST,
            )

        # Forward the request to RunPod endpoint
        response = requests.post(RUNPOD_IP + "/train_model", json=incoming_data)

        # Check if the request was successful
        if response.status_code == 200:
            print("RunPod request successful.")
            # Return the response from the RunPod endpoint
            return jsonify(response.json())
        else:
            print("RunPod request failed.")
            # Forward any error messages from the RunPod endpoint
            return (
                jsonify(response.json()),
                response.status_code,
            )

    except Exception as e:
        print(e)
        return (
            jsonify({"message": ERR_GENERAL_EXCEPTION.format(str(e))}),
            HTTP_INTERNAL_SERVER_ERROR,
        )

@app.route("/start_model", methods=["POST"])
def start_api():
    # Template function for starting model until implemented, for now just returns 200
    return jsonify({"message": "Model started successfully."}), 200

@app.route("/stop_model", methods=["POST"])
def stop_api():
    # Template function for stopping model until implemented, for now just returns 200
    return jsonify({"message": "Model stopped successfully."}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
