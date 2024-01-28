from PIL import Image
import boto3
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np
import json
from concurrent.futures import ThreadPoolExecutor
import io


# Initialize AWS services and return rekognition and s3 clients
def init_aws_services():
    load_dotenv()
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION")

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    rekognition = session.client("rekognition")
    s3 = session.client("s3")

    return rekognition, s3


def init_mongo_client():
    load_dotenv()
    try:
        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASS")

        if not db_host or not db_user or not db_pass:
            raise ValueError("Database credentials are not set properly")

        client = MongoClient(f"mongodb+srv://{db_user}:{db_pass}@{db_host}/?retryWrites=true&w=majority")
        return client

    except Exception as e:
        raise ValueError(f"Error initializing MongoDB client: {e}")


def get_class_id(client, class_label, org_id):
    # Get the damageLabelData collection from the droneanalytics database
    damageLabelData = client[org_id]["damageLabelData"]
    class_slug = class_label.lower().replace(" ", "-")
    # print("looking for:", class_label.lower().replace(" ", "-"))
    # Search for a document in the damageLabelData collection where the slug is equal to the class_label
    existing_doc = damageLabelData.find_one({"label": class_label})

    max_class_id_doc = damageLabelData.find_one(sort=[("classId", -1)])
    max_class_id = max_class_id_doc["classId"] if max_class_id_doc else 0

    if existing_doc:
        # check if class_id exists, if not get max_class_id and increment
        if "classId" not in existing_doc:
            max_class_id = max_class_id + 1
            print("adding class_id", max_class_id, class_label)
            damageLabelData.update_one(
                {"label": class_label},
                {"$set": {"slug": class_slug, "classId": max_class_id}},
            )
            return max_class_id
        # If a document is found, return the class_id from that document
        return existing_doc["classId"]
    else:
        # If no document is found, find the current maximum class_id in damageLabelData
        # Increment the max_class_id to create a new unique class_id
        max_class_id = max_class_id + 1

        print("adding new class", class_label, class_slug, max_class_id)
        damageLabelData.insert_one(
            {
                "label": class_label,
                "slug": class_label.lower().replace(" ", "-"),
                "description": "",
                "class_id": max_class_id,
            }
        )

        # Return the new class_id
        return max_class_id


def get_image_from_s3(s3, bucket_name, s3_path):
    image = s3.get_object(Bucket=bucket_name, Key=s3_path)["Body"].read()
    image = Image.open(io.BytesIO(image))
    image = np.array(image)
    return image


def get_manifest_from_s3(s3, org_id, model_name):
    bucket = "drone-analytics-assets"
    manifest_key = f"{model_name}.manifest"
    key = f"{org_id}/manifests/{manifest_key}"

    # Retrieve manifest data from S3 as bytes
    manifest_data_bytes = s3.get_object(Bucket=bucket, Key=key)["Body"].read()

    # Decode the manifest data to a string using the appropriate character encoding
    manifest_data = manifest_data_bytes.decode("utf-8")

    # Split the JSON data by newline and remove empty strings
    json_list = [
        json_str.strip() for json_str in manifest_data.split("\n") if json_str.strip()
    ]

    # Concatenate the JSON objects into a single string
    final_json = "\n".join(json_list)

    return final_json


# Upload Manifest File
def upload_manifest(s3, manifest_name, org_id, manifest_path):
    bucket_name = "drone-analytics-assets"
    manifest_key = f"{org_id}/manifests/{manifest_name}"
    s3.upload_file(manifest_path, bucket_name, manifest_key)


def put_manifest(s3, manifest_name, org_id, manifest_content):
    bucket_name = "drone-analytics-assets"
    manifest_key = f"{org_id}/manifests/{manifest_name}.manifest"

    # Assuming manifest_content is a string
    s3.put_object(Body=manifest_content, Bucket=bucket_name, Key=manifest_key)
    print("Manifest Uploaded:", manifest_name)


# Add Images to S3
def add_images_to_s3(s3, bucket_name, image):
    s3.upload_file(image, bucket_name, image)


if __name__ == "__main__":
    # test get_manifest_from_s3 function
    rekognition, s3 = init_aws_services()

    property_id = "650163c6f0900337718efe3c"
    manifest_name = "model_v1694365758.manifest"

    manifest = get_manifest_from_s3(s3, property_id, manifest_name)
