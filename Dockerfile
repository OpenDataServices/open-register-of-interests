FROM python:3.8
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD python /code/oroi/manage.py runserver 0.0.0.0:8001
