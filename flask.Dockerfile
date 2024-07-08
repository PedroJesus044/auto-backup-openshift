FROM python:3.11.5

ENV FLASK_CORS_OPTIONS *
ENV ABKP_DB_HOST auto-backup-mariadb
ENV ABKP_DB_USER auto-backup
ENV ABKP_DB_PASS auto-backup
ENV ABKP_DB_NAME auto-backup
ENV TZ America/Mexico_City

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./Flask/ .

CMD ["flask", "run", "--host=0.0.0.0"]