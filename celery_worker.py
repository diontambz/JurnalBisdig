from celery import Celery
from app import create_app  # Asumsi Anda memiliki fungsi factory `create_app` di app.py

app = create_app()
app.app_context().push()

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)