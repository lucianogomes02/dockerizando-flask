FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install poetry
RUN pip install --upgrade pip
RUN pip install poetry
ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /usr/src/app
COPY . .
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

RUN export FLASK_APP=app.py

CMD [ "flask", "run", "--host=0.0.0.0"]
