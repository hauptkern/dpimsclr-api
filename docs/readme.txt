dpimsclr-api v.1

Description
-------
Document Image Scaler API using FastAPI, ARQ , Boto3.
It also has separate endpoint that scale images and calculate token costs using GPT-4V conventions.

Setup
-------
1. Clone the repository

git clone git@github.com:hauptkern/dpimsclr-api.git

2. Set environment variables

Create .env file inside the directory of the project,
Inside .env, create the following app settings variables:

APP_NAME="Your app name here"
APP_DESCRIPTION="Your app description here"
APP_VERSION="0.1"
CONTACT_NAME="Your name"
CONTACT_EMAIL="Your email"
LICENSE_NAME="The license you picked"
ENVIRONMENT="local"
DEFAULT_RATE_LIMIT=10
S3_ENDPOINT_URL="http://192.168.1.31:9000"
S3_ACCESS_KEY="YOUR_S3_ACCESS_KEY"
S3_SECRET_KEY="YOUR_S3_SECRET_KEY"
S3_QUEUE_BUCKET_NAME="docimg-queue"
S3_RESULT_BUCKET_NAME="docimg-result"
REDIS_QUEUE_HOST="localhost"
REDIS_QUEUE_PORT=6379
JOB_MAX_COUNT=100
JOB_KEEP_RESULT_DURATION=3600
JOB_TIMEOUT=60
JOB_MAX_TRY_COUNT=5
JOB_RETRY_ENABLED=1
JOB_RETRY_DEFER=5
JOB_ABORT_ENABLED=0
JOB_LOGGING_ENABLED=1

3. Set virtual environment

Create a virtual environment inside the directory of the project using:
python -m venv .venv
and activate the virtual environment.

4. Install dependencies

Install the dependencies using:
pip install -r requirements.txt

5. Run services

Run the backend service using:
uvicorn main:app --host 0.0.0.0 --port 8000

Run the worker service using:
arq core.worker.settings.WorkerSettings
