FROM python:3.10

WORKDIR /flask-app

COPY . /flask-app/

RUN pip install flask

CMD [ "python3", "-m" , "flask", "--app", "app", "run", "--host=0.0.0.0"]
