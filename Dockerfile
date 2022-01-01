FROM python:3.10

COPY service /opt/my/service

WORKDIR /opt/my/service

RUN pip install -r requirements.txt

EXPOSE 9000
ENTRYPOINT ["/opt/my/service/run.sh"]


