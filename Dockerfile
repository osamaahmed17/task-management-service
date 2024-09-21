FROM python:3.12.1-alpine3.18
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 8000
CMD uvicorn src.main:app --reload --env-file .env --host 0.0.0.0 --port 8000