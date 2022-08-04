FROM python:3.10

RUN python3 -m venv /opt/virtualenv

# This is wrong!
RUN . /opt/virtualenv/bin/activate

# Install dependencies:
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app.py .

CMD [ "python3", "-m" , "flask", "--app", "app", "run", "--host=0.0.0.0"]
