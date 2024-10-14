FROM python:3.12-alpine

WORKDIR /app

ADD . /app/orb-task-02

WORKDIR /app/orb-task-02

RUN pip install --upgrade pip

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

RUN poetry shell

CMD python ./src/manage.py migrate & python ./src/manage.py collectstatic --no-input & python ./src/manage.py runserver 0.0.0.0:8080
