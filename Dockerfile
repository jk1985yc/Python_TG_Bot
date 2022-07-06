FROM python:3.9.13-slim

WORKDIR /apps

COPY ./apps /apps
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#Time
ENV TW=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TW /etc/localtime && echo $TW > /etc/timezone

CMD ["python", "app.py"]
