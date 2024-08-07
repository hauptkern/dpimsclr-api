from arq.connections import RedisSettings
from core.config import settings
from .functions import normal_scale_task, vision_scale_task, shutdown, startup

REDIS_QUEUE_HOST = settings.REDIS_QUEUE_HOST
REDIS_QUEUE_PORT = settings.REDIS_QUEUE_PORT


class WorkerSettings:
    functions = [normal_scale_task, vision_scale_task]
    redis_settings = RedisSettings(host=REDIS_QUEUE_HOST, port=REDIS_QUEUE_PORT)
    on_startup = startup
    on_shutdown = shutdown
    handle_signals = False
    max_jobs = settings.JOB_MAX_COUNT
    keep_results = settings.JOB_KEEP_RESULT_DURATION
    job_timeout = settings.JOB_TIMEOUT
    max_tries = settings.JOB_MAX_TRY_COUNT
    retry_jobs = settings.JOB_RETRY_ENABLED
    allow_abort_jobs = settings.JOB_ABORT_ENABLED
    log_results = settings.JOB_LOGGING_ENABLED
