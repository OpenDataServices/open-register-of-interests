FROM python:3.8.3-buster
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
CMD sh -c ' \
    ./manage.py migrate && \
    ./manage.py search_index --rebuild -f && \
    ./manage.py csv_user_dump_all && \
    mkdir -p ui/static/ && \
    mv /tmp/all_data.csv ui/static && \
    ./manage.py runserver 0.0.0.0:8001 \
    '
