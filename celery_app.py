from celery import Celery

def make_celery():
    celery = Celery(
        'aris-api-gateway',
        backend='redis://localhost:6379/0',
        broker='redis://localhost:6379/0'
    )
    return celery

celery = make_celery()
