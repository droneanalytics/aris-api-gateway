import runpod
from flask import Flask, request, jsonify
import os
import requests
from celery import Celery
from dotenv import load_dotenv
from requests.exceptions import RequestException
from error_codes import (
    HTTP_BAD_REQUEST,
    HTTP_CONFLICT,
    HTTP_INTERNAL_SERVER_ERROR,
    ERR_MISSING_JSON_PAYLOAD,
    ERR_MISSING_PARAM,
    ERR_GENERAL_EXCEPTION,
    ERR_MISSING_REQUIRED_FIELDS
)
import redis
# Import Celery instance
from celery_app import celery
from tasks import send_request_to_runpod

# Load environment variables
load_dotenv()

# Initialise Celery
app = Flask(__name__)
# Init runpod client
runpod.api_key = os.getenv("RUNPOD_API_KEY")
# Init redis
r = redis.Redis(host='localhost', port=6379, db=0)

global pod_id
pod_id = "pod_id"
global runpod_ip
runpod_ip = f"https://{pod_id}-4000.proxy.runpod.net"
r.set('runpod_ip', runpod_ip)

# Endpoint to check the status of a task
@app.route("/task_status/<task_id>", methods=["GET"])
def task_status(task_id):
    task = celery.AsyncResult(task_id)
    return jsonify({
        'status': task.status,
        'result': task.result
    })

@app.route("/run_inference", methods=["POST"])
def run_inference_api():
    try:
        incoming_data = request.json
        if not incoming_data:
            print("No data received")
            return jsonify({"message": ERR_MISSING_JSON_PAYLOAD}), HTTP_BAD_REQUEST

        if "inference_id" not in incoming_data or "domain" not in incoming_data:
            print("Required fields missing")
            return jsonify({"message": ERR_MISSING_REQUIRED_FIELDS}), HTTP_BAD_REQUEST

        task = send_request_to_runpod.apply_async(args=[incoming_data])
        print(f"Task {task.id} enqueued")
        return jsonify({"message": "Request enqueued", "task_id": task.id}), 202

    except Exception as e:
        print(f"Exception: {str(e)}")
        return jsonify({"message": ERR_GENERAL_EXCEPTION.format(str(e))}), HTTP_INTERNAL_SERVER_ERROR

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
    global pod_id
    global runpod_ip
    docker_args = """bash -c 'apt update;DEBIAN_FRONTEND=noninteractive apt-get install openssh-server -y;mkdir -p ~/.ssh;cd $_;chmod 700 ~/.ssh;echo '$PUBLIC_KEY' >> authorized_keys;chmod 700 authorized_keys;cd /mmdetection;pip install -e .;cd app;pip install -r requirements.txt;cd ..;service ssh start;sleep infinity'"""
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
    pod_id = pod["id"]
    runpod_ip = f"https://{pod_id}-4000.proxy.runpod.net"
    r.set('runpod_ip', runpod_ip)
    print(runpod_ip)
    return jsonify({"message": pod}), 200

@app.route("/stop_model", methods=["POST"])
def stop_model():
    global pod_id
    stop = runpod.terminate_pod(pod_id)
    return jsonify({"message": stop}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
