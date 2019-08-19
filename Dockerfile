FROM python:3.7

COPY . /app

RUN pip install /app

CMD ["python", "/app/door.py"]
