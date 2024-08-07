FROM python:3.11-slim

RUN adduser --disabled-password --gecos "" --no-create-home dpimsclr

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app
RUN chown -R dpimsclr:dpimsclr /app

USER dpimsclr

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Uncomment the following line if using Gunicorn
# CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
