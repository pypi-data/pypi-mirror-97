FROM python:3.6

COPY . /app
WORKDIR /app


RUN pip install -r requirements.txt
RUN mkdir /tmp/test
CMD python -m pytest --junitxml=/tmp/test.xml
