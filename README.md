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

This section provides a guide on managing and accessing the 'api_session' screen session where the 'main.py' Flask application is running.

- **Starting the Screen Session**
  
  1. Start or reattach to the 'api_session' screen session:
     ```bash
     screen -S api_session
     ```
  2. Inside the 'screen' session, navigate to the directory containing 'main.py' and run the Flask application:
     ```bash
     python3 main.py
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

#### **Managing Redis and Celery**

- **Redis Installation and Setup**
  1. Install Redis on the server:
     ```bash
     sudo apt-get install redis-server
     ```
  2. Start the Redis service:
     ```bash
     sudo systemctl start redis.service
     ```
  3. Verify Redis is running:
     ```bash
     redis-cli ping
     ```

- **Running Celery Worker**
  1. Start a screen session for Celery worker:
     ```bash
     screen -S celery_worker
     ```
  2. Run the Celery worker inside the screen session:
     ```bash
     celery -A tasks worker --loglevel=info
     ```
  3. Detach from the screen session:
     Press 'Ctrl + A' followed by 'D'.

- **Monitoring Celery Tasks with Flower**
  1. Start Celery Flower in a new screen session:
     ```bash
     screen -S flower
     celery -A tasks flower
     ```
  2. Detach from the screen session:
     Press 'Ctrl + A' followed by 'D'.

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
5. Inside the 'screen' session, navigate to the directory containing 'main.py' and run the Flask application:
   ```bash
   python main.py
   ```
6. Detach from the screen session using 'Ctrl + A + D'.

---

#### **API Endpoints**

```json
{
  "Endpoints": [
    {
      "Description": "Start the Model",
      "Method": "POST",
      "Body": {
        "org_id": "<org-id>"
      }
    },
    {
      "Description": "Stop the Model",
      "Method": "POST",
      "Body": {
        "org_id": "<org-id>"
      }
    },
    {
      "Description": "Run Inference",
      "Method": "POST",
      "Body": {
        "inference_id": "<inference-id>",
        "domain": "<domain>"
      }
    },
    {
      "Description": "Train Model",
      "Method": "POST",
      "Body": {
        "org_id": "<org-id>"
      }
    }
  ]
}
```

---
