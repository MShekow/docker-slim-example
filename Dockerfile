FROM python:3.11.9

WORKDIR /app

COPY service .

RUN pip install -r requirements.txt

EXPOSE 9000
CMD ["/app/run.sh"]
