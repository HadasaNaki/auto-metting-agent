from celery import Celery

app = Celery("worker", broker="redis://redis:6379/0")
app.config_from_object("celeryconfig")
app.autodiscover_tasks(["tasks"])
