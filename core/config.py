import os
from enum import Enum
from pydantic.v1 import BaseSettings
from starlette.config import Config

current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_file_dir, "..", ".env")
config = Config(env_path)


class AppSettings(BaseSettings):
    APP_NAME: str = config("APP_NAME", default="dpimsclr-api")
    APP_DESCRIPTION: str | None = config("APP_DESCRIPTION", default=None)
    APP_VERSION: str | None = config("APP_VERSION", default=None)
    LICENSE_NAME: str | None = config("LICENSE", default=None)
    CONTACT_NAME: str | None = config("CONTACT_NAME", default=None)
    CONTACT_EMAIL: str | None = config("CONTACT_EMAIL", default=None)


class TestSettings(BaseSettings):
    ...


class RedisQueueSettings(BaseSettings):
    REDIS_QUEUE_HOST: str = config("REDIS_QUEUE_HOST", default="localhost")
    REDIS_QUEUE_PORT: int = config("REDIS_QUEUE_PORT", default=6379)


class S3BucketSettings(BaseSettings):
    S3_ENDPOINT_URL: str = config("S3_ENDPOINT_URL", default="http://localhost:9000")
    S3_ACCESS_KEY: str | None = config("S3_ACCESS_KEY", default=None)
    S3_SECRET_KEY: str | None = config("S3_SECRET_KEY", default=None)
    S3_QUEUE_BUCKET_NAME: str | None = config("S3_QUEUE_BUCKET_NAME", default=None)
    S3_RESULT_BUCKET_NAME: str | None = config("S3_RESULT_BUCKET_NAME", default=None)


class RateLimitSettings(BaseSettings):
    DEFAULT_RATE_LIMIT: int = config("DEFAULT_RATE_LIMIT", default=10)


class WorkerSettings(BaseSettings):
    JOB_MAX_COUNT: int = config("JOB_MAX_COUNT", default=50)
    JOB_KEEP_RESULT_DURATION: int = config("JOB_KEEP_RESULT_DURATION", default=3600)
    JOB_TIMEOUT: int = config("JOB_TIMEOUT", default=60)
    JOB_MAX_TRY_COUNT: int = config("JOB_MAX_TRY_COUNT", default=3)
    JOB_RETRY_ENABLED: bool = config("JOB_RETRY_ENABLED", default=False)
    JOB_RETRY_DEFER: int = config("JOB_RETRY_DEFER", default=5)
    JOB_ABORT_ENABLED: bool = config("JOB_ABORT_ENABLED", default=False)
    JOB_LOGGING_ENABLED: bool = config("JOB_LOGGING_ENABLED", default=True)


class EnvironmentOption(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = config("ENVIRONMENT", default="local")


class Settings(
    AppSettings,
    TestSettings,
    RateLimitSettings,
    RedisQueueSettings,
    WorkerSettings,
    EnvironmentSettings,
    S3BucketSettings
):
    pass


settings = Settings()
