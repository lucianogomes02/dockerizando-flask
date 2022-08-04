FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install poetry
RUN pip install poetry
ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /usr/src/app
COPY . .
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

CMD [ "python3", "-m" , "flask", "--app", "app", "run", "--host=0.0.0.0"]
