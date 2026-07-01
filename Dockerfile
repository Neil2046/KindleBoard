FROM python:3.12-alpine

WORKDIR /app
COPY app.py /app/app.py
COPY static /app/static
COPY data/schedule.db /app/default-data/schedule.db

ENV DATA_DIR=/data
ENV PORT=10000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

VOLUME ["/data"]
EXPOSE 10000

CMD ["python", "app.py"]
