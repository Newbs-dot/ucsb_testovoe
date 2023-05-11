FROM python:3.8.10

RUN mkdir -p /app/
COPY requirements.txt app/requirements.txt
WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /app/

CMD python3 ./app/main.py