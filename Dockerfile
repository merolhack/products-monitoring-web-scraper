# syntax=docker/dockerfile:1
FROM python:3.7
ENV PYTHONIOENCODING utf-8
WORKDIR /src
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
USER 1000
CMD [ "python", "./app.py" ]
