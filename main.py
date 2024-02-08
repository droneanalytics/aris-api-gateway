import os
import runpod
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
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
        incoming_data = request.json
        print(incoming_data)
        if not incoming_data:
            print("Missing JSON payload.")
            return (
                jsonify({"message": ERR_MISSING_JSON_PAYLOAD}),
                HTTP_BAD_REQUEST,
            )
        print(runpod_ip + "/run_inference")
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
    # resume = runpod.resume_pod(pod_id=pod_id, gpu_count=1)
    docker_args = """bash -c 'apt update;DEBIAN_FRONTEND=noninteractive apt-get install openssh-server -y;mkdir -p ~/.ssh;cd $_;chmod 700 ~/.ssh;echo '$PUBLIC_KEY' >> authorized_keys;chmod 700 authorized_keys;cd /mmdetection;pip install -e .;cd app;pip install -r requirements.txt;cd ..;service ssh start;cd /mmdetection/app;uvicorn main:app --host 0.0.0.0 --port 4000'"""
    
    pod = runpod.create_pod(
        name="aris-runpod", 
        image_name="arken22/aris:runpod", 
        gpu_type_id="NVIDIA GeForce RTX 4090", 
        cloud_type="SECURE", 
        container_disk_in_gb=5, 
        docker_args=docker_args,
        ports="4000/http,22/tcp,43201/tcp", 
        volume_mount_path="/mmdetection", 
        template_id="u228fcbb71", 
        network_volume_id="wcuy34u9z9")
    # Get pod id
    global pod_id
    pod_id = pod["id"]
    return jsonify({"message": pod}), 200

@app.route("/stop_model", methods=["POST"])
def stop_model():
    stop = runpod.terminate_pod(pod_id)
    return jsonify({"message": stop}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
