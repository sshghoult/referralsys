FROM python:3.8
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./ ./
RUN chmod +x ./docker-entrypoint.sh

CMD ["sh", "-c", "bash docker-entrypoint.sh"]