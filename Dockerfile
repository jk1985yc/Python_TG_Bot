FROM python:3.9.13-slim

WORKDIR /apps

COPY ./apps /apps
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]
