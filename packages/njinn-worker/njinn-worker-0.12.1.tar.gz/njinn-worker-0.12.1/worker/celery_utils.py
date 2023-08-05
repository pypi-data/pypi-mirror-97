from celery import Celery

__celery_app = None


def get_celery_app(broker_url, step=None):
    global __celery_app
    if __celery_app is None:
        __celery_app = Celery("NjinnWorker")

        __celery_app.conf.update(
            enable_utc=True,
            broker_heartbeat=0,
            accept_content=["json"],
            imports=("worker.tasks",),
            broker_url=broker_url,
            worker_prefetch_multiplier=1,
        )
        if step is not None:
            __celery_app.steps["worker"].add(step)
    return __celery_app
