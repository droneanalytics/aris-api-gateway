### ARIS API Gateway

Before starting any operation, if accessing remotely, SSH into the Linux server.

---

#### **Clone the Repository**

1. Clone the repository:
   ```bash
   git clone https://github.com/droneanalytics/aris-api-gateway.git
   ```

---

#### **Navigate to the 'aris-api-gateway' Directory**

1. Change directory:
   ```bash
   cd aris-api-gateway
   ```

---

#### **Accessing the 'api_session' Screen Session**

This section provides a guide on managing and accessing the 'api_session' screen session where the 'api_main.py' Flask application is running.

- **Starting the Screen Session**
  
  1. Start or reattach to the 'api_session' screen session:
     ```bash
     screen -S api_session
     ```
  2. Inside the 'screen' session, navigate to the directory containing 'api_main.py' and run the Flask application:
     ```bash
     python3 api_main.py
     ```

- **Detaching from the Screen Session**

  1. Press 'Ctrl + A' followed by 'D' to detach from the 'api_session'. The Flask application will continue running in the background.

- **Reattaching to the Screen Session**

  1. Reattach to the 'api_session' using:
     ```bash
     screen -r api_session
     ```

- **Deleting the Screen Session**

  1. To delete the 'api_session' screen session:
     ```bash
     screen -XS api_session quit
     ```

---

#### **Connecting to the Virtual Environment**

1. Navigate to the 'aris-api-gateway' directory:
   ```bash
   cd aris-api-gateway
   ```
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

---

#### **Hosting the Flask Application**

1. Navigate to the 'aris-api-gateway' directory:
   ```bash
   cd aris-api-gateway
   ```
2. Start or reattach to the 'api_session' screen session:
   ```bash
   screen -S api_session
   ```
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Inside the 'screen' session, navigate to the directory containing 'api_main.py' and run the Flask application:
   ```bash
   python api_main.py
   ```
6. Detach from the screen session using 'Ctrl + A + D'.

---

#### **API Endpoints**

---

- **Start the Model**

  - **Endpoint:** ```/start_model```
  - **Method:** `POST`
  - **Body:**
    ```json
    {
        "org_id": "<org-id>"
    }
    ```
  - **Description:** Initializes AWS services and MongoDB client and starts the model for the given organization ID.

---

- **Stop the Model**

  - **Endpoint:** ```/stop_model```
  - **Method:** `POST`
  - **Body:**
    ```json
    {
        "org_id": "<org-id>"
    }
    ```
  - **Description:** Initializes AWS services and MongoDB client and stops the model for the given organization ID.

---

- **Run Inference**

  - **Endpoint:** ```/run_inference```
  - **Method:** `POST`
  - **Body:**
    ```json
    {
        "model_arn": "<model-arn>",
        "s3_path": "<s3-image-path>"
    }
    ```
  - **Response:**
    ```json
    {
        "CustomLabels": [
            {
                "Name": "string",
                "Confidence": ...,
                "Geometry": {
                    "BoundingBox": {
                        "Width": ...,
                        "Height": ...,
                        "Left": ...,
                        "Top": ...
                    },
                    "Polygon": [
                        {
                            "X": ...,
                            "Y": ...
                        }
                    ]
                }
            }
        ]
    }
    ```
  - **Errors:**
    - 400: Missing JSON payload or required parameter.
    - 409: Model is currently in training.
    - 500: An unspecified error occurred.
  - **Description:** Runs inference on an image using AWS Rekognition's custom labels feature.

---

- **Train Model**

  - **Endpoint:** ```/train_model```
  - **Method:** `POST`
  - **Body:**
    ```json
    {
        "org_id": "<org-id>"
    }
    ```
  - **Description:** Initializes AWS services and MongoDB client, and triggers the training process for the model associated with the given organization ID.

---

- **Create Project**

  - **Endpoint:** ```/create_project```
  - **Method:** `POST`
  - **Body:**
    ```json
    {
        "org_id": "<org-id>"
    }
    ```
  - **Description:** Initializes AWS services and MongoDB client, and creates a new project for the given organization ID.

---
