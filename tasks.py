from celery_app import celery
import requests
from requests.exceptions import RequestException
import redis

@celery.task(bind=True, max_retries=None, default_retry_delay=60)
def send_request_to_runpod(self, data):
    r = redis.Redis(host='localhost', port=6379, db=0)
    runpod_ip = r.get('runpod_ip').decode('utf-8')
    print(runpod_ip)
    url = f"{runpod_ip}/run_inference"

    # Include the Celery task ID in the request data
    data['task_id'] = self.request.id

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    except RequestException as exc:
        print(f"Request failed: {exc}, retrying...")
        self.retry(exc=exc)
