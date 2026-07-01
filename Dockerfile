FROM python:3.12-slim

WORKDIR /app
COPY app.py /app/app.py
COPY static /app/static
COPY data/schedule.db /app/default-data/schedule.db

ENV DATA_DIR=/data
ENV PORT=10000

VOLUME ["/data"]
EXPOSE 10000

CMD ["python", "app.py"]
