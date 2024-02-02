import os
import runpod
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
    init_runpod_client,
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

# Init runpod client
runpod.api_key = os.getenv("RUNPOD_API_KEY")
pod_id = os.getenv("POD_ID")

app = Flask(__name__)

runpod_ip = os.getenv("RUNPOD_IP")

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
        print("test")
        print(runpod_ip + "/run_inference")
        incoming_data = request.json
        if not incoming_data:
            print("Missing JSON payload.")
            return (
                jsonify({"message": ERR_MISSING_JSON_PAYLOAD}),
                HTTP_BAD_REQUEST,
            )

        # Forward the request to RunPod endpoint
        response = requests.post(runpod_ip + "/run_inference", json=incoming_data)

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
        response = requests.post(runpod_ip + "/train_model", json=incoming_data)

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
def start_model():
    resume = runpod.resume_pod(pod_id=pod_id, gpu_count=1)
    return jsonify({"message": resume}), 200

@app.route("/stop_model", methods=["POST"])
def stop_model():
    stop = runpod.stop_pod(pod_id)
    return jsonify({"message": stop}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
